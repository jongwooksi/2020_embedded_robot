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
distance_count_25 = 0

def TX_data_py2(ser, one_byte): 

    ser.write(serial.to_bytes([one_byte])) 
    Receiving(ser)
    

def RX_data(ser):

    if ser.inWaiting() > 0:
        result = ser.read(1)
        RX = ord(result)
        return RX
    else:
        return 0
 

def Receiving(ser):
    global receiving_exit

    global X_255_point
    global Y_255_point
    global X_Size
    global Y_Size
    global Area, Angle
    global distance_count
    
    receiving_exit = 1
    
    while True:
        if receiving_exit == 0:
            break
        time.sleep(threading_Time)
        while ser.inWaiting() > 0:
            result = ser.read(1)
            RX = ord(result)
            print ("RX=" + str(RX))
            
        
            if RX == 50:
                receiving_exit = 0
                break
   
                
            if RX == 99:
                if distance_count < 3:
                    distance_count += 1
                    print(distance_count)
            
def get_distance():
    return distance_count
