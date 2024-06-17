from tkinter import *
from tkinter.ttk import *
import tkinter as tk

from threading import Thread
from serial.tools import list_ports
import serial
import numpy as np
import matplotlib.pyplot as plt
from time import ctime 
from time import time
from time import sleep

from matplotlib import animation

from Gyro import Gyro_3D
from Gyro import Gyro_graph
from Time_Graph import Time_Graph
from Helper import Status

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyquaternion import Quaternion
                                
                                                                                                                                                                                                                                                                      
# make program with tkinter
root = Tk()
root.title("THRUST-Ground Station") # set title
root.geometry("1200x800+0+0") # weight x height + x + y
root.minsize(width=250, height=250) # minimum size 

frame1=tk.Frame(root, relief="solid", bd=1)
#frame1.pack()
frame1.grid(row=0,column=0, sticky="nsw")

frame2=tk.Frame(root, relief="solid", bd=1)
#frame2.pack()
frame2.grid(row=0,column=1,sticky= "nsw")

frame3=tk.Frame(root, relief="solid", bd=1)
#frame3.pack()
frame3.grid(row=0,column=2,sticky= "nse")


gyro3D = Gyro_3D(frame1)
gyro3D_anim = animation.FuncAnimation(gyro3D.fig, gyro3D.animate, init_func=gyro3D.init, frames=100, interval=30, blit=False)

### Yaw ###
Yaw = Time_Graph(frame2, 1, (50,2*np.pi), "red", "Yaw")
Yaw_anim = animation.FuncAnimation(Yaw.fig, Yaw.animate, init_func= Yaw.init_line ,frames=100, interval=50, blit=False)

### Pitch ###
#Pitch = Gyro_graph(frame2, "Pitch")
#Pitch_anim = animation.FuncAnimation(Pitch.fig, Pitch.animate, fargs= [YPR,],init_func= Pitch.init_line ,frames=100, interval=50, blit=False)

### Roll ###
#Roll = Gyro_graph(frame2, "Roll")
#Roll_anim = animation.FuncAnimation(Roll.fig, Roll.animate, fargs= [YPR,],init_func= Roll.init_line ,frames=100, interval=50, blit=False)

### Altitude ###
Alt = Time_Graph(frame2, 3, (50,100), "blue", "Altitude")
Alt_anim = animation.FuncAnimation(Alt.fig, Alt.animate, init_func= Alt.init_line ,frames=100, interval=50, blit=False)

### Status ###
Connect_Serial = Status(frame1)

root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(3, weight=1)

cnt = 0
def loop():
    ### Read Data from Serial ###
    ### Serial Data : String, ex) "123.0,242.2,25.3"
    #raw_data = ser.readline() 
    #data = raw_data.decode('utf-8').split(',')
    # [Yaw, Pitch, Roll, ?, Altitude, ]
    data = ['0.0','0.0','0.0','0.0','0.0'] # Fake data
    global cnt
    
    global gyro3D
    global Yaw
    global Alt
    
    cnt = cnt + 1 
    data_length = 5
    if (len(data) == data_length):
        ### Parser ###
        data[data_length-1] = data[data_length-1][:-2]
        global YPR
        YPR = [float(data[0])+(cnt*0.01*np.pi),float(data[1]),float(data[2]), float(data[3])]
        gyro3D.YPR = YPR
        Yaw.data = float(data[0]) + (cnt*0.01*np.pi)
        Alt.data= float(data[4]) + cnt
        
        #Roll_anim = animation.FuncAnimation(Roll.fig, Roll.animate, fargs= [YPR,],init_func= Roll.init_line ,frames=200, interval=50, blit=False)
    
    root.after(80,loop)

if __name__ == '__main__': # start program
    """
    ports = list_ports.comports()
    for port in ports:
        print(port)

    ser = serial.Serial('COM9',9600)
    """
    val = root.after(80,loop)
    #thread = Thread(target=loop)
    #thread.start()
    
    while True: # Only exits, because update cannot be used on a destroyed application
        root.update()
        root.update_idletasks()
    