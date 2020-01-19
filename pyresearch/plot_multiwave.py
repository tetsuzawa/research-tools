#!/usr/bin/env python
# coding: utf-8

# Usage:
#   python3 plot_multiwave.py foo.wav
# then you can see the wave's abstruct

import signal
import sys
import wave

import matplotlib.pyplot as plt
import numpy as np

signal.signal(signal.SIGINT, signal.SIG_DFL)

plt.rcParams['font.family'] = 'IPAPGothic'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.figsize'] = (8, 7)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.subplot.hspace'] = 0.3
plt.rcParams['figure.subplot.wspace'] = 0.3


def main():
    args = sys.argv

    if len(args) < 2:
        print("error : please pass the wave file argument")
        print("Usage: python3 plot_muiltiwave.py foo.wav")
        sys.exit()

    for i in range(len(args) - 1):
        wf = wave.open(args[i + 1], "r")
        buf = wf.readframes(wf.getnframes())
        wf.close()

        f = np.frombuffer(buf, dtype="int16")

        plt.plot(f, alpha=0.5, label=args[i + 1])
        plt.legend()
        plt.grid(True)

    plt.show()


if __name__ == '__main__':
    main()
