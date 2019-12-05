# encording: utf-8

import os
import argparse
import pathlib

import numpy as np
import pandas as pd
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
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.figsize'] = (8, 7)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['figure.subplot.hspace'] = 0.3
plt.rcParams['figure.subplot.wspace'] = 0.3


def main():
    parser = argparse.ArgumentParser(description="This script plots graph from a csv file with 3 columns.")

    parser.add_argument('input_path_1',
                        action='store',
                        type=str,
                        help='Directory path where the csv file is located.',)
    parser.add_argument('input_path_2',
                        action='store',
                        type=str,
                        help='Directory path where the csv file is located.',)
    parser.add_argument('input_path_3',
                        action='store',
                        type=str,
                        help='Directory path where the csv file is located.',)

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        const="/Users/tetsu/personal_files/Research/filters/test/img",
                        default=".",
                        # default=None,
                        type=str,
                        help='Directory path where you want to locate png files. (default: current directory)',
                        metavar=None)

    args = parser.parse_args()

    input_name_1 = args.input_path_1
    input_name_2 = args.input_path_2
    input_name_3 = args.input_path_3
    input_name_1 = pathlib.Path(input_name_1)
    input_name_2 = pathlib.Path(input_name_2)
    input_name_3 = pathlib.Path(input_name_3)

    df1 = pd.read_csv(input_name_1, header=None)
    df2 = pd.read_csv(input_name_2, header=None)
    df3 = pd.read_csv(input_name_3, header=None)
    print("analize file name: ", input_name_1)
    print("analize file name: ", input_name_2)
    print("analize file name: ", input_name_3)

    d1, y1, e1, mse1 = df1[0], df1[1], df1[2], df1[3]
    d2, y2, e2, mse2 = df2[0], df2[1], df2[2], df2[3]
    d3, y3, e3, mse3 = df3[0], df3[1], df3[2], df3[3]

    fig = plt.figure()

    ax1 = fig.add_subplot(111)
    ax1.plot(mse1, "y-", alpha=0.5, label="NLMS")
    ax1.plot(mse2, "r-", alpha=0.5, label="AP")
    ax1.plot(mse3, "b-", alpha=0.5, label="RLS")
    ax1.set_ylabel("MSE [dB]")
    ax1.set_xlabel("iteration")
    ax1.legend()
    plt.grid()

    output_dir = pathlib.Path(args.dst_path)
    subject = str(input_name_1.stem).split("_")[1]
    num = str(input_name_1.stem).split("-")[1].split(".")[0]
    output_name = pathlib.Path("algo_"+subject+"_L-"+num).with_suffix(".png")
    output_path = pathlib.Path.joinpath(output_dir, output_name)
    plt.savefig(output_path)
    print("\nfilterd data plot is saved at: ", output_path, "\n")


if __name__ == '__main__':
    main()
