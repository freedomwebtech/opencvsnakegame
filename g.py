import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import cvzone
import numpy as np
import random
import vlc
detector=HandDetector(detectionCon=0.5,maxHands=1)
player = vlc.MediaPlayer("/home/pi/Downloads/m.mp3")
player1 = vlc.MediaPlayer("/home/pi/Downloads/m1.mp3")

class snakegame():
    def __init__(self,pathfood):
        self.points=[]
        self.length=[]
        self.currentlength=0
        self.prevheadofsnake=0,0
        self.allowedlengthofsnake=50
        self.gameover=False
        self.food=cv2.imread(pathfood,cv2.IMREAD_UNCHANGED)
        self.food=cv2.resize(self.food,(60,50))
        self.wfood,self.hfood,_=self.food.shape
        self.foodpoints=0,0
        self.foodlocation()
        self.score=0
    def foodlocation(self):
        self.foodpoints=random.randint(100,600),random.randint(100,400)
    def update(self,img,currentheadofsnake):
        if self.gameover:
            cvzone.putTextRect(img,"GAME OVER",[140,150],scale=5,thickness=3,offset=20)
            player.stop()
            player1.play()
        else:    
            
             px,py=self.prevheadofsnake
             cx,cy=currentheadofsnake
             self.points.append([cx,cy])
             distance=math.hypot(px-cx,py-cy)
             self.length.append(distance)
             self.currentlength+=distance
             self.prevheadofsnake=cx,cy
             player.play()
        
             if self.currentlength > self.allowedlengthofsnake:
                for i ,length in enumerate(self.length):
                    self.currentlength-=length
                    self.points.pop(i)
                    self.length.pop(i)
             rx,ry=self.foodpoints
             if rx -self.wfood//2 < cx < rx +self.wfood//2 and ry -self.hfood//2 < cy < ry +self.hfood//2:
                self.foodlocation()
                self.allowedlengthofsnake+=30
                self.score+=1
             if self.points:
                for i,points in enumerate(self.points):
                    if i!=0:
                       cv2.line(img,self.points[i -1],self.points[i],(255,0,0),10)
                cv2.circle(img,self.points[-1],12,(0,0,255),-1)
             pts=np.array(self.points[:-3],np.int32)
             pts=pts.reshape((-1,1,2))
             img=cv2.polylines(img,[pts],False,(0,255,0),3)
             mdistance=cv2.pointPolygonTest(pts,(cx,cy),True)
             img=cvzone.overlayPNG(img,self.food,(rx -self.wfood//2,ry -self.hfood//2))
#             cvzone.putTextRect(img,f'game score{self.score}',[30,40],scale=5,thickness=3,offset=20)
             cvzone.putTextRect(img,f'score{self.score}',[30,50],scale=2,thickness=2,offset=20)   
             if -1<= mdistance <=1:
                print("HIT")
                self.gameover=True
                self.currentlength=0
                self.prevheadofsnake=0,0
                self.allowedlengthofsnake=50
                self.foodlocation()
                
        return img 
cap=cv2.VideoCapture(0)
gameplay=snakegame("/home/pi/Downloads/food2.png")
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
        frame=gameplay.update(frame,pointindex)
        
      
        
       
    
       
    frame=cv2.imshow("FRAME",frame)
    key=cv2.waitKey(1)
    if key == ord('r'):
       gameplay.gameover=False
       break
cap.release()
cv2.destroyAllWindows()
    
