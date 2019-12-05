# encording: utf-8

import os
import sys
import argparse
import pathlib

import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import soundfile as sf

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

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        const="/tmp",
                        default=".",
                        # default=None,
                        type=str,
                        help='Directory path where you want to locate png files. (default: current directory)',
                        metavar=None)

    args = parser.parse_args()
    output_dir = pathlib.Path(args.dst_path)

    for input_path in sys.args[1:]:

        data, sr = sf.read(input_path)

        print("analize file name: ", input_path)

        fig, ax = plt.subplots(1,1,figsize=(12, 6))

        ax.plot(data, "b")
        ax.set_xlabel("iteration")
        ax.legend()
        plt.grid()

        output_name = pathlib.Path(input_path).with_suffix(".png")
        output_path = pathlib.Path.joinpath(output_dir, output_name)
        plt.savefig(output_path)
        print("\n plot is saved at: ", output_path, "\n")


if __name__ == '__main__':
    main()
