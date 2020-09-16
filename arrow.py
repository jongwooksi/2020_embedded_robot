import platform
import numpy as np
import argparse
import cv2
import serial
import time
from serialdata import *


if __name__ == '__main__':

    BPS =  4800  # 4800,9600,14400, 19200,28800, 57600, 115200

       
    serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
    serial_port.flush() # serial cls
    serial_t = Thread(target=Receiving, args=(serial_port,))
    serial_t.daemon = True
    serial_t.start()
        
    W_View_size = 320
    H_View_size = int(W_View_size / 1.333)

    FPS         = 10  #PI CAMERA: 320 x 240 = MAX 90

    cap = cv2.VideoCapture(0)

    cap.set(3, W_View_size)
    cap.set(4, H_View_size)
    cap.set(5, FPS)  
    
    left_count = 0
    right_count = 0
    TX_data_py2(serial_port, 43)
    
    while True:
        _,frame = cap.read()

        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 0, 0])
        upper_red = np.array([180, 236, 152])

        mask = cv2.inRange(hsv, lower_red, upper_red)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode(mask, kernel)

        contours,_ = cv2.findContours(mask , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt,True),True)
          
            
            if area > 2000 and area < 320*180:

                points = []
               
                if len(approx)==7:
                    
                    for i in range(7):
                       points.append([approx.ravel()[2*i], approx.ravel()[2*i+1]])

                    points.sort()
                   
                    minimum = points[1][0] - points[0][0]
                    maximum = points[6][0] - points[5][0]

                    if maximum < minimum :
                        left_count += 1
                    else:
                        right_count += 1
                    
                    cv2.drawContours(frame,[approx],0,(0,0,0),5)
                    
                
              
        if left_count>right_count and left_count > 10:
            f = open("arrow.txt", 'w')
            print("left")
            f.write("left")
            exit(1)
            
        if left_count<right_count and right_count > 10:
            f = open("arrow.txt", 'w')
            print("right")
            f.write("right")
            exit(1)
           
           
        cv2.imshow("Frame",frame)
        time.sleep(0.1)
        #cv2.imshow("MASK",mask)

        key = cv2.waitKey(1)
        if key ==27:
            break
       
       
    

f.close()
cap.release()
cv2.destroyAllWindows()    
