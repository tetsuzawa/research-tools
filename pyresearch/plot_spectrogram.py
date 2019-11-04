import struct
import sys
import os.path
import pandas as pd
import matplotlib.pyplot as plt
import wave
from scipy import fromstring, int16, frombuffer

# self made module
import wave_process
import plot_tool


def main():
    if len(sys.argv) != 4:
        print("usage: python3.7 ahe.ph [XXX.DDB or .DSB or .wav] [fft_length] [sampling_freqency]")
        sys.exit()

    audiofile = sys.argv[1]
    N = int(sys.argv[2])
    fs = int(sys.argv[3])
    name, ext = os.path.splitext(audiofile)
    channels = 1

    if ext == ".DDB":
        strs = open_file(audiofile)
        data = np.fromstring(strs, dtype=np.float64)  # 2バイトの整数とし文字列を読み込む
    elif ext == ".DSB":
        strs = open_file(audiofile)
        data = np.fromstring(strs, dtype=np.int16)
    elif ext == ".wav":
        audiodata = wave_process.wave_proccess(audiofile)
        data = audiodata.data
        channels = audiodata.ch

    plot_tool.spectrogram(N=N, y=data, fs=fs, window_func_name="hamming")


if __name__ == '__main__':
    main()
