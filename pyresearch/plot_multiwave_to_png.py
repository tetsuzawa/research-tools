#!/usr/bin/env python
# coding: utf-8

# Usage:
#   python3 plot_multiwave.py foo.wav
# then you can see the wave's abstruct

import pathlib
import signal
import sys

# matplotlib.use("Agg")
import matplotlib.pyplot as plt
import soundfile as sf

# import matplotlib

signal.signal(signal.SIGINT, signal.SIG_DFL)

plt.rcParams['font.family'] = 'IPAPGothic'
plt.rcParams['font.size'] = 16
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
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
        input_path = args[i + 1]
        data, sr = sf.read(input_path)

        input_path = pathlib.Path(input_path)

        plt.plot(data, alpha=0.5, label=input_path.stem)
        plt.xlabel("Sample")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.tight_layout()
        plt.grid()

    output_name = input_path.with_suffix(".png")
    output_path = output_name.name
    plt.savefig(output_path)
    plt.show()
    print("\n plot is saved at: ", output_path, "\n")


if __name__ == '__main__':
    main()
