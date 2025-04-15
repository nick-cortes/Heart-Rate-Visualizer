import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from collections import deque
import serial
import time

min_height = 0
min_distance = 25
WINDOW_SIZE = 300
MIN_PEAK_PROMINENCE = 375
UPDATE_INTERVAL = 0.05

ser = serial.Serial('COM3', 115200)
ir_data = deque([0] * WINDOW_SIZE)

fig, ax = plt.subplots()
graph,  = ax.plot(ir_data)
peaks_plot, = ax.plot([], [], "rx", linestyle='none', label='Detected Peaks')

ax.set_title("Detrended IR Data")
ax.set_ylim(-1500, 1500)
ax.set_xlim(0, WINDOW_SIZE)

plt.draw()
plt.pause(0.0001)

last_update_time = time.time()

plt.ion()

while True:
    data = ser.readline().strip()
    if not data:
        break
    data = float(data)
    ir_data.append(data)
    if (len(ir_data) > WINDOW_SIZE):
        ir_data.popleft()

    peak_indices, properties = find_peaks(ir_data, distance=min_distance, prominence=MIN_PEAK_PROMINENCE)
    if len(peak_indices) > 0:
        peak_amplitudes = []
        for index in peak_indices:
            peak_amplitudes.append(ir_data[index])
    else:
        peak_amplitudes = []
    
    curr_time = time.time()
    if curr_time - last_update_time > UPDATE_INTERVAL:
        graph.set_ydata(ir_data)
        peaks_plot.set_data(peak_indices, peak_amplitudes)

        last_update_time = curr_time
        plt.draw()
        plt.pause(0.0001)

plt.ioff()
plt.show()