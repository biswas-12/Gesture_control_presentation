import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cv2

#variables
width , height = 1600 , 1080
folderPath = "Presentation"

#camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)


# get the list of presentation images
pathImages =sorted(os.listdir(folderPath), key=len)
#print(pathImages)

#variables
imgNumber = 0
hs, ws = int(120*1), int(220*1)
gestureThreshold = 300
buttonPressed = False
buttonCount = 0
buttonDelay = 30
annotation = [[]]
annotationNumber = -1
annotationStart = False
#hand Detector
detector = HandDetector(detectionCon=0.8 , maxHands=1 )


while True :
    #import images
    success, img =cap.read()
    img = cv2.flip(img,1)
    pathFullImages = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImages)

    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold),(width, gestureThreshold), (0,255,0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        lmList = hand['lmList']

        indexFinger = lmList[8][0] , lmList[8][1]
        xval = int(np.interp(lmList[8][0], [width//2 , w], [0, width]))
        yval = int(np.interp(lmList[8][1], [250 , height-250], [0, height]))
        #indexFinger = xval,yval



        if cy <= gestureThreshold : # if hand is at the height of face

            #gesture 1 - left
            if fingers == [1, 0, 0, 0, 0] :
                print("Left")
                if imgNumber >0 :
                    buttonPressed = True
                    annotation = [[]]
                    annotationNumber = -1
                    annotationStart = False
                    imgNumber -= 1

            # gesture 2 - right
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                if imgNumber < len(pathImages)-1 :
                    buttonPressed = True
                    annotation = [[]]
                    annotationNumber = -1
                    annotationStart = False
                    imgNumber += 1

        #gesture 3 - show pointer
        if fingers == [0, 1, 1, 0, 0]:
             cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 225), cv2.FILLED)

        # gesture 4 - draw pointer
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotation.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 225), cv2.FILLED)
            annotation[annotationNumber].append(indexFinger)
        else :
            annotationStart = False

        # gesture 5 - erase
        if fingers == [1, 1, 1, 1, 1]:
           if annotation:
               annotation.pop(-1)
               annotationNumber -= 1
               buttonPressed = True


    #button pressed itteration
    if buttonPressed:
        buttonCount += 1
        if buttonCount > buttonDelay :
                buttonCount = 0
                buttonPressed = False

    for i  in range (len(annotation) ):
        for j in range (len(annotation[i])) :
            if j!=0 :
                cv2.line(imgCurrent, annotation[i][j-1], annotation[i][j], (0, 0, 200), 12)


    #adding webcam image on slides
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q') :
        break