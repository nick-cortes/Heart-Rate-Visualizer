import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from collections import deque
import serial
import time

min_distance = 25
WINDOW_SIZE = 300
MIN_PEAK_PROMINENCE = 275
UPDATE_INTERVAL = 0.05

ser = serial.Serial('COM3', 115200)
ir_data = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
times_deque = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)

fig, ax = plt.subplots()
graph,  = ax.plot(times_deque, ir_data)
peaks_plot, = ax.plot([], [], "rx", linestyle='none', label='Detected Peaks')

ax.set_title("Live Detrended IR Data")
ax.set_xlabel("Time")
ax.set_ylabel("IR Value")
ax.set_ylim(-1500, 1500)

plt.draw()
plt.pause(0.0001)

last_update_time = time.time()

plt.ion()

while True:
    data = ser.readline().decode('utf-8').strip().split(",")
    irTime = float(data[0]);
    irValue = float(data[1]);
    ir_data.append(irValue);
    times_deque.append(irTime)
    
    curr_time = time.time()
    if curr_time - last_update_time > UPDATE_INTERVAL:
        peak_indices, properties = find_peaks(ir_data, distance=min_distance, prominence=MIN_PEAK_PROMINENCE)

        peak_times = []
        for index in peak_indices:
            peak_times.append(times_deque[index])
        peak_amplitudes = []
        for index in peak_indices:
                peak_amplitudes.append(ir_data[index])
        
        peaks_plot.set_data(peak_times, peak_amplitudes) # update heart beat indicators
        graph.set_data(times_deque, ir_data) # update IR values and times
        ax.set_xlim(times_deque[0], times_deque[-1])

        last_update_time = curr_time
        plt.draw()
        plt.pause(0.0001)
    
    fig.canvas.flush_events()