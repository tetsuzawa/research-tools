# -*- coding: utf-8 -*-
# python3.7 VS_plot.DXB.py [FILE_NAME] [FFT_LENGTH]
#
import struct
import sys
import math
import string
import numpy as np
import os.path
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import wave
from scipy import fromstring, int16, frombuffer

import wave_process
import plot_tool


def open_file(audiofile):
    fp = open(audiofile, encoding="utf-8")
    strs = fp.read()  # 全データを文字列として読み込む
    fp.close()
    return strs


def main():
    if (len(sys.argv) < 4) or (len(sys.argv) > 5):
        print("usage: python3.7 ahe.ph [XXX.DDB or .DSB or .wav] [fft_length] [sampling_freqency] ([start second])")
        sys.exit()
    elif len(sys.argv) == 5:
        start_sec = float(sys.argv[4])
    
    else:
        start_sec = 0

    audiofile = sys.argv[1]
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

    else:
        exit()

    N = int(sys.argv[2])
    fs = int(sys.argv[3])

    # 結果表示
    print("分析対象ファイル：", audiofile)
    print("解析開始秒：", start_sec)
    print("サンプル数：", N)
    print("チャンネル数：", channels)
    print("サンプリング周波数：", fs)

    plot_tool.plot_3charts(N=N, y=data, fs=fs, start_sec=start_sec)


if __name__ == '__main__':
    main()
