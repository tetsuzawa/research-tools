# -*- coding: utf-8 -*-

import warnings

import numpy as np
import matplotlib.pyplot as plt


class StepSizeError(Exception):
    pass


def nlms_agm_on(alpha, update_count, threshold, d, adf_N):
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
        x : ndarray(N, 1)
            filter input figures
        d : ndarray(N, 1)
            desired signal
        adf_N : int
            length of adaptive filter
    """
    if not 0 < alpha < 2:
        raise StepSizeError

    def nlms_agm_adapter(sample_num):

        w = np.random.rand(adf_N, 1)  # initial cofficient (data_len, 1)
        for i in np.arange(1, update_count+1):
            y = np.dot(w.T, x)  # find dot product of cofficients and numbers
            e = d_part[sample_num, 0] - y  # find error
            # update w -> array(e)
            w = w + alpha * np.array(e) * x / x_norm_squ
            if(abs(e) < threshold):  # error threshold
                break

        y_opt = np.dot(w.T, x)  # adapt filter
        return y_opt

    # define time samples
    # t = np.array(np.linspace(0, adf_N, adf_N)).T

    # Make filter input figures
    x = np.random.rand(adf_N, 1)

    # find norm square
    x_norm_squ = np.dot(x.T, x)

    # devision number
    dev_num = len(d) // adf_N
    if len(d) % adf_N != 0:
        sample_len = dev_num*adf_N
        warnings.warn(
            f"the data was not divisible by adf_N, the last part was truncated. \
              original sample : {len(d)} > {sample_len} : truncated sample")
        d = d[:dev_num*adf_N]
    d_dev = np.split(d, dev_num)

    # ADF : Adaptive Filter
    ADF_out = []  # Define output list
    for d_part in d_dev:
        for j in np.arange(0, adf_N, 1):
            end_con = float(nlms_agm_adapter(sample_num=j))
            ADF_out.append(end_con)

    ADF_out_arr = np.array(ADF_out)
    ADF_out_nd = ADF_out_arr.reshape(len(ADF_out_arr), 1)

    # _plot_command_############################
    plt.figure(facecolor='w')  # Backgroundcolor_white
    plt.plot(d, "c--", alpha=0.5, label="Desired Signal")
    plt.plot(ADF_out_nd, "r--", alpha=0.5, label="NLMS_online")
    plt.plot(d-ADF_out_nd, "g--", alpha=0.5, label="NLMS_online_filterd")
    plt.grid()
    plt.legend()
    plt.title('NLMS Algorithm Online')
    try:
        plt.show()
    except KeyboardInterrupt:
        plt.close('all')

    return ADF_out_nd


if __name__ == "__main__":
    adf_N = 256
    # Make desired value
    d = np.random.rand(1347, 1)
    nlms_agm_on(alpha=1.3, update_count=20, threshold=0.01, d=d, adf_N=adf_N)
