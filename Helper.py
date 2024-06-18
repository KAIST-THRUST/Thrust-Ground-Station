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
    
class Var:
    def __init__(self, root, location, name = 'Var', color='black'):
        (row,column) = location
        state = Label(root, text = str(name) + " : ", borderwidth=4, foreground = color, font = ("Arial", 15))
        state.grid(row=row,column=column,sticky="w")
        
        self.var = Label(root, text = "0", borderwidth=4, font = ("Arial", 15))
        self.var.grid(row=row,column=column,sticky="e")
    
    def update(self, i):
        self.var.configure(text="{:.2f}".format(self.data))
    
class Status:
    def __init__(self,  root, location, name = 'state'):
        (row,column) = location
        status_frame = tk.Frame(root, relief="solid", bd=3)
        
        txt1 = Label(status_frame, text = name, borderwidth=2, font = ("Arial", 15))
        txt1.grid(row=0,column=0, sticky="w", padx=5, pady=5)
        
        stat1 = Label(status_frame, text = "Disconnected", borderwidth=2, background = "red", font = ("Arial", 15))
        stat1.grid(row=1,column=0,sticky="w", padx=5, pady=5)
        
        status_frame.grid(row=row,column=column, sticky="news")
        
        return