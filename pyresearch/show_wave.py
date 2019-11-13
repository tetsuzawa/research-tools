# -*- coding: utf-8 -*-

# use like this : python show_wave.py test.wav
# then you can see the wave's abstruct

import sys
import wave

import numpy as np
import matplotlib.pyplot as plt


def main():
    args = sys.argv

    # wf = wave.open("test.wav" , "r" )
    if len(args) < 2:
        print("error : please pass the wave file argument")
        print("use like this : python show_wave.py test.wav")
        sys.exit()

    wf = wave.open(args[1], "r")
    buf = wf.readframes(wf.getnframes())

    # バイナリデータを整数型（16bit）に変換
    f = np.frombuffer(buf, dtype="int16")
    F = np.fft.fft(f)

    # FFTの複素数結果を絶対に変換
    F_abs = np.abs(F)
    # 振幅をもとの信号に揃える
    # F_abs_amp = F_abs / N * 2 # 交流成分はデータ数で割って2倍
    # F_abs_amp[0] = F_abs_amp[0] / 2 # 直流成分（今回は扱わないけど）は2倍不要

    fig, (axf, axF) = plt.subplots(ncols=2)

    # グラフ化
    axf.plot(f)
    axF.plot(F_abs)
    axf.grid()
    axF.grid()
    plt.show()


if __name__ == '__main__':
    main()
