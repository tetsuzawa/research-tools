#!/usr/bin/env python
# encoding: utf-8

import os
import argparse
import pathlib

import numpy as np
import soundfile as sf
import librosa
import librosa.display
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'IPAPGothic'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['font.size'] = 16
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.figsize'] = (8, 7)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.subplot.hspace'] = 0.3
plt.rcParams['figure.subplot.wspace'] = 0.3


def main():
    parser = argparse.ArgumentParser(description="This script plots graph from a csv file with 3 columns.")

    parser.add_argument('input_path',
                        action='store',
                        nargs=None,
                        const=None,
                        default=None,
                        type=str,
                        help='Directory path where the input file is located.',
                        metavar=None)

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        const="/tmp",
                        default=".",
                        # default=None,
                        type=str,
                        help='Directory path where you want to locate img files. (default: current directory)',
                        metavar=None)

    parser.add_argument('-l', '--log',
                        action='store_true',
                        help='Use y-axis logarithmic display.')

    args = parser.parse_args()

    input_path = pathlib.Path(args.input_path).absolute()
    input_name_list = str(input_path).split(".")

    output_dir = pathlib.Path(args.dst_path).absolute()

    is_logarithm = args.log

    #####################
    # TODO issue
    with sf.SoundFile(input_path) as sf_desc:
        sr_native = sf_desc.samplerate
        print(sr_native)
    #####################

    y, sr = librosa.load(str(input_path), sr=sr_native)

    D = np.abs(librosa.stft(y))
    log_D = librosa.amplitude_to_db(D, ref=np.max)

    plt.figure(figsize=(8, 7))
    if is_logarithm:
        librosa.display.specshow(log_D, sr=sr, x_axis='time', y_axis='log')
    else:
        librosa.display.specshow(log_D, sr=sr, x_axis='time', y_axis='linear')

    plt.set_cmap("inferno")
    plt.title('Spectroram')
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    plt.show()

    output_name = pathlib.Path(input_path.name).with_suffix(".png")
    output_path = pathlib.Path.joinpath(output_dir, output_name)

    plt.savefig(str(output_path))

    print(f"\nimage is saved at: {output_path}\n")


if __name__ == '__main__':
    main()
