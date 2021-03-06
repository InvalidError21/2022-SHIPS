#!/usr/bin/python
import math
import numpy as np
import cv2
import pyfirmata as pf
import time

#dictionary of all contours
contours = {}
#array of edges of polygon
approx = []
#scale of the text
scale = 2
#camera
cap = cv2.VideoCapture(0)

board = pf.Arduino('/dev/ttyACM0')
LeftM = board.get_pin('d:9:s')
RightM = board.get_pin('d:10:s')

board.pass_time(2)

LeftM.write(1500)
RightM.write(1500)

board.pass_time(2)


print('wait')

#calculate angle
def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)

while(cap.isOpened()):
    #Capture frame-by-frame
    ret, frame = cap.read()
    

    
    #blue=0.02 , g,r=0.04
    #lower_blue1 = np.array([140, 120, 15]) #red
    #upper_blue1 = np.array([180, 255, 255]) #red
    #lower_blue1 = np.array([40, 10, 10]) #green
    #upper_blue1 = np.array([100, 85, 85]) #green
    lower_blue1 = np.array([116, 99, 20]) #blue
    upper_blue1 = np.array([121, 225, 255]) #blue



    
    if ret==True:
        #grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #Canny
        #canny = cv2.Canny(frame,100,200)
        hsv1 = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        
        
        img_mask = cv2.inRange(hsv1, lower_blue1, upper_blue1)
        
    
        kernel = np.ones((11,11), np.uint8)
        #img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
        #img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)

        img_result = cv2.bitwise_and(frame, frame, mask=img_mask)
       
        numOfLabels, img_label, stats, centroids = cv2.connectedComponentsWithStats(img_mask)

        for idx, centroid in enumerate(centroids):
            if stats[idx][0] == 0 and stats[idx][1] == 0:
                continue

            if np.any(np.isnan(centroid)):
                continue

        x1,y1,width,height,area1 = stats[idx]
        centerX,centerY = int(centroid[0]), int(centroid[1])
        canny3 = cv2.cvtColor(img_result,cv2.COLOR_BGR2GRAY)
        #canny3 = cv2.Canny(img_result,100,200)
        

    
        #contours
        canny2, contours, hierarchy = cv2.findContours(canny3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0,len(contours)):
            #approximate the contour with accuracy proportional to
            #the contour perimeter
            approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.04,True)

            #Skip small or non-convex objects
            if(abs(cv2.contourArea(contours[i]))< 300 or not(cv2.isContourConvex(approx))):
                continue
            
            if(len(approx) ==3):
                    
                x,y,w,h = cv2.boundingRect(contours[i])
                if(x> 1950 and x<2630):
                            print(x)
                            LeftM.write(1450)
                            RightM.write(1600)

                elif(x>2630) and x<2870:
                            print(x)
                            LeftM.write(1450)
                            RightM.write(1550)
                            #LeftM.write(1500)
                            #RightM.write(1500)                            
                elif(x>2870 and x<3700):
                            print(x)
                            LeftM.write(1400)
                            RightM.write(1550)


                else:
                            print(x)
                            LeftM.write(1500)
                            RightM.write(1500)
                            #board.pass_time(1)
                            #LeftM.write(1500)
                            #RightM.write(1500)  
                cv2.putText(frame,'({} , {})'.format(x,y),(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                    #print(x,y)
                        
                       

        #Display the resulting frame
        #out.write(frame)
        frame = cv2.resize(frame,(800,400))
        img_result = cv2.resize(img_result,(800,400))
        cv2.imshow('frame',frame)
        cv2.imshow('canny',img_result)
        if cv2.waitKey(1) == 1048689: #if q is pressed
            break

#When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
