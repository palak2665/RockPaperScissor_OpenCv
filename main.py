import random
import time
import cv2
import cvzone
import handTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = htm.HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0]  #[AI, Human]

while True:
    imgbg = cv2.imread('E:\\Projects\\RockPaperScissor_opencv\\Resources\\BG.png')
    success,img = cap.read()
    
    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)
    imgScaled = imgScaled[:,80:480]

    # Find hands
    hands, img = detector.findHands(imgScaled)
    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgbg,str(int(timer)),(605,435),cv2.FONT_HERSHEY_PLAIN,6,(255,0,0),4)

        if timer > 3:
            stateResult = True
            timer = 0

            if hands:
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                if fingers == [0,0,0,0,0]:
                    playerMove = 1
                if fingers == [1,1,1,1,1]:
                    playerMove = 2
                if fingers == [0,1,1,0,0]:
                    playerMove = 3

                randomNumber = random.randint(1, 3)
                imgAI = cv2.imread(f'E:\\Projects\\RockPaperScissor_opencv\\Resources\\{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                imgbg = cvzone.overlayPNG(imgbg,imgAI,(149,310))
                
                # Player Wins
                if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI Wins
                if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                
                # print(playerMove)
            

    imgbg[236:656,794:1194] = imgScaled

    if stateResult:
        imgbg = cvzone.overlayPNG(imgbg,imgAI,(149,310))
    cv2.putText(imgbg,str(scores[0]),(410,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    cv2.putText(imgbg,str(scores[1]),(1112,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    # cv2.imshow('capture',img)
    cv2.imshow('BG',imgbg)
    # cv2.imshow('scaled',imgScaled)
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    elif key == ord('q'):
        break
    