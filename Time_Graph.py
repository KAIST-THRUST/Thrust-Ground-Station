from tkinter import *

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Time_Graph:
    def __init__(self, master, row, limit, color, mode=False):
        self.mode = mode
        self.data = 0
        self.row = row
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
    