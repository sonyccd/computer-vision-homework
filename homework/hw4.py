from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st


def gauss_kernel(size=3, sigma=1.0):
    interval = (2 * sigma + 1.) / size
    x = np.linspace(-sigma - interval / 2., sigma + interval / 2., size + 1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = kernel_raw / kernel_raw.sum()
    return kernel


if __name__ == '__main__':
    image = io.imread('../img/hw1.jpg')
    plt.imshow(gauss_kernel(3, 0.5))
    plt.show()
