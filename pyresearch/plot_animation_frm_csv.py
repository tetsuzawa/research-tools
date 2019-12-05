# encording: utf-8

import argparse
import pathlib

import numpy as np
import pandas as pd
import animatplot as amp

import matplotlib.pyplot as plt
from matplotlib import animation

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
plt.rcParams['figure.dpi'] = 100
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

    input_name = args.csv_path
    input_name = pathlib.Path(input_name)

    df = pd.read_csv(input_name, header=None)
    print("analize file name: ", input_name)

    d, y, e = df[0], df[1], df[2]

    output_dir = pathlib.Path(args.dst_path)
    # output_name = pathlib.Path(input_name.name).with_suffix(".gif")
    output_name = pathlib.Path(input_name.name).with_suffix(".mp4")
    output_path = pathlib.Path.joinpath(output_dir, output_name)

    samples = args.samples
    interval = args.interval

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_xlabel("iteration n")
    ax1.set_ylim((-1.6, 1.6))
    ax2.set_xlabel("iteration n")
    ax2.set_ylim((-0.5, 0.5))

    ani = animation.FuncAnimation(fig, update, fargs=(d[:samples], y[:samples], e[:samples], ax1, ax2),
                                  interval=interval, frames=int(samples/2))
    # ani.save(output_path, writer='imagemagick')
    ani.save(output_path, writer='ffmpeg')

    print("\nfilterd data plot is saved at: ", output_path, "\n")


def update(i, d, y, e, ax1, ax2):
    if i != 0:
        plt.cla()
    if i == 0:
        ax1.legend(loc='upper right')
        ax1.set_title("Desired value, Filter output and Filter error")
    i = i * 2
    # ax1.plot(d[0:i], y[0:i], "forestgreen", labels="d, y")
    # ax2.plot(e[0:i], "darkred", labels="e")
    # slide_blue = ((0, 50, 101), 0.7)
    # slide_red = ((203, 8, 18), 0.7)
    # slide_yellow = ((218, 178, 79), 1.0)
    ax1.plot(d[0:i], color="b", alpha=0.7, label="desired value d(n)")
    ax1.plot(y[0:i], color="r", alpha=0.7, label="filter output y(n)")
        # ax2.set_title("Filter error")

    ax2.plot(e[0:i], color="y", alpha=1.0, label="filter error e(n)")

        # ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        # ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

# ax1.plot(d[0:i], color=slide_blue )
    # ax1.plot(y[0:i], color=slide_red)
    # ax2.plot(e[0:i], color=slide_yellow)
    # ax1.set_xlim(0, 10)
    # ax1.set_ylim(0, 100)
    # ax2.set_xlim(0, 10)
    # ax2.set_ylim(-100, 0)


# def play_animation(d, y, e):
#     plt.figure(facecolor='w')  # Backgroundcolor_white
#     plt.plot(d, "r--", alpha=0.5, label="desired signal d(n)")
#     plt.plot(y, "b--", alpha=0.5, label="output y(n)")
#     plt.plot(e, "y-", alpha=0.5, label="error e(n)")
#     plt.grid()
#     plt.legend()
#     plt.title('ADF Output')


def f():
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    ax.grid()
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("x", fontsize=15)
    ax.set_ylabel("y", fontsize=15)

    ims = []
    x = np.linspace(0, 2 * np.pi)

    # サブプロットのリストを用意
    for t in range(100):
        y = np.sin(x - t)
        artist = ax.plot(x, y, color="b")
        ims.append(artist)

    # アニメーションを作成
    ani = animation.ArtistAnimation(
        fig,  # Figureオブジェクト
        ims,  # サブプロット(Axes)のリスト
        interval=100,  # サブプロットの更新頻度(ms)
        blit=True  # blitting による処理の高速化
    )

    # plt.show()
    # plt.imshow()
    ani.save("sample.gif", "imagemagick")


# %%
if __name__ == '__main__':
    main()
