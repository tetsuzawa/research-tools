# -*- coding: utf-8 -*-
# python3.7 VS_plot.DXB.py [FILE_NAME] [FFT_LENGTH]
#
import sys
import os.path
import math
import numpy as np
import pandas as pd
import wave
import struct
import string
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
from collections import OrderedDict
from scipy import signal
import time
from stft import stft


plt.rcParams['font.family'] = 'IPAPGothic'  # 使用するフォント
# x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['xtick.direction'] = 'in'
# y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True  # x軸の目盛線の上側を表示
plt.rcParams['ytick.right'] = True  # y軸の目盛線の右側を表示
plt.rcParams['xtick.major.width'] = 1.0  # x軸主目盛り線の線幅
plt.rcParams['ytick.major.width'] = 1.0  # y軸主目盛り線の線幅
plt.rcParams['font.size'] = 11  # フォントの大きさ
plt.rcParams['axes.linewidth'] = 1.0  # 軸の線幅edge linewidth。囲みの太さ
plt.rcParams['figure.figsize'] = (7, 5)
plt.rcParams['figure.dpi'] = 100  # dpiの設定
plt.rcParams['figure.subplot.hspace'] = 0.3  # 図と図の幅
plt.rcParams['figure.subplot.wspace'] = 0.3  # 図と図の幅

# fig = plt.figure(figsize=(8, 11))
# plt.gca().xaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))#y軸小数点以下3桁表示
# plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))#y軸小数点以下3桁表示
# plt.gca().xaxis.get_major_formatter().set_useOffset(False)

# plt.add_axes([left,bottom,width,height],zorder=0)


def define_window_function(name, N, kaiser_para=5):
    if name is None:
        return 1
    elif name == "hamming":
        return np.hamming(M=N)
    elif name == "hanning":
        return np.hanning(M=N)
    elif name == "bartlett":
        return np.bartlett(M=N)
    elif name == "blackman":
        return np.blackman(M=N)
    elif name == "kaiser":
        kaiser_para = input("Parameter of Kaiser Window : ")
        return np.kaiser(N=N, beta=kaiser_para)


def plot_3charts(N, y, fs=44100, start_sec=0, window_func_name="hamming"):
    """
    Parameters
    -----------------
    N : int
        FFT length
    y : list(int)
        Data for analysis
    fs : int
        Sampling freqency
    start_sec : float64
        Start sec
    window_func_name: str
        window_func_name :
            "hamming"
            "hanning"
            "bartlett"
            "blackman"
            "kaiser"

    Usage example
    -----------------
    plot_3charts(N=N, y=data, fs=fs, start_sec=3, window_func_name="hamming")
    """

    # Period
    dt = 1/fs
    # Define start sec
    start_pos = int(start_sec/dt)
    # Redefine y
    y = y[start_pos: N+start_pos]
    # Window function
    window_func = define_window_function(name=window_func_name, N=N)
    # Fourier transform
    Y = np.fft.fft(window_func * y)
    # Find a list of frequencies
    freqList = np.fft.fftfreq(N, d=dt)
    # Find the time for y
    t = np.arange(start_pos*dt, (N+start_pos)*dt, dt)

    # Complement 0 or less to display decibels
    y_abs = np.array(np.abs(y))
    u_0_list = np.where(y_abs <= 0)
    for u_0 in u_0_list:
        y_abs[u_0] = (y_abs[u_0-1] + y_abs[u_0+1]) / 2

    # y decibel desplay
    y_db = 20.0*np.log10(y_abs)

    # amplitudeSpectrum = [np.sqrt(c.real ** 2  + c.imag ** 2 ) for c in Y]
    # phaseSpectrum     = [np.arctan2(np.float64(c.imag),np.float64(c.real)) for c in Y]
    # Adjust the amplitude to the original signal.
    amplitudeSpectrum = np.abs(Y) / N * 2
    amplitudeSpectrum[0] = amplitudeSpectrum[0] / 2
    # amplitudeSpectrum = np.abs(Y) / np.max(amplitudeSpectrum)
    phaseSpectrum = np.rad2deg(np.angle(Y))
    decibelSpectrum = 20.0 * \
        np.log10(amplitudeSpectrum / np.max(amplitudeSpectrum))

    fig = plt.figure(figsize=(11, 8))

    '''
    ax1 = fig.add_subplot(311)
    ax1.plot(y)
    ax1.axis([0,N,np.amin(y),np.amax(y)])
    ax1.set_xlabel("time [sample]")
    ax1.set_ylabel("amplitude")
    '''

    ax1 = fig.add_subplot(321)
    ax1.plot(t, y_db, "-", markersize=1)
    ax1.axis([start_sec, (N+start_pos) * dt, np.amin(y_db), np.amax(y_db)+10])
    ax1.set_xlabel("Time [sec]")
    ax1.set_ylabel("Amplitude [dB]")

    ax2 = fig.add_subplot(322)
    ax2.set_xscale('log')
    ax2.axis([10, fs/2, np.amin(decibelSpectrum), np.amax(decibelSpectrum)+10])
    ax2.plot(freqList, decibelSpectrum, '-', markersize=1)
    ax2.set_xlabel("Frequency [Hz]")
    ax2.set_ylabel("Amplitude [dB]")

    ax3 = fig.add_subplot(323)
    ax3.plot(freqList, decibelSpectrum, '-', markersize=1)
    ax3.axis([0, fs/2, np.amin(decibelSpectrum), np.amax(decibelSpectrum)+10])
    ax3.set_xlabel("Frequency [Hz]")
    ax3.set_ylabel("Amplitude [dB]")

    ax4 = fig.add_subplot(324)
    ax4.set_xscale('log')
    ax4.axis([10, fs/2, -180, 180])
    ax4.set_yticks(np.linspace(-180, 180, 9))
    ax4.plot(freqList, phaseSpectrum, '-', markersize=1)
    ax4.set_xlabel("Frequency [Hz]")
    ax4.set_ylabel("Phase [deg]")

    ax5 = fig.add_subplot(325)
    ax5.plot(t, y, "-", markersize=1)
    ax5.axis([start_sec, (N+start_pos)*dt, np.amin(y)*0.9, np.amax(y)*1.1])
    ax5.set_xlabel("Time [sec]")
    ax5.set_ylabel("Amplitude")

    ax6 = fig.add_subplot(326)
    ax6.axis([10, fs/2, np.amin(amplitudeSpectrum)
              * 0.9, np.amax(amplitudeSpectrum)*1.1])
    ax6.plot(freqList, amplitudeSpectrum, '-', markersize=1)
    ax6.set_xlabel("Frequency [Hz]")
    ax6.set_ylabel("Amplitude")

    # subplot(314)
    # xscale('linear')
    # plot(freqList, phaseSpectrum,".")
    # axis([0,fs/2,-np.pi,np.pi])
    # xlabel("frequency[Hz]")
    # ylabel("phase [rad]")

    try:
        plt.show()
    finally:
        plt.close()


