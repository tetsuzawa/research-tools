# %%
import os
import argparse
import pathlib

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

plt.rcParams['font.family'] = 'IPAPGothic'  # 使用するフォント
# x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['xtick.direction'] = 'in'
# y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True  # x軸の目盛線の上側を表示
plt.rcParams['ytick.right'] = True  # y軸の目盛線の右側を表示
plt.rcParams['xtick.major.width'] = 1.0  # x軸主目盛り線の線幅
plt.rcParams['ytick.major.width'] = 1.0  # y軸主目盛り線の線幅
plt.rcParams['font.size'] = 11  # フォントの大きさ
plt.rcParams['axes.linewidth'] = 1.0  # 軸の線幅edge linewidth。囲みの太さ
plt.rcParams['figure.figsize'] = (8, 7)
plt.rcParams['figure.dpi'] = 300  # dpiの設定
plt.rcParams['figure.subplot.hspace'] = 0.3  # 図と図の幅
plt.rcParams['figure.subplot.wspace'] = 0.3  # 図と図の幅


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
                        type=str,
                        help='Directory path where you want to locate png files. (default: current directory)',
                        metavar=None)

    args = parser.parse_args()

    input_filename = args.csv_path
    input_name_list = input_filename.split(".")

    df = pd.read_csv(input_filename, header=None)
    print("analize file name: ", input_filename)

    d, y, e = df[0], df[1], df[2]

    plt.figure(facecolor='w')  # Backgroundcolor_white
    plt.plot(d, "r--", alpha=0.5, label="desired signal d(n)")
    plt.plot(y, "b--", alpha=0.5, label="output y(n)")
    plt.plot(e, "y-", alpha=0.5, label="error e(n)")
    plt.grid()
    plt.legend()
    plt.title('LMS Algorithm Online')

    # img_out_dir = "/Users/tetsu/personal_files/Research/filters/test/LMS_img/"
    img_out_dir = pathlib.Path(args.dst_path)
    img_out_name = "".join(input_name_list[:-1]) + ".png"
    img_out_path = img_out_dir.joinpath(img_out_name)
    plt.savefig(img_out_path)
    print("\nfilterd data plot is saved at: ", img_out_path, "\n")


# %%
if __name__ == '__main__':
    main()
