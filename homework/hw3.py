import math

import matplotlib.pyplot as plt
import numpy as np
import skimage.io as io


# returns indexes
def peak_detect(histogram, lookahead=5, min_range=0, max_range=256):
    minum_index = []
    maxum_index = []
    if max_range == 256:
        max_range = len(histogram)
    for i in range(min_range, max_range):
        if lookahead < i < len(histogram) - lookahead:
            if histogram[i + 1:i + lookahead].max() < histogram[i] and histogram[i - lookahead:i - 1].max() < histogram[
                i]:
                if len(maxum_index) > 1:
                    if maxum_index[len(maxum_index) - 1] != i - 1:
                        maxum_index.append(i)
                else:
                    maxum_index.append(i)
            if histogram[i + 1:i + lookahead].min() > histogram[i] and histogram[i - lookahead:i - 1].min() > histogram[
                i]:
                if len(minum_index) > 1:
                    if minum_index[len(minum_index) - 1] != i - 1:
                        minum_index.append(i)
                else:
                    minum_index.append(i)
    return minum_index, maxum_index


def peakiness(img, dist=20):
    hist = np.histogram(img.ravel(), 256)[0]
    maxum_indexs = peak_detect(hist)[1]
    maxum = np.take(hist, maxum_indexs)
    print(maxum)
    min_max_index = np.argpartition(maxum, -4)[-2:]
    print(maxum_indexs, maxum[min_max_index])


def iterative_threshold(img):
    t = np.mean(img)
    r1 = img[img > t]
    r2 = img[img < t]
    r1_mean_old = np.mean(r1)
    r2_mean_old = np.mean(r2)
    count = 0
    while True:
        count = count + 1
        t = 0.5 * (r1_mean_old + r2_mean_old)
        r1 = img[img > t]
        r2 = img[img < t]
        r1_mean_new = np.mean(r1)
        r2_mean_new = np.mean(r2)
        if math.ceil(r1_mean_old) == math.ceil(r1_mean_new) and math.ceil(r2_mean_old) == math.ceil(r2_mean_new):
            break
        elif count > 100:
            break
    return threshold(img, math.ceil(t))


def adaptive_threshold(img):
    img_cp = np.copy(img)
    i, j = img_cp.shape
    hi = math.ceil(i / 2)
    hj = math.ceil(j / 2)
    top_left = img_cp[0:hi, 0:hj]
    top_right = img_cp[0:hi, hj:j]
    bottom_left = img_cp[hi:i, 0:hj]
    bottom_right = img_cp[hi:i, hj:j]
    iterative_threshold(top_left)
    iterative_threshold(top_right)
    iterative_threshold(bottom_left)
    iterative_threshold(bottom_right)
    return img_cp


# find threshold of image using numpy array masking
def threshold(img, t):
    maska = img < t
    maskb = img >= t
    img[maska] = 1
    img[maskb] = 0
    return img


def driver():
    image = io.imread('../img/hw1.jpg')
    hist = np.histogram(image.ravel(), 256)[0]
    gradient = np.gradient(hist)
    plt.plot(hist)
    plt.plot(gradient)
    plt.show()


if __name__ == '__main__':
    driver()
