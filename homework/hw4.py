from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st


def gkern(kernlen=21, nsig=3):
    interval = (2*nsig+1.)/(kernlen)
    x = np.linspace(-nsig-interval/2., nsig+interval/2., kernlen+1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    kernel = kernel_raw/kernel_raw.sum()
    return kernel

if __name__ == '__main__':
    image = io.imread('../img/hw1.jpg')
    plt.imshow(gkern(3, 0.5))
    plt.show()