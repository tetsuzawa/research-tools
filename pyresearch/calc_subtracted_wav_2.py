# coding: utf-8


import sys

import librosa
import numpy as np
import soundfile as sf


def main():
    noise_file_path = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    print('input file:', input_file_path)
    data, data_fs = librosa.load(input_file_path, sr=None, mono=True)
    data_st = librosa.stft(data)
    data_st_abs = np.abs(data_st)
    angle = np.angle(data_st)
    b = np.exp(1.0j * angle)

    print('noise file:', noise_file_path)
    noise_data, noise_fs = librosa.load(noise_file_path, sr=None, mono=True)
    noise_data_st = librosa.stft(noise_data)
    noise_data_st_abs = np.abs(noise_data_st)
    mean_noise_abs = np.mean(noise_data_st_abs, axis=1)

    subtracted_data = data_st_abs - mean_noise_abs.reshape(
        (mean_noise_abs.shape[0], 1))  # reshape for broadcast to subtract
    subtracted_data_phase = subtracted_data * b  # apply phase information
    y = librosa.istft(subtracted_data_phase)  # back to time domain signal

    # save as a wav file
    # scipy.io.wavfile.write(output_file_path, data_fs, (y * 32768).astype(np.int16))  # save signed 16-bit WAV format
    sf.write(file=str(output_file_path), data=y, samplerate=data_fs, endian="LITTLE", format="WAV", subtype="PCM_16")
    print('output file:', output_file_path)


if __name__ == '__main__':
    main()
