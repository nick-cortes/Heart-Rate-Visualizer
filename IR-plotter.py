import serial
import matplotlib.pyplot as plt
from collections import deque

ser = serial.Serial('COM3', 9600)  # need to update this when max30102 comes in

window_size = 100  # Number of data points to show
IR_data = deque([0]*window_size)

fig, ax = plt.subplots()
graph = ax.plot()
ax.set_title("Heart Rate Data")
ax.set_xlabel("time")
ax.set_ylabel("IR")

plt.ion()

while True:
    new_data = ser.readline()
    IR_data.append(new_data)
    if len(IR_data) > window_size: 
        IR_data.popleft()
    plt.draw()
    plt.pause(0.01)