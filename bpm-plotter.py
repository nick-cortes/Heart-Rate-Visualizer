"""
Take in live IR data, identifies heart beats, and then plots BPM over time.
This uses much of the same logic as live-ir-writer.py and ir-peak-plotter.py.
"""
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from collections import deque
import serial
import time

min_distance = 25
WINDOW_SIZE = 200
MIN_PEAK_PROMINENCE = 325
UPDATE_INTERVAL = 0.05
BEATS_TO_AVERAGE = 8

ser = serial.Serial('COM3', 115200)

ir_data = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
times_deque = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
bpm_deque = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
bpm_times = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
calculated_bpm_values = deque([0] * BEATS_TO_AVERAGE, maxlen=BEATS_TO_AVERAGE)

fig, ax = plt.subplots()
graph,  = ax.plot(times_deque, ir_data)
peaks_plot, = ax.plot([], [], "rx", linestyle='none', label='Detected Peaks')

ax.set_title("Live Detrended IR Data")
ax.set_xlabel("Time")
ax.set_ylabel("BPM")
ax.set_ylim(60, 130)

plt.draw()
plt.pause(0.0001)

last_update_time = time.time()
last_peak = 0
beat_count = 0

plt.ion()

while True:
    data = ser.readline().decode('utf-8').strip().split(",")
    irTime = float(data[0]);
    irValue = float(data[1]);
    ir_data.append(irValue);
    times_deque.append(irTime)
    
    peak_indices, properties = find_peaks(ir_data, distance=min_distance, prominence=MIN_PEAK_PROMINENCE)

    peak_times = []
    for index in peak_indices:
        peak_times.append(times_deque[index])
    
    if len(peak_indices) > 0:
        most_recent_peak = times_deque[peak_indices[-1]]
        if most_recent_peak != last_peak:
            # we have a beat!
            delta = most_recent_peak - last_peak 
            bpm = 60 / (delta / 1000)
            calculated_bpm_values.append(bpm)
            last_peak = most_recent_peak
            beat_count += 1
            print(f"Beat detected! {beat_count}")
    
    average_bpm = 0.0
    if len(calculated_bpm_values) > 0:
        average_bpm = sum(calculated_bpm_values) / len(calculated_bpm_values)
    bpm_deque.append(average_bpm)
    bpm_times.append(irTime)

    curr_time = time.time()

    if curr_time - last_update_time > UPDATE_INTERVAL:
        
        graph.set_data(bpm_times, bpm_deque)
        ax.set_xlim(times_deque[0], times_deque[-1])

        last_update_time = curr_time
        plt.draw()
        plt.pause(0.0001)
    
    fig.canvas.flush_events()