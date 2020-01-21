#!/usr/bin/env python
# encoding: utf-8

import argparse
import pathlib

import librosa
import librosa.display
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    description = "This script plots spectrogram from csv or wav file."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('input_path',
                        action='store',
                        type=str,
                        help='Directory path where the input file is located.',
                        metavar=None)

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        const="/tmp",
                        default=".",
                        type=str,
                        help='Directory path where you want to locate img files. (default: current directory)',
                        metavar=None)

    parser.add_argument('-l', '--log',
                        action='store_true',
                        help='Use y-axis logarithmic display.')

    args = parser.parse_args()

    input_path = pathlib.Path(args.input_path)
    output_dir = pathlib.Path(args.dst_path)
    is_logarithm = args.log

    sr = 48000
    data = []
    if input_path.suffix == ".wav":
        data, sr = librosa.load(str(input_path), sr=None)
    elif input_path.suffix == ".csv":
        df = pd.read_csv(str(input_path), header=None)
        data = np.array(df[0], dtype=np.float)
    else:
        parser.usage()
        exit(1)

    d = np.abs(librosa.stft(data))
    log_D = librosa.amplitude_to_db(d, ref=np.max)

    plt.figure(figsize=(8, 7))
    if is_logarithm:
        librosa.display.specshow(log_D, sr=sr, x_axis='time', y_axis='log')
        librosa.display.specshow(log_D, sr=sr, x_axis='time', y_axis='log')
    else:
        librosa.display.specshow(log_D, sr=sr, x_axis='s', y_axis='linear')

    plt.set_cmap("inferno")
    plt.xlabel("Time [sec]")
    plt.ylabel("Frequency [Hz]")
    plt.title('Spectrogram')
    plt.colorbar(format='%2.0f dB')
    plt.tight_layout()
    plt.show()

    output_name = pathlib.Path(input_path.name).with_suffix(".png")
    output_path = pathlib.Path.joinpath(output_dir, output_name)

    plt.savefig(str(output_path))

    print(f"\nimage is saved at: {output_path}\n")


if __name__ == '__main__':
    main()
