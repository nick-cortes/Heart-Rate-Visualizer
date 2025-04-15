import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np

ir_data = []
with open("detrended_ir_data.csv") as file:
    for line in file:
        data = file.readline().strip()
        data = float(data)
        ir_data.append(data)
ir_data_np = np.array(ir_data)

min_height = 0
min_distance = 25
peak_indices, properties = find_peaks(ir_data_np, distance=min_distance)

peak_amplitudes = ir_data_np[peak_indices]

WINDOW_SIZE = len(ir_data)

fig, ax = plt.subplots()
ax.plot(ir_data)
ax.plot(peak_indices, peak_amplitudes, "rx", linestyle='none', label='Detected Peaks')

ax.set_title("Detrended IR Data")
ax.set_ylim(-1500, 1500)
ax.set_xlim(0, WINDOW_SIZE)

plt.show()