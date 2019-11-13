#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Usage:
#   python3 plot_multiwave.py foo.wav
# then you can see the wave's abstruct

import sys
import wave

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (8, 7)
plt.rcParams['figure.dpi'] = 100  # dpiの設定


def main():
    args = sys.argv

    if len(args) < 2:
        print("error : please pass the wave file argument")
        print("Usage: python3 plot_muiltiwave.py foo.wav")
        sys.exit()

    for i in range(len(args) - 1):
        wf = wave.open(args[i + 1], "r")
        buf = wf.readframes(wf.getnframes())

        f = np.frombuffer(buf, dtype="int16")
        # F = np.fft.fft(f)
        #
        # F_abs = np.abs(F)
        # N = len(F_abs)
        # F_abs_amp = F_abs / N * 2
        # F_abs_amp[0] = F_abs_amp[0] / 2
        #
        # fig, (axf, axF) = plt.subplots(ncols=2)
        #
        # axf.plot(f)
        # axF.set_xscale("log")
        # axF.plot(F_abs_amp[:int(len(F_abs_amp / 2))])
        # axf.grid()
        # axF.grid()

        plt.plot(f, label=args[i + 1])
        plt.legend()
        plt.grid(True)

    plt.show()


if __name__ == '__main__':
    main()
