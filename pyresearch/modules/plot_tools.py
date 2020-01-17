# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

# diagram display settings
plt.rcParams['font.family'] = 'IPAPGothic'
plt.rcParams['font.size'] = 16
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.width'] = 1.0
plt.rcParams['ytick.major.width'] = 1.0
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.figsize'] = (8, 7)
plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.subplot.hspace'] = 0.3
plt.rcParams['figure.subplot.wspace'] = 0.3


class PlotTools(object):
    """ PlotTools - plotting utility class for research
    """

    def __init__(self, y, fs=44100, fft_N=1024, stft_N=256, **kwargs):

        if "start_pos" in kwargs:
            self.start_sec = kwargs["start_sec"]
        else:
            self.start_sec = 0

        #
        self.y = np.array(y)  # data
        self.fs = fs  # Sampling frequency
        self.dt = 1 / fs  # Sampling interval
        # Start position to analyse
        self.start_pos = int(self.start_sec / self.dt)

        self.fft_N = fft_N  # FFT length
        self.stft_N = stft_N  # STFT length
        self.freq_list = np.fft.fftfreq(fft_N, d=self.dt)  # FFT frequency list

        if "window" in kwargs:
            window_name = kwargs["window"]
        else:
            window_name = "hamming"

        self.fft_window = define_window_function(name=window_name, N=self.fft_N)
        self.stft_window = define_window_function(name=window_name, N=self.stft_N)

        self.Y = np.fft.fft(self.fft_window * self.y)
        self.samples = np.arange(self.start_pos, fft_N + self.start_pos)
        self.t = np.arange(self.start_sec, (fft_N + self.start_pos) * self.dt, self.dt)

        y_abs = np.abs(y)
        # Complement 0 or less to mean to prevent from divergence
        self.y_abs = completion_0(y_abs)  # Absolute value of y
        self.y_gain = 20.0 * np.log10(y_abs)  # Gain of y

        # Spectrum
        self.amp_spectrum = np.abs(self.Y) / fft_N * 2
        self.amp_spectrum[0] = self.amp_spectrum[0] / 2
        self.gain_spectrum = 20 * np.log10(self.amp_spectrum / np.max(self.amp_spectrum))
        self.phase_spectrum = np.rad2deg(np.angle(self.Y))
        self.power_spectrum = self.amp_spectrum ** 2
        self.power_gain_spectrum = 10 * np.log10(self.power_spectrum / np.max(self.power_spectrum))

        self.acf = np.real(np.fft.ifft(self.power_spectrum / np.amax(self.power_spectrum)))
        self.acf = self.acf / np.amax(self.acf)

    def plot_y_time(self):
        """plot_y_time - y vs time [sec]
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(self.t, self.y, "-", markersize=1)
        ax1.axis([self.start_sec, (self.fft_N + self.start_pos) *
                  self.dt, np.amin(self.y) * (-1.1), np.amax(self.y) * 1.1])
        ax1.set_xlabel("Time [sec]")
        ax1.set_ylabel("Amplitude")
        ax1.set_title("Amplitude - Time")
        plt.show()

    def plot_y_sample(self):
        """plot_y_sample - y vs sample number
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(self.samples, self.y, "-", markersize=1)
        ax1.axis([self.start_pos, self.fft_N + self.start_pos,
                  np.amin(self.y) * 1.1, np.amax(self.y) * 1.1])
        ax1.set_xlabel("Sample")
        ax1.set_ylabel("Amplitude")
        ax1.set_title("Amplitude - Sample")
        plt.show()

    def plot_freq_analysis_log(self):
        """ plot_freq_analysis_log - 1. gain vs frequency. 2. phase vs frequency
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax1.set_xscale('log')
        ax1.axis([10, self.fs / 2, np.amin(self.gain_spectrum),
                  np.amax(self.gain_spectrum) + 10])
        ax1.plot(self.freq_list, self.gain_spectrum, '-', markersize=1)
        ax1.set_xlabel("Frequency [Hz]")
        ax1.set_ylabel("Amplitude [dB]")
        ax1.set_title("Amplitude spectrum")

        ax2 = fig.add_subplot(212)
        ax2.set_xscale('log')
        ax2.axis([10, self.fs / 2, -180, 180])
        ax2.set_yticks(np.linspace(-180, 180, 9))
        ax2.plot(self.freq_list, self.phase_spectrum, '-', markersize=1)
        ax2.set_xlabel("Frequency [Hz]")
        ax2.set_ylabel("Phase [deg]")
        ax2.set_title("Phase spectrum")
        plt.show()

    def plot_freq_analysis(self):
        """ plot_freq_analysis - 1. amplitude vs time [sec]. 2. amplitude vs frequency
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax1.plot(self.t, self.y, "-", markersize=1)
        ax1.axis([self.start_sec, (self.fft_N + self.start_pos) *
                  self.dt, np.amin(self.y) * 1.2, np.amax(self.y) * 1.2])
        ax1.set_xlabel("Time [sec]")
        ax1.set_ylabel("Amplitude")
        ax1.set_title("Amplitude - Time")

        ax2 = fig.add_subplot(212)
        ax2.axis([10, self.fs / 2, np.amin(self.amp_spectrum)
                  * 0.9, np.amax(self.amp_spectrum) * 1.1])
        ax2.plot(self.freq_list, self.amp_spectrum, '-', markersize=1)
        ax2.set_xlabel("Frequency [Hz]")
        ax2.set_ylabel("Amplitude")
        ax2.set_title("Amplitude - Frequency")
        plt.show()

    def plot_power_gain_spectrum(self):
        """ plot_power_gain_spectrum - power vs frequency
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_xscale('log')
        ax1.axis([10, self.fs / 2, np.amin(self.power_gain_spectrum),
                  np.amax(self.power_gain_spectrum) + 10])
        ax1.plot(self.freq_list, self.gain_spectrum, '-', markersize=1)
        ax1.set_xlabel("Frequency [Hz]")
        ax1.set_ylabel("power")
        ax1.set_title("Power spectrum")
        plt.show()

    def plot_acf(self):
        """ plot_power_gain_spectrum - auto correlation function
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.axis([-self.fft_N / 10, self.fft_N / 2, np.amin(self.acf) * 1.1,
                  np.amax(self.acf) * 1.1])
        ax1.plot(list(range(self.fft_N)), self.acf, '-', markersize=1)
        ax1.set_xlabel("sample number")
        ax1.set_ylabel("Correlation")
        ax1.set_title("Auto correlation Function")
        plt.show()

    def plot_spectrogram_acf(self):
        """ plot_power_gain_spectrum - 1. spectrogram. 2. short time auto correlation function
        """
        # The degree of frame overlap when the window is shifted
        overlap = int(self.stft_N / 2)
        # Length of wav
        frame_length = len(self.y)
        # Time per wav_file
        time_of_file = frame_length * self.dt

        # Define execute time
        start = overlap * self.dt
        stop = time_of_file
        step = (self.stft_N - overlap) * self.dt
        time_ruler = np.arange(start, stop, step)

        # Definition initialization in transposition state
        spec = np.zeros([len(time_ruler), 1 + int(self.stft_N / 2)])
        st_acf = np.zeros([len(time_ruler), 1 + int(self.stft_N / 2)])
        pos = 0

        for fft_index in range(len(time_ruler)):
            # Frame cut out
            frame = self.y[pos:pos + self.stft_N]
            # Frame cut out determination
            if len(frame) == self.stft_N:
                # Multiply window function
                windowed_data = self.stft_window * frame
                # FFT for only real demention
                fft_result = np.fft.rfft(windowed_data)
                fft_result = np.abs(fft_result)
                fft_result = fft_result / np.amax(fft_result)
                power_spectrum = np.abs(fft_result) ** 2
                acf = np.real(np.fft.ifft(
                    power_spectrum / np.amax(power_spectrum)))
                acf = acf / np.amax(acf)
                # Find power spectrum
                fft_data = 10 * np.log10(np.abs(fft_result) ** 2)
                # Assign to spec
                for i in range(len(spec[fft_index])):
                    spec[fft_index][-i - 1] = fft_data[i]
                    st_acf[fft_index][-i - 1] = acf[i]

                # Shift the window and execute the next frame.
                pos += (self.stft_N - overlap)

        # ============  plot  =============
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        im = ax1.imshow(spec.T, extent=[0, time_of_file,
                                        0, self.fs / 2],
                        aspect="auto",
                        cmap="inferno",
                        interpolation="nearest",
                        norm=Normalize(vmin=-80, vmax=0))
        ax1.set_xlabel("Time[sec]")
        ax1.set_ylabel("Frequency[Hz]")
        ax1.set_title("Spectrogram")
        pp1 = fig.colorbar(im, ax=ax1, orientation="vertical")
        plt.tight_layout()
        # pp1.set_clim(-80, 0)
        pp1.set_label("power")
        plt.show()

        # ============  plot  =============
        fig = plt.figure()
        ax2 = fig.add_subplot(111)
        im2 = ax2.imshow(st_acf.T, extent=[0, time_of_file,
                                           0, self.fs / 2],
                         aspect="auto",
                         cmap="inferno",
                         interpolation="nearest",
                         norm=Normalize(vmin=0, vmax=1.00))

        ax2.set_xlabel("time[sec]")
        ax2.set_ylabel("frequency[Hz]")
        ax2.set_title("Short Time Auto correlation Function")

        pp2 = fig.colorbar(im2, ax=ax2, orientation="vertical")
        plt.tight_layout()
        pp2.set_label("power")

        plt.show()

    def plot_all(self):
        """ plot_all - execute all of plotting functions
        """
        self.plot_y_time()
        self.plot_y_sample()
        self.plot_freq_analysis()
        self.plot_freq_analysis_log()
        self.plot_power_gain_spectrum()
        self.plot_acf()
        self.plot_spectrogram_acf()


