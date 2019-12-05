# coding:utf-8
import sys

import numpy as np
import wave

from wave_handler_multi_ch import WaveHandler


def main():
    print("start")

    filename = sys.argv[1]
    filename_L = sys.argv[2]
    filename_R = sys.argv[3]
    print("input: ", filename)
    print("output L: ", filename_L)
    print("output R: ", filename_R)
    # %%
    stereo_wav = WaveHandler(filename)

    # %%
    mono_L = stereo_wav.data[::2]
    mono_R = stereo_wav.data[1::2]

    # %%

    # %%
    L = WaveHandler()
    R = WaveHandler()

    # %%
    L.ch = 1
    L.width = 2
    L.fs = 48000
    R.ch = 1
    R.width = 2
    R.fs = 48000

    # %%

    L.wave_write(filename_L, mono_L)
    R.wave_write(filename_R, mono_R)

    # %%
    print("done")


if __name__ == '__main__':
    main()
