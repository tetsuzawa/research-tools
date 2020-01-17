#!/usr/bin/env python3
# coding: utf-8

import argparse
import pathlib

import numpy as np
import soundfile as sf


def main():
    parser = argparse.ArgumentParser(description="This script makes white noise to designated path.")

    parser.add_argument('duration',
                        action='store',
                        type=float,
                        help='The length of noise.')

    parser.add_argument('-d', '--dst_path',
                        action='store',
                        nargs='?',
                        const="/tmp",
                        default=".",
                        type=str,
                        help='Directory path where you want to locate output files. (default: current directory)')

    args = parser.parse_args()
    duration = args.duration
    output_dir = pathlib.Path(args.dst_path)
    output_name = pathlib.Path.joinpath(output_dir, f"white_noise_{duration}s.wav")

    sig = np.random.rand(int(duration * 48000))

    sf.write(file=str(output_name), data=sig, samplerate=48000, endian="LITTLE", format="WAV", subtype="PCM_16")


if __name__ == '__main__':
    main()
