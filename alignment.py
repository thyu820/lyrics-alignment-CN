import numpy as np
from fuzzywuzzy import fuzz

def dtw_alignment(asr_segments, lyrics):
    def calculate_distance(s1, s2):
        return 100 - fuzz.ratio(s1, s2)

    n, m = len(asr_segments), len(lyrics)
    dtw_matrix = np.zeros((n + 1, m + 1))
    dtw_matrix[0, 1:] = np.inf
    dtw_matrix[1:, 0] = np.inf

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = calculate_distance(asr_segments[i-1]['text'], lyrics[j-1])
            dtw_matrix[i, j] = cost + min(dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1])

    alignment = []
    i, j = n, m
    while i > 0 and j > 0:
        alignment.append((i-1, j-1))
        if i == 1:
            j -= 1
        elif j == 1:
            i -= 1
        else:
            min_value = min(dtw_matrix[i-1, j], dtw_matrix[i, j-1], dtw_matrix[i-1, j-1])
            if min_value == dtw_matrix[i-1, j-1]:
                i -= 1
                j -= 1
            elif min_value == dtw_matrix[i-1, j]:
                i -= 1
            else:
                j -= 1

    alignment.reverse()
    return alignment