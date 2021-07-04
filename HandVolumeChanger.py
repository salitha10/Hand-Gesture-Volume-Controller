import cv2 as cv
import time
import numpy as np
#import mediapipe as mp
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv.VideoCapture(0)
pTime = 0

detector = htm.handDetector(detConf=0.7)


# volume controller
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()

    detector.findHands(img)
    lmList = detector.handPosition(img, draw=False)

    if len(lmList) != 0:
        print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2


        # Thumb and sencond fonger
        cv.circle(img, (x1, y1), 8, (255,0,255), cv.FILLED)
        cv.circle(img, (x2, y2), 8, (255,0,255), cv.FILLED)
        cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv.circle(img, (cx, cy), 8, (255,0,255), cv.FILLED)

        # Get length between draw_landmarks
        length = math.hypot(x2 - x1, y2 - y1)
        print(length)

        # Hand Range 50 - 300
        # Volume Range -65 - 0

        # Convert hand range to volume range
        vol = np.interp(length, [10,150], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        # Volume bar
        volBar = np.interp(length, [10,150], [400, 100])

        # Volume percentage
        volPer = np.interp(length, [10,150], [0, 100])
        

        # If fingers touch
        if length < 20 :
            cv.circle(img, (cx, cy), 8, (0,255,0), cv.FILLED)

    # Indicator
    cv.rectangle(img, (50,100), (85, 400), (0,255, 255), 3)
    cv.rectangle(img, (50,int(volBar)), (85, 400), (0,255, 255), cv.FILLED)

    #Fps
    cTime = time.time()
    fps = 1 / (cTime-pTime)
    pTime = cTime

    cv.putText(img, f'FPS: {int(fps)}', (10,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
    cv.putText(img, f'FPS: {int(fps)}', (10,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)

     # Vol Percentage
    cv.putText(img, f'{int(volPer)} %', (40,450), cv.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)


    # Show
    cv.imshow('Img', img)
    cv.waitKey(1)