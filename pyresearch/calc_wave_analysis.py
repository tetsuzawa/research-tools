# %%
import sys

import numpy as np

sys.path.append('./')
sys.path.append('/Users/tetsu/personal_files/Research')
sys.path.append('/Users/tetsu/personal_files/Research/research_tools')

from wave_handler_multi_ch import WaveHandler
# from wave_process import WaveHandler
from plot_tools import PlotTools

# from research_tools.wave_handler import WaveHandler
# from research_tools.plot_tools import PlotTools

"""
Note that the modules (numpy, maplotlib, wave, scipy) are properly installed on your environment.

Plot wave, spectrum, save them as pdf and png at same directory.

Example:
   python calc_wave_analysis.py IR_test.wav

"""


def get_nearest_value(target_list, v):
    if 1 > len(target_list):
        return -1

    idx = 0
    minv = abs(target_list[0] - v)
    for i in range(len(target_list)):
        if abs(target_list[i] - v) < minv:
            idx = i
            minv = abs(target_list[i] - v)
    return idx


def main():
    # %%
    filename = sys.argv[1]
    wav = WaveHandler(filename=filename)
    print("analize file name: ", filename)

    two_powers = [int(2 ** i) for i in range(30)]
    idx = get_nearest_value(two_powers, wav.chunk_size)
    ###########
    # if two_powers[idx] > wav.chunk_size:
    #     data = np.concatenate([wav.data, np.zeros(two_powers[idx] - len(wav.data))])
    if two_powers[idx] > wav.chunk_size:
        idx -= 1
    ###########

    # %%
    graph = PlotTools(y=wav.data[:two_powers[idx]], fs=wav.fs, fft_N=two_powers[idx], window="hamming")
    # graph = PlotTools(y=wav.data, fs=wav.fs, fft_N=len(wav.data), window="hamming")

    # %%
    # graph.plot_all()

    # %%

    graph.plot_y_sample()
    # graph.plot_y_gain_time()
    # graph.plot_freq_analysis()
    # graph.plot_freq_analysis_log()
    # graph.plot_power_gain_spectrum()
    # graph.plot_acf()
    graph.plot_spectrogram_acf()


# %%
if __name__ == '__main__':
    main()
