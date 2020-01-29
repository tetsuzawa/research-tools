# coding:utf-8
import sys

import soundfile as sf


def main():
    print("start")

    filename = sys.argv[1]
    filename_L = sys.argv[2]
    filename_R = sys.argv[3]
    print("input: ", filename)
    print("output L: ", filename_L)
    print("output R: ", filename_R)

    data, fs = sf.read(filename)
    mono_L = data[:, 0]
    mono_R = data[:, 1]

    sf.write(file=filename_L, data=mono_L, samplerate=48000, endian="LITTLE", format="WAV", subtype="PCM_16")
    sf.write(file=filename_R, data=mono_R, samplerate=48000, endian="LITTLE", format="WAV", subtype="PCM_16")

    print("done")


if __name__ == '__main__':
    main()
