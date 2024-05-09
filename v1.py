### This code is just for testing ###

from serial.tools import list_ports
import serial
import time

ports = list_ports.comports()
for port in ports:
    print(port)

ser = serial.Serial('COM9',9600)

#ser.open()

data = []

while True:

    data1 = ser.readline() 
    #data2 = data1.split(b'\\') 
    #data.append(data)
    #data = data1.decode('utf-8')
    print(data1)
    
    if len(data) > 1000:
        break
    
ser.close()