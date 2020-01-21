# encoding: utf-8

import argparse
import pathlib

import matplotlib
import pandas as pd
from scipy import signal

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
plt.rcParams['figure.subplot.wspace'] = 0.5


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

    parser.add_argument('-s', '--sample',
                        action='store',
                        nargs='?',
                        const=-1,
                        default=-1,
                        # default=None,
                        type=int,
                        help='Number of samples to plot',
                        metavar=None)

    args = parser.parse_args()
    output_dir = pathlib.Path(args.dst_path)
    sample = args.sample

    SNR_list = [0, -20, -40]
    LEN_list = [4, 64, 256]
    ALGO_list = ["NLMS", "AP", "RLS"]
    APP_NAME = "auto_on_ref_convo"

    colors = ["y-", "r-", "b-", "g-", "c-", "m-"]

    fig, ax = plt.subplots(3, 3, figsize=(14, 14))

    # ******************* band control *******************
    filter1 = signal.firwin(numtaps=512, cutoff=8000, width=None, pass_zero="lowpass", window='hamming', nyq=None, fs=48000)
    # ******************* band control *******************

    for i, SNR in enumerate(SNR_list):
        for j, LEN in enumerate(LEN_list):
            for k, ALGO in enumerate(ALGO_list):
                input_path = f"SNR_{SNR}/{ALGO}_{APP_NAME}_L-{LEN}_mse.csv"
                if ALGO == "AP":
                    input_path = f"SNR_{SNR}/{ALGO}_{APP_NAME}_L-{LEN}_order-8_mse.csv"

                df = pd.read_csv(input_path, header=None)
                print("analize file name: ", input_path)

                mse = df[3]

                # ******************* band control *******************
                mse_8kHz_lpf = signal.lfilter(filter1, 1, mse)
                print("lpf")
                # ******************* band control *******************

                # ax[i, j].plot(mse[:sample], colors[k], alpha=0.5, label=ALGO)
                ax[i, j].plot(mse_8kHz_lpf[:sample], colors[k], alpha=0.5, label=ALGO)

                # ax[i, j].legend()
                # ax[i, j].set_ylabel("MSE [dB]")
                # ax[i, j].set_xlabel("Iteration")

                # *********** legend ************
                # box = ax[i, j].get_position()
                # ax[i, j].set_position([box.x0, box.y0, box.width * 0.8, box.height])
                # ax[i, j].legend(loc='center left', bbox_to_anchor=(1, 0.5))
                # *********** legend ************

                ax[i, j].set_ylim(-100, 5)
                ax[i, j].grid()
    # plt.legend()
    # plt.ylabel("MSE [dB]")
    # plt.xlabel("Iteration")
    # plt.ylim(-100, 5)

    # plt.tight_layout()
    # plt.grid()

    # for i, input_path in enumerate(input_paths):
    #     df = pd.read_csv(input_path, header=None)
    #     print("analize file name: ", input_path)
    #
    #     input_path = pathlib.Path(input_path)
    #
    #     num = str(input_path.stem).split("-")[1].split(".")[0].split("_")[0]
    #
    #     d, y, e, mse = df[0], df[1], df[2], df[3]
    #
    #     ax.plot(mse[:sample], colors[i], alpha=0.5, label=num)
    #
    # ax.legend()
    # ax.set_ylabel("MSE [dB]")
    # ax.set_xlabel("iteration")
    # ax.set_ylim(-80, 5)
    #
    # plt.tight_layout()
    # plt.grid()

    # algo = str(input_path.stem).split("_")[0]
    # subject = str(input_path.stem).split("_")[1]
    output_name = pathlib.Path("onepage").with_suffix(".png")
    output_path = pathlib.Path.joinpath(output_dir, output_name)
    plt.savefig(output_path)
    print("\nfilterd data plot is saved at: ", output_path, "\n")


if __name__ == '__main__':
    main()
