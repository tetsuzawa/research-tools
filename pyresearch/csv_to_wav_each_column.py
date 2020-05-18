#! /usr/bin/env python
# coding: utf-8

import pathlib
import sys

import numpy as np
import pandas as pd
import soundfile as sf


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    df = pd.read_csv(input_path)
    output_path = pathlib.Path(output_path)

    arr = np.array(df)

    for i, data in enumerate(arr.T):
        sf.write(file=str(output_path.stem + f"_col{i}.wav"), data=data, samplerate=48000, endian="LITTLE",
                 format="WAV", subtype="PCM_16")

    print(f"output files are saved at: {output_path}")


if __name__ == '__main__':
    main()
