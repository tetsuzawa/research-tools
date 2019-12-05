# encording: utf-8

import os
import argparse
import pathlib

import numpy as np
import pandas as pd
import matplotlib

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
                        nargs=None,
                        const=None,
                        default=None,
                        type=str,
                        help='Directory path where the csv file is located.',
                        metavar=None)

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        const="/Users/tetsu/personal_files/Research/filters/test/img",
                        default=".",
                        # default=None,
                        type=str,
                        help='Directory path where you want to locate png files. (default: current directory)',
                        metavar=None)

    # parser.add_argument('-t', '--taps',
    #                     action='store',
    #                     nargs='?',
    #                     default=4,
    #                     default=None,
                        # type=int,
                        # help='Directory path where you want to locate png files. (default: current directory)',
                        # metavar=None)

    args = parser.parse_args()

    input_name = args.csv_path
    input_name = pathlib.Path(input_name)

    df = pd.read_csv(input_name, header=None)
    print("analize file name: ", input_name)

    d, y, e, mse = df[0], df[1], df[2], df[3]

    fig = plt.figure()
    # mse_tap = args.taps
    # mse = []
    # for i in range(len(d) - mse_tap):
    #     mse.append(MSE(d[i:i + mse_tap], y[i:i + mse_tap]))
    # mse = [MSE(e[i:i + mse_tap]) for i in range(len(e) - mse_tap)]
    #
    # log_mse = 20 * np.log10(mse)
    # print(log_mse[:5])
    # if np.max(log_mse) > 1:
    #     log_mse -= np.max(log_mse)
    # else:
    #     log_mse += np.max(log_mse)
    # print(log_mse[:5])

    ax1 = fig.add_subplot(111)
    ax1.set_ylabel("MSE [dB]")
    ax1.set_xlabel("iteration")
    ax1.plot(mse, "y-", alpha=1.0)
    # ax1.set_yscale("log")
    plt.grid()

    output_dir = pathlib.Path(args.dst_path)
    input_name = pathlib.Path(str(input_name.stem) + "_conv")
    output_name = pathlib.Path(input_name.name).with_suffix(".png")
    output_path = pathlib.Path.joinpath(output_dir, output_name)
    plt.savefig(output_path)
    print("\nfilterd data plot is saved at: ", output_path, "\n")


def MSE(y_list, x_list=None):
    if x_list is None:
        x_list = np.zeros(len(y_list))
    x_list = np.array(x_list)
    y_list = np.array(y_list)
    # mse = []
    # for i in range(len(x_list)):
    #     mse.append((x_list[i] - y_list[i]) ** 2)

    mse = (y_list - x_list) ** 2

    return sum(mse) / len(mse)


# %%
if __name__ == '__main__':
    main()
