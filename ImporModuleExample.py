import cv2 as cv
import mediapipe as mp
import time
import HandTrackingModule as htm

# Get webcam
cam = cv.VideoCapture(0)

pTime = 0
cTime = 0

detector = htm.handDetector()

while True:
    success, img = cam.read()

    detector.findHands(img)
    lmList = detector.handPosition(img)

    if len(lmList) != 0:
        print(lmList[0])

    # Calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display FPS
    cv.putText(img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

    # Show frame
    cv.imshow("Image", img)
    cv.waitKey(1)