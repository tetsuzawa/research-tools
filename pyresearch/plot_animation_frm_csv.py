# encording: utf-8

import argparse
import pathlib

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import animatplot as amp

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
    # parser = argparse.ArgumentParser(description="This script plots graph from a csv file with 3 columns.")
    #
    # parser.add_argument('csv_path',
    #                     action='store',
    #                     nargs=None,
    #                     const=None,
    #                     default=None,
    #                     type=str,
    #                     help='Directory path where the csv file is located.',
    #                     metavar=None)
    #
    # parser.add_argument('-d', '--dst_path',
    #                     action='store',
    #                     nargs='?',
    #                     const="/Users/tetsu/personal_files/Research/filters/test/img",
    #                     default=".",
    #                     default=None,
    # type=str,
    # help='Directory path where you want to locate png files. (default: current directory)',
    # metavar=None)
    #
    # args = parser.parse_args()
    #
    # input_filename = args.csv_path
    # input_name_list = input_filename.split(".")
    #
    # df = pd.read_csv(input_filename, header=None)
    # print("analize file name: ", input_filename)
    #
    # d, y, e = df[0], df[1], df[2]
    play_animation(None, None, None)

    # plt.figure(facecolor='w')  # Backgroundcolor_white
    # plt.plot(d, "r--", alpha=0.5, label="desired signal d(n)")
    # plt.plot(y, "b--", alpha=0.5, label="output y(n)")
    # plt.plot(e, "y-", alpha=0.5, label="error e(n)")
    # plt.grid()
    # plt.legend()
    # plt.title('LMS Algorithm Online')
    #
    # img_out_dir = pathlib.Path(args.dst_path)
    # img_out_name = "".join(input_name_list[:-1]) + ".png"
    # img_out_path = pathlib.Path.joinpath(img_out_dir, img_out_name)
    # plt.savefig(img_out_path)
    # print("\nfilterd data plot is saved at: ", img_out_path, "\n")


def play_animation(d, y, e):
    fig = plt.figure()

    def plot(data):
        plt.cla()  # 現在描写されているグラフを消去
        rand = np.random.randn(100)  # 100個の乱数を生成
        im = plt.plot(rand)  # グラフを生成

    ani = FuncAnimation(fig, plot, interval=100, frames=10)
    # ani.save("output.gif", writer="imagemagick")
    ani.save("output.html", writer="imagemagick")


# %%
if __name__ == '__main__':
    main()
