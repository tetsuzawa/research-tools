# %%
import sys

sys.path.append('./')
sys.path.append('/Users/tetsu/personal_files/Research')
sys.path.append('/Users/tetsu/personal_files/Research/research_tools')

from wave_process import WaveHandler
from plot_tools import PlotTools
# from research_tools.wave_handler import WaveHandler
# from research_tools.plot_tools import PlotTools

"""
Note that the modules (numpy, maplotlib, wave, scipy) are properly installed on your environment.

Plot wave, spectrum, save them as pdf and png at same directory.

Example:
   python calc_wave_analysis.py IR_test.wav

"""


# %%
filename = sys.argv[1]
wav = WaveHandler(filename=filename)
print("analize file name: ", filename)

# %%
graph = PlotTools(y=wav.data, fs=wav.fs, fft_N=wav.chunk_size, window="hamming")

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
