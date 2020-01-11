# -*- coding: utf-8 -*-

import warnings

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
matplotlib.rcParams['agg.path.chunksize'] = 100000

class StepSizeError(Exception):
    pass


def nlms_agm_on(alpha, update_count, threshold, d, adf_N, tap_len=64):
    """
    Update formula
    _________________
        w_{k+1} = w_k + alpha * e_k * x_k / ||x||^2 + 1e-8

    Parameters
    -----------------
        alpha : float
            step size
            0 < alpha < 2
        update_count : int
            update count
        threshold : float
            threshold of end condition
        sample_num : int
            sample number
        x : ndarray(adf_N, 1)
            filter input figures
        w : ndarray(adf_N, 1)
            initial coefficient (adf_N, 1)
        d : ndarray(adf_N, 1)
            desired signal
        adf_N : int
            length of adaptive filter
    """
    if not 0 < alpha < 2:
        raise StepSizeError

    def nlms_agm_adapter(sample_num):
        nonlocal x
        nonlocal w
        start_chunk = sample_num * adf_N
        end_chunk = (sample_num + 1) * adf_N

        for _ in range(1, update_count + 1):
            ### y = np.dot(w.T, x)  # find dot product of coefficients and numbers

            # =============
            # TODO 8/14 掛け算を畳み込みにする
            # y = w * x  # find dot product of coefficients and numbers
            y = np.convolve(a=w[:, 0], v=x[:, 0], mode='same').reshape(len(x),1)
            # =============

            ### 動かない d_part_tmp = d_part[start_chunk:end_chunk, 0].reshape(adf_N, 1)
            d_part_tmp = d_part.reshape(adf_N, 1)
            ### 2の1 y_tmp = np.full((adf_N, 1), y)
            # e = (d_part[start_chunk:end_chunk, 0] - np.full((adf_N, 1), y))  # find error
            e = d_part_tmp - y  # find error
            """
            e = d[sample_num] - y  # find error
            """
            # update w -> array(e)
            # 8/14 アダマール積じゃなくてじゃなくてノルムのスカラー積？？
            w = w + alpha * e * x / (x_norm_squ + 1e-8)
            e_norm = np.linalg.norm(e)
            if e_norm < threshold:  # error threshold
                break
            # TODO 8/14 次の消す
            """
            e_norm = np.linalg.norm(e)
            w = w + alpha * e_norm * x / x_norm_squ
            if e_norm < threshold:  # error threshold
                break
            """

        # y_opt = np.dot(w.T, x)  # adapt filter

        # =============
        # TODO 8/14 掛け算を畳み込みにする
        # y_opt = (w * x).reshape(adf_N, )  # adapt filter
        y_opt = (np.convolve(a=w[:, 0], v=x[:, 0], mode='same')).reshape(adf_N, )  # adapt filter
        # =============

        return y_opt

    # define time samples
    # t = np.array(np.linspace(0, adf_N, adf_N)).T

    w = np.random.rand(tap_len, 1)  # initial coefficient (data_len, 1)
    # w = (w - np.mean(w)) * 2

    x = np.random.rand(tap_len, 1)  # Make filter input figures
    x = (x - np.mean(x)) * 2

    # find norm square
    x_norm_squ = np.dot(x.T, x)

    # devision number
    dev_num = len(d) // adf_N
    if len(d) % adf_N != 0:
        sample_len = dev_num * adf_N
        warnings.warn(
            f"the data was not divisible by adf_N, the last part was truncated. \
              original sample : {len(d)} > {sample_len} : truncated sample")
        d = d[:dev_num * adf_N]
    d_dev = np.split(d, dev_num)

    # ADF : Adaptive Filter
    ### 2の2 ###
    adf_out = []  # Define output list
    for i, d_part in enumerate(d_dev):
        ###### end_con = float(nlms_agm_adapter(sample_num=i))
        end_con = nlms_agm_adapter(sample_num=i)
        adf_out.append(end_con)
    """
    ### 2の1 ###
    adf_out = []  # Define output list
    for d_part in d_dev:
        for j in np.arange(0, adf_N, 1):
            end_con = float(nlms_agm_adapter(sample_num=j))
            adf_out.append(end_con)
    """

    """
    adf_out = []  # Define output list
    ########################################
    # TODO dの回数じゃないの？
    # for j in np.arange(0, len(d), 1):
    #     end_con = float(nlms_agm_adapter(sample_num=j))
    #     adf_out.append(end_con)
    ########################################
    for j in np.arange(0, adf_N, 1):
        end_con = float(nlms_agm_adapter(sample_num=j))
        adf_out.append(end_con)
    """

    ##### adf_out_arr = np.array(adf_out)
    ##### adf_out_nd = adf_out_arr.reshape(len(adf_out_arr), 1)
    adf_out_nd = np.array(adf_out).reshape(len(d), 1)

    # _plot_command_############################
    plt.figure(facecolor='w')  # Back ground color_white
    plt.plot(d, "c--", alpha=0.5, label="Desired Signal")
    plt.plot(adf_out_nd, "r--", alpha=0.5, label="NLMS_online")
    # plt.plot(d - adf_out_nd[:len(d)], "g--", alpha=0.5, label="NLMS_online_filtered")
    plt.grid()
    plt.legend()
    plt.title('NLMS Algorithm Online')
    # _plot_command_############################
    plt.figure(facecolor='w')  # Back ground color_white
    plt.plot(d - adf_out_nd[:len(d)], "g--", alpha=1, label="NLMS_online_filtered")
    plt.grid()
    plt.legend()
    plt.title('NLMS Algorithm Online')
    try:
        plt.show()
    except KeyboardInterrupt:
        plt.close('all')

    return adf_out_nd


if __name__ == "__main__":
    adf_N = 64
    # Make desired value
    d = np.random.rand(1028, 1)
    d = (d - np.mean(d)) * 2
    d[50:55] = d[50:55] - 1
    nlms_agm_on(alpha=1, update_count=30, threshold=0.05, d=d, adf_N=adf_N)