def spectrogram(N, y, fs=44100, window_func_name="hamming"):
    # The degree of frame overlap when the window is shifted
    OVERLAP = N / 2
    # Length of wav
    frame_length = len(y)
    # Time per sample
    dt = 1/fs
    # Time per wav_file
    time_of_file = frame_length * dt

    # Define execute time
    start = OVERLAP * dt
    stop = time_of_file
    step = (N - OVERLAP) * dt
    time_ruler = np.arange(start, stop, step)

    # Window function
    Window_func = define_window_function(name=window_func_name, N=N)

    # Definition initialization in transposition state
    spec = np.zeros([len(time_ruler), 1 + int(N / 2)])
    pos = 0

    """
    stft_test(N=N, y=y, window_func=Window_func, OVERLAP=OVERLAP)
    """

    for fft_index in range(len(time_ruler)):
        # Frame cut out
        frame = y[pos:pos+N]
        # Frame cut out determination
        if len(frame) == N:
            # Multiply window function
            windowed_data = Window_func * frame
            # FFT for only real demention
            fft_result = np.fft.rfft(windowed_data)
            # Find power spectrum
            fft_data = np.log(np.abs(fft_result) ** 2)
            # fft_data = np.log(np.abs(fft_result))
            # fft_data = np.abs(fft_result) ** 2
            # fft_data = np.abs(fft_result)
            # Assign to spec
            for i in range(len(spec[fft_index])):
                spec[fft_index][-i-1] = fft_data[i]

            # Shift the window and execute the next frame.
            pos += (N - OVERLAP)

        # ============  plot  =============
        plt.imshow(spec.T, extent=[0, time_of_file,
                                   0, fs/2], aspect="auto", cmap="inferno")
        plt.xlabel("time[sec]")
        plt.ylabel("frequency[Hz]")
        # cm = plt.pcolormesh(X,Y,z, cmap='inferno')
        # plt.colorbar(, orientation="vertical")
        plt.colorbar()
        plt.show()


def stft_test(N, y, window_func, OVERLAP):
    spectrogram = abs(signal.stft(y, window_func, OVERLAP)[:, : N / 2 + 1]).T

    # 表示
    fig = plt.figure()
    fig.patch.set_alpha(0.)
    imshow_sox(spectrogram)
    plt.tight_layout()
    plt.show()


def imshow_sox(spectrogram, rm_low=0.1):
    max_value = spectrogram.max()
    # amp to dbFS
    db_spec = np.log10(spectrogram / float(max_value)) * 20
    # カラーマップの上限と下限を計算
    hist, bin_edges = np.histogram(db_spec.flatten(), bins=1000, normed=True)
    hist /= float(hist.sum())
    plt.hist(hist)
    plt.show()
    S = 0
    ii = 0
    while S < rm_low:
        S += hist[ii]
        ii += 1
    vmin = bin_edges[ii]
    vmax = db_spec.max()
    plt.imshow(db_spec, origin="lower", aspect="auto",
               cmap="hot", vmax=vmax, vmin=vmin)
