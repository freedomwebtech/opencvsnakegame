import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import cvzone
import numpy as np
import random
import vlc
detector=HandDetector(detectionCon=0.5,maxHands=1)
player = vlc.MediaPlayer("/home/pi/opencvsnakegame/m.mp3")
player1 = vlc.MediaPlayer("/home/pi/opencvsnakegame/m1.mp3")


     
cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    hands,frame=detector.findHands(frame)  
    if hands:
        hands1=hands[0]
        lmlist=hands1['lmList']
        x=lmlist[8][0]
        y=lmlist[8][1]
        pointindex=(x,y)
       
        
       
    
       
    frame=cv2.imshow("FRAME",frame)
    key=cv2.waitKey(1)
    if key == ord('r'):
       gameplay.gameover=False
       break
cap.release()
cv2.destroyAllWindows()
    
