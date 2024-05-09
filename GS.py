from tkinter import *
from tkinter.ttk import *
import tkinter as tk

from threading import Thread
from serial.tools import list_ports
import serial
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

from matplotlib import animation

from Gyro import Gyro_graph
from Helper import Status

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyquaternion import Quaternion

class Gyro_3D:
    def __init__(self, master):
        
        # Set up figure & 3D axis for animation
        self.fig = plt.figure(figsize=(4,4))
        ax = self.fig.add_axes([0, 0, 1, 1], projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #ax.axis('off')

        # use a different color for each axis
        colors = ['r', 'g', 'b']
        # set up lines and points
        self.lines = sum([ax.plot([], [], [], c=c)
                    for c in colors], [])

        self.startpoints = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.endpoints = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        # prepare the axes limits
        ax.set_xlim((-1, 1))
        ax.set_ylim((-1, 1))
        ax.set_zlim((-1, 1))

        # set point-of-view: specified by (altitude degrees, azimuth degrees)
        ax.view_init(20, 45)

        canvas = FigureCanvasTkAgg(self.fig, master=master)
        canvas.get_tk_widget().grid(row=0, column=0)

        return
    
    def init(self):
        for line in self.lines:
            line.set_data(np.array([]), np.array([]))
            line.set_3d_properties([])

        return self.lines
    
    ### Random Quaternion Function ###
    def generate_quaternion(self):
        q1 = Quaternion.random()
        q2 = Quaternion.random()
        while True:
            for q in Quaternion.intermediates(q1, q2, 20, include_endpoints=True):
                yield q
            #q1, q2 = q2, q1
            q1 = q2
            q2 = Quaternion.random()
            
    ### Radian euler => quaternion ###
    def get_quaternion_from_euler(self, roll, pitch, yaw):
        """
        Convert an Euler angle to a quaternion.
        
        Input
            :param roll: The roll (rotation around x-axis) angle in radians.
            :param pitch: The pitch (rotation around y-axis) angle in radians.
            :param yaw: The yaw (rotation around z-axis) angle in radians.
        
        Output
            :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
        """
        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        
        return [qx, qy, qz, qw]
    
    ### animation function ###
    def animate(self, i,data):
        # we'll step two time-steps per frame.  This leads to nice results.
        #i = (2 * i) % x_t.shape[1]
        
        #q = next(quaternion_generator)
        
        #q = Quaternion(axis=[0.0,0.0,1.0], radians=0.1*data[0]*np.pi)
        
        print("here : :: ", YPR)
        #data[0] += 0.01*np.pi
        #data[1] = 0 #0.01*np.pi #np.random.uniform(0,2)*np.pi
        #data[2] = np.pi#np.random.uniform(0,2)*np.pi
        data[0] = YPR[0]
        data[1] = YPR[1]
        data[2] = YPR[2]
        q = Quaternion(array=self.get_quaternion_from_euler(data[0],data[1],data[2]))
        
        
        #data[0]+=1
        #q = Quaternion(array=get_quaternion_from_euler(data[0],data[1],data[2]))
        
        for line, start, end in zip(self.lines, self.startpoints, self.endpoints):
            #end *= 5
            #print(start,end)
            start = q.rotate(start)
            end = q.rotate(end)
            #print(start,end)
            line.set_data(np.array([start[0], end[0]]), np.array([start[1], end[1]]))
            line.set_3d_properties([start[2], end[2]])

            #pt.set_data(x[-1:], y[-1:])
            #pt.set_3d_properties(z[-1:])

        #ax.view_init(30, 0.6 * i)
        #fig.canvas.draw()
        return self.lines
                             
ports = list_ports.comports()
for port in ports:
    print(port)

ser = serial.Serial('COM9',9600)
YPR = [0,0,0] # Yaw, Pitch, Roll data                                                                                                                                                                                                                                                                             
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
    data = data1.decode('utf-8').split(',')
    if (len(data) == 3):
        data[2] = data[2][:-2]
        global YPR
        YPR = [float(data[0]),float(data[1]),float(data[2])]
        #print(YPR)
        #Roll_anim = animation.FuncAnimation(Roll.fig, Roll.animate, fargs= [YPR,],init_func= Roll.init_line ,frames=200, interval=50, blit=False)
        
    root.after(100,loop)

if __name__ == '__main__': # start program
    val = root.after(100,loop)
    #thread = Thread(target=loop)
    #thread.start()
    #print(YPR)
    while True: # Only exits, because update cannot be used on a destroyed application
       
        root.update()
        root.update_idletasks()
        #print("ahh: ", YPR)
    