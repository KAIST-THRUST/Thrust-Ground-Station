from tkinter import *
from tkinter.ttk import *
import tkinter as tk

from threading import Thread
from serial.tools import list_ports
import serial
from time import sleep

from matplotlib import animation

from Gyro import Gyro_graph, Gyro_3D
from Helper import Status
                             
ports = list_ports.comports()
for port in ports:
    print(port)

ser = serial.Serial('COM9',9600)
                                                                                                                                                                                                                                                                                       
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


YPR = [0,0,0] # Yaw, Pitch, Roll data
gyro3D = Gyro_3D(frame1)
gyro3D_anim = animation.FuncAnimation(gyro3D.fig, gyro3D.animate, fargs=[YPR,], init_func=gyro3D.init, frames=500, interval=30, blit=False)

### Yaw ###
Yaw = Gyro_graph(frame2, "Yaw")
Yaw_anim = animation.FuncAnimation(Yaw.fig, Yaw.animate, fargs= [YPR,],init_func= Yaw.init_line ,frames=200, interval=50, blit=False)

### Pitch ###
Pitch = Gyro_graph(frame2, "Pitch")
Pitch_anim = animation.FuncAnimation(Pitch.fig, Pitch.animate, fargs= [YPR,],init_func= Pitch.init_line ,frames=200, interval=50, blit=False)

### Roll ###
Roll = Gyro_graph(frame2, "Roll")
Roll_anim = animation.FuncAnimation(Roll.fig, Roll.animate, fargs= [YPR,],init_func= Roll.init_line ,frames=200, interval=50, blit=False)

### Status ###
Connect_Serial = Status(frame1)

root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(3, weight=1)

def loop():
    #while True:
    data1 = ser.readline() 
    #data2 = data1.split(b'\\') 
    #data.append(data)
    data = data1.decode('utf-8')
    print(data)
        #YPR = [0,0,0]
    root.after(100,loop)

if __name__ == '__main__': # start program
    root.after(100,loop)
    #thread = Thread(target=loop)
    #thread.start()
    root.mainloop() 
    
    