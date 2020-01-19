# encoding: utf-8

import argparse
import pathlib

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use('Agg')
import matplotlib.pyplot as plt

"""
Note that the modules (numpy, maplotlib, wave, scipy) are properly installed on your environment.

Plot wave, spectrum, save them as pdf and png at same directory.

Example:
   python calc_wave_analysis.py IR_test.wav
"""

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
    parser = argparse.ArgumentParser(description="This script plots graph from a csv file with 3 columns.")

    parser.add_argument('csv_path',
                        action='store',
                        type=str,
                        help='Directory path where the csv file is located.',
                        metavar=None)

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        default=".",
                        type=str,
                        help='Directory path where you want to locate png files. (default: current directory)',
                        metavar=None)

    parser.add_argument('-l', '--log',
                        action='store_true',
                        help='Use y-axis logarithmic display.')

    args = parser.parse_args()

    input_name = args.csv_path
    input_name = pathlib.Path(input_name)

    is_logarithm = args.log

    df = pd.read_csv(input_name, header=None)
    print("analize file name: ", input_name)

    d, y, e = df[0], df[1], df[2]

    fig, (ax1, ax2) = plt.subplots(2, 1)
    if is_logarithm:
        ax1.set_yscale("log")
        ax2.set_yscale("log")
        d /= np.max(d)
        y /= np.max(d)
        e /= np.max(e)

    ax1.plot(d, "b--", alpha=0.5, label="desired signal d(n)")
    ax1.plot(y, "r-", alpha=0.5, label="output y(n)")
    ax1.legend()
    ax2.plot(e, "y-", alpha=1.0, label="error e(n)")
    plt.grid()
    ax2.legend()
    plt.title('ADF Output')

    output_dir = pathlib.Path(args.dst_path)
    output_name = pathlib.Path(input_name.name).with_suffix(".png")
    output_path = pathlib.Path.joinpath(output_dir, output_name)
    plt.savefig(output_path)
    print("\nfilterd data plot is saved at: ", output_path, "\n")


if __name__ == '__main__':
    main()
