import serial
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import time
import json 
import pyautogui
import keyboard

pyautogui.PAUSE = 0.001 
arduino = serial.Serial('/dev/ttyACM0')  # open serial port

def read_serial():
    data = arduino.readline()
    return data

def plot_figure(x, y, z):
    pass

while True:
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
        print('You Pressed A Key!')
        break
    try:
        values = json.loads(read_serial().decode().strip())
    except:
        values = {"x": "0", "y": "0", "z": "0"}
    print(values)
    pyautogui.moveRel(int(float(values["y"])), int(float(values["x"])))
