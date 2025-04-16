"""
Takes in live IR data from the MAX30102 and writes it to detrended_ir_data.csv.
Mainly used to have a consistent graph with which to tune peak detection.
"""
import serial
import matplotlib.pyplot as plt
from collections import deque

ser = serial.Serial('COM3', 115200)  # FIX THIS VALUE when max30102 comes in

window_size = 100  # Number of data points to show
BPM_data = deque([0]*window_size)

fig, ax = plt.subplots()
graph,  = ax.plot(BPM_data)

ax.set_title("Heart Rate Data")
ax.set_xlabel("time")
ax.set_ylabel("BPM")

ax.set_ylim(-700, 700)
ax.set_xlim(0, window_size)

plt.ion()

with open("detrended_ir_data.csv", "w") as file:

    while True:
        line = ser.readline().decode('utf-8').strip().split(',')
        if not line:
            continue

        ir = float(line[0]);
        new_data = float(ir) # new IR value
        file.write(f"{new_data}\n")
        file.flush()

        BPM_data.append(new_data)
        if len(BPM_data) > window_size: 
            BPM_data.popleft()
        graph.set_ydata(BPM_data)
        plt.draw()
        plt.pause(0.0001)