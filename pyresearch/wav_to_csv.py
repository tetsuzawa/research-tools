#! /usr/bin/env python
# coding: utf-8

import pathlib
import sys

import pandas as pd
import soundfile as sf


def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    data, fs = sf.read(input_path)

    df = pd.DataFrame(data)

    output_path = pathlib.Path(output_path)

    df.to_csv(str(output_path.stem + ".csv"), header=None, index=None)

    print(f"output files are saved at: {output_path}")


if __name__ == '__main__':
    main()
