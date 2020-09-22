import cv2
import serial
import time
import sys
from threading import Thread

serial_use = 1
serial_port =  None
Read_RX =  0
receiving_exit = 1
threading_Time = 0.01
distance_count = 0
distance_exit = 1

def TX_data_py2(ser, one_byte): 

    while receiving_exit == 2:
        time.sleep(threading_Time)  
        
    ser.write(serial.to_bytes([one_byte])) 
    
    
     



def Receiving(ser):
    global receiving_exit
    global distance_count
    global X_255_point
    global Y_255_point
    global X_Size
    global Y_Size
    global Area, Angle
    
    
    while True:
        receiving_exit = 1
        time.sleep(threading_Time)
        while True:
            if receiving_exit == 0:
                break
            time.sleep(threading_Time)
            #print(receiving_exit)
            while ser.inWaiting() > 0:
                receiving_exit = 2
                result = ser.read(1)
                RX = ord(result)
                print ("RX=" + str(RX))
            
                if RX == 99:
                    result = ser.read(1)
                    RX = ord(result)
                    if RX == 99:
                        distance_count += 1
                        if distance_count > 3:
                           receiving_exit = 0
                           break
                    
                if RX == 100:
                    receiving_exit = 0
                    break


            
def get_distance():
    
    return distance_count
              
    
