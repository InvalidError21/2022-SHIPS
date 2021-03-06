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
LeftM = board.get_pin('d:11:s')
RightM = board.get_pin('d:9:s')

board.pass_time(2)

LeftM.write(1500)
RightM.write(1500)
print('wait')

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

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
    

    
    
    #lower_blue1 = np.array([140, 120, 15]) #red
    #upper_blue1 = np.array([180, 255, 255]) #red
    #lower_blue1 = np.array([40, 10, 10]) #green
    #upper_blue1 = np.array([100, 85, 85]) #green
    lower_blue1 = np.array([112, 100, 15]) #blue
    upper_blue1 = np.array([126, 225, 255]) #blue



    
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
        canny3 = cv2.Canny(img_result,100,200)
        

    
        #contours
        canny2, contours, hierarchy = cv2.findContours(canny3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            #approximate the contour with accuracy proportional to
            #the contour perimeter
            approx = cv2.approxPolyDP(contour,cv2.arcLength(contour,True)*0.01,True)

            #Skip small or non-convex objects
            if(abs(cv2.contourArea(contour))< 10 or not(cv2.isContourConvex(approx))):
                continue
                  
            if len(approx) >= 10:
                
              
                    #detect circle
                
                area = cv2.contourArea(contour)
                        
                x,y,w,h = cv2.boundingRect(contour)
                        # x = 1900~3600
                
                if(x> 1950 and x<2630):
                            print(x)
                            LeftM.write(1470)
                            RightM.write(1560)

                elif(x>2630) and x<2870:
                            print(x)
                            LeftM.write(1440)
                            RightM.write(1560)
                            #LeftM.write(1500)
                            #RightM.write(1500)                            
                elif(x>2870 and x<3700):
                            print(x)
                            LeftM.write(1460)
                            RightM.write(1530)


                else:
                            print(x)
                            LeftM.write(1500)
                            RightM.write(1500)
                            #board.pass_time(1)
                            #LeftM.write(1500)
                            #RightM.write(1500)                
                            
                        
                radius = w/2
                if(abs(1 - (float(w)/h))<=2 and abs(1-(area/(math.pi*radius*radius)))<=0.3):
                        cv2.putText(frame,'({} , {})'.format(x,y),(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                                
        frame = cv2.resize(frame,(800,400))
        img_result = cv2.resize(img_result,(800,400))
        cv2.imshow('frame',frame)
        cv2.imshow('canny',img_result)
        if cv2.waitKey(1) == 1048689: #if q is pressed
            break                
                       



#When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
