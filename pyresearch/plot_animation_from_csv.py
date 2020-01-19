# encoding: utf-8

import argparse
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import animation

plt.rcParams['font.family'] = 'IPAPGothic'
plt.rcParams['font.size'] = 11
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.figsize'] = (8, 7)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.subplot.hspace'] = 0.3
plt.rcParams['figure.subplot.wspace'] = 0.3


def main():
    description = "This script plots graph from a csv file with 3 columns."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('csv_path',
                        action='store',
                        const=None,
                        default=None,
                        type=str,
                        help='Directory path where the csv file is located.',
                        metavar=None)

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        const="/tmp",
                        default=".",
                        type=str,
                        help='Directory path where you want to locate png files. (default: current directory)',
                        metavar=None)

    parser.add_argument('-s', '--samples',
                        action='store',
                        nargs='?',
                        # const="/tmp",
                        default=50,
                        type=int,
                        help='Samples to draw.',
                        metavar=None)

    parser.add_argument('-i', '--interval',
                        action='store',
                        nargs='?',
                        # const="/tmp",
                        default=100,
                        type=int,
                        help='Interval to draw.',
                        metavar=None)

    args = parser.parse_args()

    input_path = args.csv_path
    input_path = pathlib.Path(input_path)

    df = pd.read_csv(input_path, header=None)
    print("analize file name: ", input_path)

    d, y, e = df[0], df[1], df[2]

    output_dir = pathlib.Path(args.dst_path)
    output_name = pathlib.Path(input_path.name).with_suffix(".gif")
    # output_name = pathlib.Path(input_path.name).with_suffix(".mp4")
    output_path = pathlib.Path.joinpath(output_dir, output_name)

    samples = args.samples
    interval = args.interval

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_xlabel("iteration n")
    ax1.set_ylim((-1.6, 1.6))
    ax2.set_xlabel("iteration n")
    ax2.set_ylim((-0.5, 0.5))

    ani = animation.FuncAnimation(fig, update, fargs=(d[:samples], y[:samples], e[:samples], ax1, ax2),
                                  interval=interval, frames=int(samples / 2))
    ani.save(output_path, writer='imagemagick')
    # ani.save(output_path, writer='ffmpeg')

    print("\nfilterd data plot is saved at: ", output_path, "\n")


def update(i, d, y, e, ax1, ax2):
    if i == 0:
        ax1.legend(loc='upper right')
        ax1.set_title("Desired value, Filter output and Filter error")
    else:
        plt.cla()
    i = i * 2
    ax1.plot(d[0:i], color="b", alpha=0.7, label="desired value d(n)")
    ax1.plot(y[0:i], color="r", alpha=0.7, label="filter output y(n)")

    ax2.plot(e[0:i], color="y", alpha=1.0, label="filter error e(n)")


if __name__ == '__main__':
    main()
