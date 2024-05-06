from tkinter import *

import numpy as np
import matplotlib.pyplot as plt

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
        
        data[0] += 0.01*np.pi
        data[1] = 0 #0.01*np.pi #np.random.uniform(0,2)*np.pi
        data[2] = np.pi#np.random.uniform(0,2)*np.pi
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
    
class Gyro_graph:
    def __init__(self, master, mode):
        self.mode = mode
        
        if self.mode == "Yaw":
            row = 1
            self.num = 0
            color = "blue"
        elif self.mode == "Pitch":
            row = 3
            self.num = 1
            color = "green"
        elif self.mode == "Roll":
            row = 5
            self.num=2
            color = "red"
            
        state = Label(master, text = str(mode) + " : ", borderwidth=4, foreground =color, font = ("Arial", 15))
        state.grid(row=row,column=0,sticky="w")
        
        self.var = Label(master, text = "0", borderwidth=4, font = ("Arial", 15))
        self.var.grid(row=row,column=0,sticky="e")

        self.fig = plt.figure(figsize=(3,2))
        ax = plt.subplot(111, xlim=(0, 50), ylim=(0, 2*np.pi))
        self.line, = ax.plot(np.arange(50), np.ones(50, dtype=np.float)*np.nan, lw=1, c=color,ms=1)

        canvas = FigureCanvasTkAgg(self.fig, master=master)
        canvas.get_tk_widget().grid(row=row+1, column=0)
    
    def init_line(self):
        return self.line
        
    def animate(self,i,data):
        y = data[self.num]
        self.var.configure(text=data[self.num])
        
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        self.line.set_ydata(new_y)
        return self.line,
    