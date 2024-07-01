from tkinter import *
from tkinter.ttk import *
import tkinter as tk

from serial.tools import list_ports
import serial
import os
import numpy as np

from matplotlib import animation

from Gyro import Gyro_3D
from Helper import Time_Graph
from Helper import Status
from Helper import Var
from Helper import Gps_Graph_2D
#from Helper import Gps_Graph_3D
#from Helper import graph_2D

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

### Hyper Parameter ###
### Change this parameter according to your personalization setting
update_time = 80    # Receive data & update ground station period (ms)
com = 'COM9'        # Port
Serial_rate = 9600  # Serial Rate
data_length = 15    # Number of serial data : [Transceiver, x, y, z, u, Yaw, Pitch, Roll, Altitude, Pressure, Temperature, Servo, Voltage, SD,GPS]
debug = 0           # Change this 1 to show debug print
### =============== ###      
                                                                                                                                                                                                                                                                      
# make program with tkinter
root = Tk()
root.title("THRUST-Ground Station") # set title
root.geometry("1200x800+0+0") # weight x height + x + y
root.resizable(width=False,height=False)
root.minsize(width=250, height=250) # minimum size 

root.rowconfigure(0,weight=1)
root.rowconfigure(1,weight=9)
root.rowconfigure(2,weight=1)

root.columnconfigure(1,weight=1)
#root.columnconfigure(2,weight=5)
root.columnconfigure(3,weight=4)

### Top frame ###
top_frame = tk.Frame(root, bg='gray', width = 1200, height=50)
top_frame.grid(row=0, columnspan=4, sticky='news')
#-------------#

### frame 1 ###
# Rocket Image 

#frame1 = tk.Button(root,text = "1", bg= 'red')
frame1 = tk.Frame(root, relief="solid", bd=3)
frame1.grid(row=1,column=0, sticky='news')
dirloc = os.path.dirname(__file__)
img = tk.PhotoImage(file=dirloc + "/Image/Rocket.png")

rocket_img = tk.Label(frame1,image=img)
rocket_img.pack()
#-------------#

### frame 2 ###
# Status frame
frame2 = tk.Frame(root)
frame2.grid(row=1,column=1, sticky='news')

frame2.columnconfigure(0,weight=1)

Servo_stat = Status(frame2, (0,0), 'Servo')
frame2.rowconfigure(0, weight=1)

Voltage_stat = Status(frame2, (1,0), 'Voltage')
frame2.rowconfigure(1, weight=1)

Transceiver_stat = Status(frame2, (2,0), 'Transceiver')
frame2.rowconfigure(2, weight=1)

Gyro_stat = Status(frame2, (3,0), 'Gyro')
frame2.rowconfigure(3, weight=1)

GPS_stat = Status(frame2, (4,0), 'GPS')
frame2.rowconfigure(4, weight=1)

Altitude_stat = Status(frame2, (5,0), 'Altitude')
frame2.rowconfigure(5, weight=1)

SD_stat = Status(frame2, (6,0), 'SD Card')
frame2.rowconfigure(6, weight=1)

Pressure_stat = Status(frame2, (7,0), 'Pressure')
frame2.rowconfigure(7, weight=1)
#-------------#

### frame 3 ###
# Gyro, Pressure frame
frame3 = tk.Frame(root, relief="solid",bd = 3)
frame3.grid(row=1, column=2, sticky='news')

frame3.columnconfigure(0,weight=1)
frame3.columnconfigure(1,weight=1)

# Gyro_3D 
gyro_label=Label(frame3, text="Gyro ", borderwidth=2, font = ("Arial", 15))
gyro_label.grid(row=0,column=0,sticky='w')

gyro3D = Gyro_3D(frame3)
gyro3D_canvas = FigureCanvasTkAgg(gyro3D.fig, master=frame3)
gyro3D_canvas.get_tk_widget().grid(row=1, column=0, rowspan=2, sticky='w')
gyro3D_anim = animation.FuncAnimation(gyro3D.fig, gyro3D.animate, init_func=gyro3D.init, frames=100, interval=30, blit=False)

# Quaternion
quat_var = tk.Frame(frame3)
quat_var.grid(row=1,column=1, sticky='nw')
quat_label=Label(quat_var, text=" Quaternion ", borderwidth=2, font = ("Arial", 15))
quat_label.grid(row=0,column=0,sticky='news')
x_var = Var(quat_var,(1,0),'X','blue')
y_var = Var(quat_var,(2,0),'Y','green')
z_var = Var(quat_var,(3,0),'Z','red')
w_var = Var(quat_var,(4,0),'W','black')

