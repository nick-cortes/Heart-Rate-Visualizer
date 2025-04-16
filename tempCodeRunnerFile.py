peak_indices, properties = find_peaks(ir_data, distance=min_distance, prominence=MIN_PEAK_PROMINENCE)

        peak_times = []
        for index in peak_indices:
            peak_times.append(times_deque[index])
        peak_amplitudes = []
        for index in peak_indices:
                peak_amplitudes.append(ir_data[index])