"""
Takes data from detrended_ir_data.csv and plots the estimated bpm based on peak detection.
"""
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from collections import deque

min_height = 0
min_distance = 25
WINDOW_SIZE = 300
MIN_PEAK_PROMINENCE = 500

ir_data = deque([0] * WINDOW_SIZE)

fig, ax = plt.subplots()
graph,  = ax.plot(ir_data)
peaks_plot, = ax.plot([], [], "rx", linestyle='none', label='Detected Peaks')

ax.set_title("Detrended IR Data")
ax.set_ylim(-1500, 1500)
ax.set_xlim(0, WINDOW_SIZE)

plt.ion()

with open("detrended_ir_data.csv") as file:
    while True:
        line = file.readline().strip().split(',')
        if not line:
            break
        time = float(line[0])
        irValue = float(line[1])
        ir_data.append(irValue)
        if (len(ir_data) > WINDOW_SIZE):
            ir_data.popleft()

        peak_indices, properties = find_peaks(ir_data, distance=min_distance, prominence=MIN_PEAK_PROMINENCE)
        if len(peak_indices) > 0:
            peak_amplitudes = []
            for index in peak_indices:
                peak_amplitudes.append(ir_data[index])
        else:
            peak_amplitudes = []

        if irValue == peak_indices[-1]:
            bpm = 60 / (time - last_beat_time / 1000)
            last_beat_time = time

        # update graph with new data  - ADD HERE

        plt.draw()
        plt.pause(0.001)

plt.ioff()
plt.show()