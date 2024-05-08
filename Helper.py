from tkinter import *
import tkinter as tk

import numpy as np

class Status:
    def __init__(self, root):
        status_frame = tk.Frame(root, relief="solid", bd=1)
        
        txt1 = Label(status_frame, text = "state 1 : ", borderwidth=4, font = ("Arial", 15))
        txt1.grid(row=0,column=0,sticky="e")
        
        stat1 = Label(status_frame, text = "Disconnected", borderwidth=4, background = "red", font = ("Arial", 15))
        stat1.grid(row=0,column=1,sticky="nswe")
        
        txt2 = Label(status_frame, text = "state 2 : ", borderwidth=4, font = ("Arial", 15))
        txt2.grid(row=1,column=0,sticky="e")
        
        stat2 = Label(status_frame, text = "Disconnected", borderwidth=4, background = "red", font = ("Arial", 15))
        stat2.grid(row=1,column=1,sticky="nswe")
        
        status_frame.grid(row=1,column=0, sticky="nswe")
        
        return