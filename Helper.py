from tkinter import *
import tkinter as tk

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyquaternion import Quaternion

class graph_2D:
    def __init__(self, master, mode):
        self.mode = mode
        self.data = 0
        if self.mode == "Yaw":
            row = 1
            color = "blue"
        elif self.mode == "Pitch":
            row = 3
            color = "green"
        elif self.mode == "Roll":
            row = 5
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
        
    def animate(self,i):
        y = self.data
        self.var.configure(text="{:.2f}".format(self.data))
        
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        self.line.set_ydata(new_y)
        return self.line,

class Gps_Graph_2D:
    def __init__(self, master, location, color, mode=False):
        self.mode = mode
        self.data = 0
        (row,column) = location
        self.color = color
            
        state = Label(master, text = str(mode) + " : ", borderwidth=4, foreground =color, font = ("Arial", 15))
        state.grid(row=row,column=0,sticky="w")
    
        self.var = Label(master, text = "0", borderwidth=4, font = ("Arial", 15))
        self.var.grid(row=row,column=0,sticky="e")

        self.fig = plt.figure(figsize=(3,3))

        self.ax = plt.subplot(111, xlim=(-100, 100), ylim=(-100, 100))
        #self.sc = self.ax.scatter(0,0)
        #self.line, = self.ax.plot(np.arange(50), np.ones(50, dtype=np.float)*np.nan, lw=1, c=color,ms=1)

        canvas = FigureCanvasTkAgg(self.fig, master=master)
        canvas.get_tk_widget().grid(row=row+1, column=0)
        
    def update(self,x,y):
        self.var.configure(text="{:.2f}".format(self.data))
        #self.sc.set_offsets(np.c_[[x],[y]])
        self.ax.scatter(x,y,marker='o',color='0')
        self.fig.canvas.draw_idle()
        #self.ax.clf()
        return

class Gps_Graph_3D:
    def __init__(self, master, location, color, mode=False):
        self.mode = mode
        self.data = 0
        (row,column) = location
        self.color = color
            
        state = Label(master, text = str(mode) + " : ", borderwidth=4, foreground =color, font = ("Arial", 15))
        state.grid(row=row,column=0,sticky="w")
    
        self.var = Label(master, text = "0", borderwidth=4, font = ("Arial", 15))
        self.var.grid(row=row,column=0,sticky="e")

        self.fig = plt.figure(figsize=(3,3))

        #self.ax = plt.subplot(111, xlim=(0, xlimit), ylim=(0, ylimit))
        self.ax = self.fig.add_axes([0, 0, 1, 1], projection='3d')
        self.ax.set_xlim((-50, 50))
        self.ax.set_ylim((-50, 50))
        self.ax.set_zlim((0, 200))
        self.ax.view_init(20, 45)
        
        self.line, = self.ax.plot(np.arange(50), np.ones(50, dtype=np.float)*np.nan, lw=1, c=color,ms=1)

        canvas = FigureCanvasTkAgg(self.fig, master=master)
        canvas.get_tk_widget().grid(row=row+1, column=0)
    
    def init_line(self):
        return self.line
        
    def animate(self,i):
        y = self.data
        self.var.configure(text="{:.2f}".format(self.data))
        
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        self.line.set_ydata(new_y)
        return self.line,

class Time_Graph:
    def __init__(self, master, location, limit, color, mode=False):
        self.mode = mode
        self.data = 0
        (row,column) = location
        self.color = color
            
        state = Label(master, text = str(mode) + " : ", borderwidth=4, foreground =color, font = ("Arial", 15))
        state.grid(row=row,column=0,sticky="w")
        
        self.var = Label(master, text = "0", borderwidth=4, font = ("Arial", 15))
        self.var.grid(row=row,column=0,sticky="e")

        self.fig = plt.figure(figsize=(3,2))
        
        (xlimit, ylimit) = limit
        self.ax = plt.subplot(111, xlim=(0, xlimit), ylim=(0, ylimit))
        self.line, = self.ax.plot(np.arange(50), np.ones(50, dtype=np.float)*np.nan, lw=1, c=color,ms=1)

        canvas = FigureCanvasTkAgg(self.fig, master=master)
        canvas.get_tk_widget().grid(row=row+1, column=0)
    
    def init_line(self):
        return self.line
        
    def animate(self,i):
        y = self.data
        self.var.configure(text="{:.2f}".format(self.data))
        
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        self.line.set_ydata(new_y)
        return self.line,

class Var:
    def __init__(self, root, location, name = 'Var', color='black'):
        (row,column) = location
        val_frame = tk.Frame(root)
        
        self.data = 0.00
        
        state = Label(val_frame, text = str(name) + " : ", borderwidth=4, foreground = color, font = ("Arial", 15))
        state.grid(row=0,column=0,sticky="w")
        
        self.var = Label(val_frame, text = self.data, borderwidth=4, foreground = color, font = ("Arial", 15))
        self.var.grid(row=0,column=1,sticky="e")
        
        val_frame.grid(row=row,column=column, sticky="news")
        
        val_frame.columnconfigure(0,weight=1)
        val_frame.columnconfigure(1,weight=1)
    
    def update(self):
        self.var.configure(text="{:.2f}".format(self.data))
    
class Status:
    def __init__(self,  root, location, name = 'state'):
        (row,column) = location
        self.name = name
        self.prev_state = 0
        self.status_frame = tk.Frame(root, relief="solid", bd=3)
        
        self.txt1 = Label(self.status_frame, text = self.name, borderwidth=2, font = ("Arial", 15))
        self.txt1.grid(row=0,column=0, sticky="w", padx=5, pady=5)
        
        self.stat1 = Label(self.status_frame, text = "Disconnected", borderwidth=2, background = "red", font = ("Arial", 15))
        self.stat1.grid(row=1,column=0,sticky="w", padx=5, pady=5)
        
        self.status_frame.grid(row=row,column=column, sticky="news")
        
        return
    
    def connect(self):
        self.stat1.config(text="  Connected  ", background = "green")
        
    def disconnect(self):
        self.stat1.config(text="Disconnected", background = "red")
        
    def update(self, state):
        # Update state only the state change occurs
        # Connected : state = non-zero real number 
        # Disconnected : state = 0 
        
        if (self.prev_state != state):
            if (state != 0):
                self.connect()
            else:
                self.disconnect()
            self.prev_state = state
            
class Button:
    def __init__(self,root, location, serial):
        self.serial = serial
        (row,column) = location
        Launch_button = tk.Button(root, text='Launch', relief='solid',bg = 'red', fg='white', font = ("Arial", 15),command=self.click)
        Launch_button.grid(row=row, column=column, sticky='news')
    
    def click(self):
        self.serial.write("1")