# Euler
YPR_var = tk.Frame(frame3)
YPR_var.grid(row=2,column=1, sticky='nw')
YPR_label=Label(YPR_var, text=" Euler ", font = ("Arial", 15))
YPR_label.grid(row=0,column=0,sticky='news')

Yaw_var = Var(YPR_var, (1,0),'Yaw','blue')
Pitch_var = Var(YPR_var, (2,0),'Pitch','green')
Roll_var = Var(YPR_var, (3,0),'Roll','red')

# Pressure
Pressure = Time_Graph(frame3, (4,0), (50,100), "black", "Pressure")
Pressure_anim = animation.FuncAnimation(Pressure.fig, Pressure.animate, init_func= Pressure.init_line ,frames=100, interval=50, blit=False)

Temp_var = Var(frame3, (6,0),'Temperature','black')
Time_var = Var(frame3, (7,0),'Time','black')
#-------------#

### frame 4 ###
# Altitude, gps
frame4 = tk.Frame(root, relief="solid",bd = 3)
frame4.grid(row=1, column=3, sticky='news')

# 2D GPS
Gps = Gps_Graph_2D(frame4, (0,0), "black", "Gps")
#Gps_anim = animation.FuncAnimation(Gps.fig, Gps.animate, frames=100, interval=50, blit=False)

# 3D GPS
#Gps = Gps_Graph_3D(frame4, (0,0), "black", "Gps")
#Gps_anim = animation.FuncAnimation(Gps.fig, Gps.animate, init_func= Gps.init_line ,frames=100, interval=50, blit=False)

Altitude = Time_Graph(frame4, (2,0), (50,100), "black", "Altitude")
Altitude_anim = animation.FuncAnimation(Altitude.fig, Altitude.animate, init_func= Altitude.init_line ,frames=100, interval=50, blit=False)
#-------------#

### Bottom frame ###
bottom_frame = tk.Frame(root, bg='gray', width = 1200, height=50, pady=3)
bottom_frame.grid(row=2, columnspan=4, sticky='news')
#-------------#

cnt = 0
test = 0
def loop():
    ### Read Data from Serial ###
    # Serial Data : String, ex) "123.0,242.2,25.3"   
    raw_data = ser.readline() 
    data = raw_data.decode('utf-8').split(',')
    # Test Data
    # data = ['0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0','0.0'] # Fake data
    # [Transceiver, x, y, z, u, Yaw, Pitch, Roll, Altitude, Pressure, Temperature, Servo, Voltage, SD,GPS]
    trans,x,y,z,u,yaw,pitch,roll,alt,p,temp,servo,volt,sd,gps = list(map(float, data))

    global cnt
    global test
    cnt = cnt + 1
    
    if (len(data) == data_length):
        ### Parser ###
        data[data_length-1] = data[data_length-1][:-2]
        quaternion = [x,y,z,u]
        
        # Update Gyro 3D graph
        gyro3D.Quat = quaternion
        
        x_var.data = quaternion[0]
        x_var.update()
        y_var.data = quaternion[1]
        y_var.update()
        z_var.data = quaternion[2]
        z_var.update()
        w_var.data = quaternion[3]
        w_var.update()
        
        Yaw_var.data = yaw
        Yaw_var.update()
        Pitch_var.data = pitch
        Pitch_var.update()
        Roll_var.data = roll
        Roll_var.update()
        
        Pressure.data = p
        Altitude.data = alt
        
        Temp_var.data = temp
        Temp_var.update()
        Time_var.data = cnt
        Time_var.update()

        if (cnt % 30 == 0):
            # Test variable 
            # use this variable to test the status!
            # Also You should remove this when you actually use it
            test = (int(test)+1)%2
            
            # Change here to gps data
            Gps.data = cnt
            Gps.update(cnt,cnt)
            
        Servo_stat.update(servo)
        Voltage_stat.update(volt)
        Transceiver_stat.update(trans)
        Gyro_stat.update(yaw)
        GPS_stat.update(gps)
        Altitude_stat.update(alt)
        SD_stat.update(sd)
        Pressure_stat.update(p)
    
    root.after(update_time,loop)

if __name__ == '__main__': # start program
    ports = list_ports.comports()
    
    if debug:
        for port in ports:
            print(port)

    ser = serial.Serial(com,Serial_rate)
    
    # Receive data and update GS in 'update_time' ms
    val = root.after(update_time,loop)
    
    while True: # Only exits, because update cannot be used on a destroyed application
        root.update()
        root.update_idletasks()
    