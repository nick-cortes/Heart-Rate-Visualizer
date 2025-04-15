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

ax.set_ylim(-300, 300)
ax.set_xlim(0, window_size)

plt.ion()

while True:
    line = ser.readline().decode('utf-8').strip().split(',')
    if not line:
        continue
    # ir, bpm = float(line[0]), float(line[1])
    bpm = float(line[0]);
    new_data = float(bpm) # new BPM value
    BPM_data.append(new_data)
    if len(BPM_data) > window_size: 
        BPM_data.popleft()
    graph.set_ydata(BPM_data)
    plt.draw()
    plt.pause(0.01)