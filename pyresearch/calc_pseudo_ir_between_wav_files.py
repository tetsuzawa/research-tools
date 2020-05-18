#! /usr/bin/env python
# coding: utf-8

import sys

import numpy as np
import soundfile as sf


def main():
    l_path = sys.argv[1]
    r_path = sys.argv[2]
    out_path = sys.argv[3]

    data_l, fs_l = sf.read(l_path)
    data_r, fs_r = sf.read(r_path)

    F_l = np.fft.fft(data_l)
    F_r = np.fft.fft(data_r)

    F_pseudo_ir = F_l / F_r
    f_pseude_ir = np.fft.ifft(F_pseudo_ir)
    f_pseude_ir_real = np.real(f_pseude_ir)

    sig = f_pseude_ir_real
    sf.write(file=out_path, data=sig, samplerate=48000, endian="LITTLE", format="WAV", subtype="PCM_16")


if __name__ == '__main__':
    main()
