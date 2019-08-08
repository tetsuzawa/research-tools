# -*- coding: utf-8 -*-
# python3.7 VS_plot.DXB.py [FILE_NAME] [FFT_LENGTH]
#
import numpy as np
import wave


class wave_process():

    def __init__(self, filename):
        # open wave file
        wf = wave.open(filename, 'r')

        # waveファイルが持つ性質を取得
        self.filename = filename
        self.ch = wf.getnchannels()
        self.width = wf.getsampwidth()
        self.fs = wf.getframerate()
        self.params = wf.getparams()
        chunk_size = wf.getnframes()
        # load wave data
        amp = (2**8) ** self.width / 2
        data = wf.readframes(chunk_size)   # バイナリ読み込み
        data = np.frombuffer(data, 'int16')     # intに変換
        data = data / amp                  # 振幅正規化
        self.chunk_size = chunk_size
        self.data = data[::self.ch]             # dateを1chに限定
        wf.close()    # 結果表示

        print("分析対象ファイル：", self.filename)
        print("チャンクサイズ：", self.chunk_size)
        print("サンプルサイズのバイト数：", self.width)
        print("チャンネル数：", self.ch)
        print("wavファイルのサンプリング周波数：", self.fs)
        print("パラメータ : ", self.params)
        print("wavファイルのデータ個数：", len(self.data))

    def wave_write(self, filename, data_array):
        ww = wave.open(filename, 'w')
        ww.setnchannels(self.ch)
        ww.setsampwidth(self.width)
        ww.setframerate(self.fs)
        amp = (2**8) ** self.width / 2
        data_array = data_array / np.max(data_array)
        write_array = np.array(data_array * amp, dtype=np.int16)
        ww.writeframes(write_array)
        ww.close()
