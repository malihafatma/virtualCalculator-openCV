import cv2
from cvzone .HandTrackingModule import HandDetector


class Button:
    def __init__(self, pos, width, height, value,  text_color=(255, 255, 255),
                     bg_color = (50, 50, 50), border_color=(102, 205, 170)):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      self.bg_color, cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      self.bg_color, 3)
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN,
                    2, self.text_color, 2)

    def checkclick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False


# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
detector = HandDetector(detectionCon=0.8, maxHands=1)

# creating buttons
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]
clearButton = Button((800, 600), 400, 100, "Clear")


buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 100 + 800
        ypos = y * 100 + 150
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))


# variables
myEquation = ''
delayCounter = 0


# loop
while True:
    # get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # detection of hand
    hands, img = detector.findHands(img, flipType=False)

    # draw all buttons
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100),
                  (102, 205, 170), cv2.FILLED)
    cv2.rectangle(img, (800, 50), (800 + 400, 70 + 100),
                  (50, 50, 50), 3)

    # Draw all buttons including the Clear button
    for button in buttonList + [clearButton]:
        button.draw(img)

    # check for hands
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        x, y, _ = lmList[8]
        if length < 50:
            for i, button in enumerate(buttonList):
                if button.checkclick(x, y) and delayCounter == 0:
                    myValue = buttonListValues[int(i % 4)][int(i / 4)]
                    if myValue == "=":
                        myEquation = eval(myEquation)
                    else:
                        myEquation += myValue
                    delayCounter = 1

    # Check for clicks on the Clear button
    if clearButton.checkclick(x, y) and delayCounter == 0:
        myEquation = ''  # Clear the equation
        delayCounter = 1

    # to avoid Duplicate
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    # display the Equation/Result
    cv2.putText(img, str(myEquation), (810, 120), cv2.FONT_HERSHEY_PLAIN,
                3, (50, 50, 50), 3)

    # display image
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''
