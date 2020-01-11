#! /usr/bin/env python
# coding: utf-8

import argparse
import pathlib

import numpy as np
import soundfile as sf


def main():
    description = "This script calculates the convolution of two wav files."
    usage = f"Usage: python {__file__} [-m full|valid|same] name1.wav name2.wav /path/to/output_name.wav"

    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('input_paths',
                        nargs="*",
                        const=None,
                        default=None,
                        type=str,
                        help='paths where the wav file is located.',
                        )

    parser.add_argument('-o', '--output_path',
                        nargs='?',
                        const="/tmp/conv.wav",
                        default="conv.wav",
                        type=str,
                        help='Output file path where you want to locate wav file. (default: current directory)',
                        )

    parser.add_argument('-m', '--mode',
                        action='store',
                        nargs='?',
                        default="full",
                        type=str,
                        choices=['full', 'valid', 'same'],
                        help='Convolution type',
                        )

    args = parser.parse_args()

    input_paths = args.input_paths
    output_path = pathlib.Path(args.output_path)
    mode = args.mode

    if len(input_paths) != 2:
        print(f"Error: number of arguments is invalid. got:{len(input_paths)}")
        print(parser.usage)
        exit(1)

    if mode != "full" and mode != "valid" and mode != "same":
        print(f"Error: mode of convolution is invalid. got:{mode}")
        print(parser.usage)

        exit(1)

    input_path_1 = input_paths[0]
    input_path_2 = input_paths[1]
    output_path = output_path

    output_path = pathlib.Path(output_path)

    data_1, fs_1 = sf.read(input_path_1)
    data_2, fs_2 = sf.read(input_path_2)

    print("working...")
    wav_out = np.convolve(data_1, data_2, mode=mode)

    sf.write(file=str(output_path.stem + ".wav"), data=wav_out, samplerate=48000, endian="LITTLE",
             format="WAV", subtype="PCM_16")

    print(f"output files are saved at: {output_path}")


if __name__ == '__main__':
    main()
