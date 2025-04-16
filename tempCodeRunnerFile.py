peak_indices, properties = find_peaks(ir_data_np, distance=min_distance)

peak_amplitudes = ir_data_np[peak_indices]