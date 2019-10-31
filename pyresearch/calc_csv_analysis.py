# %%
import sys

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


def main():
    input_filename = sys.argv[1]
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

    img_out_dir = "/Users/tetsu/personal_files/Research/filters/test/LMS_img/"
    img_out_name = "".join(input_name_list[:-1]) + ".png"
    plt.savefig(img_out_dir + img_out_name)
    print("\nfilterd data plot is saved at: ", img_out_dir + img_out_name, "\n")


# %%
if __name__ == '__main__':
    main()
