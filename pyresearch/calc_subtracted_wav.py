# %%
import sys
import os.path
import numpy as np


def main():
    current_dir = os.path.dirname(os.path.abspath("__file__"))
    sys.path.append(str(current_dir) + '/research_tools')
    sys.path.append(str(current_dir) + '/sample_wav')

    try:
        from modules.wave_process import WaveHandler

    except ModuleNotFoundError as err:
        print(err)
        raise ModuleNotFoundError

    args = sys.argv

    noise_wav_name = args[1]
    dst_wav_name = args[2]
    out_wav_name = args[3]

    noise_wav = WaveHandler(filename=noise_wav_name)
    dst_wav = WaveHandler(filename=dst_wav_name)
    out_wav = WaveHandler()

    noise_y = np.array(noise_wav.data)
    dst_y = np.array(dst_wav.data)

    noise_Y = np.fft.fft(noise_y)
    dst_Y = np.fft.fft(dst_y)
    out_Y = dst_Y - noise_Y

    out_wav_data = np.fft.ifft(out_Y)

    out_wav.wave_write(out_wav_name, np.real(out_wav_data))


if __name__ == '__main__':
    main()