def completion_0(data_array):
    """completion_0 - intermediate value completion
    """
    under_0list = np.where(data_array <= 0)
    for under_0 in under_0list:
        try:
            data_array[under_0] = 1e-8
            # 抜け値など、平均を取りたい場合コメントアウトを外す
            # data_array[under_0] = (
            #     data_array[under_0-1] + data_array[under_0+1]) / 2
        except IndexError as identifier:
            print(identifier)
            data_array[under_0] = 1e-8
        return data_array


def define_window_function(N, name):
    """define_window_function - defines window function
    """
    if name == "kaiser":
        # TODO kaiser_param kakikaeru
        # kaiser_param = input("Parameter of Kaiser Window : ")
        kaiser_param = 5
    else:
        kaiser_param = 5

    windows_dic = {
        "rectangular": np.ones(shape=N),
        "hamming": np.hamming(M=N),
        "hanning": np.hanning(M=N),
        "bartlett": np.bartlett(M=N),
        "blackman": np.blackman(M=N),
        "kaiser": np.kaiser(M=N, beta=kaiser_param),
    }

    if name in windows_dic:
        return windows_dic[name]
    else:
        raise WindowNameNotFoundError


class WindowNameNotFoundError(Exception):
    """Window name not found
    """
    print("Window Not Found")
