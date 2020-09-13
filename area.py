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
    
        
    W_View_size = 320
    H_View_size = int(W_View_size / 1.333)

    FPS         = 20  #PI CAMERA: 320 x 240 = MAX 90


    cap = cv2.VideoCapture(0)

    cap.set(3, W_View_size)
    cap.set(4, H_View_size)
    cap.set(5, FPS)  
    

    TX_data_py2(serial_port, 31)
	
    lower_green = (35, 30, 30)
    upper_green = (100, 255, 255)

    lower = np.array([0, 0, 0])
    upper = np.array([180, 255, 50])
    
    while True:
        _,frame = cap.read()
  
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        safe_mask = cv2.inRange(hsv, lower_green, upper_green)

        green = cv2.bitwise_and(frame, frame, mask = safe_mask)
        
        dan_mask = cv2.inRange(hsv, lower, upper)
        
        safe_count = len(hsv[np.where(safe_mask != 0)])
        dan_count = len(hsv[np.where(dan_mask != 0)])
        
        #print(safe_count)
        #print(dan_count)
        
        if safe_count > 15000:
           print("safe_zone")
           f = open("area.txt", 'w')
           f.write("safe")
           f.close()
           TX_data_py2(serial_port, 38)
           break
           
        elif dan_count > 15000:
           print("dangerous_zone")
           f = open("area.txt", 'w')
           f.write("dangerous")
           f.close()
           
           TX_data_py2(serial_port, 37)
           TX_data_py2(serial_port, 7)
           
           break


        
        cv2.waitKey(1)
        

    cap.release()
    cv2.destroyAllWindows()
    
    time.sleep(1)
    exit(1)