from skimage import io, data
import numpy as np
import matplotlib.pyplot as plt


def main():
    print("Loading image...")
    circle = io.imread('img/cir.gif')
    threshold(circle, 80)
    print("Shape:", circle.shape)
    print("Size:", circle.size)
    print("Image Area:", img_area(circle))
    print("Centroid:", centroid(circle))
    plt.imshow(components(circle))
    plt.show()


# take binary image and set the 1s to 255
# this way you can show the image
def normalize_binary_img(img):
    imgshow = img
    mask = imgshow == 1
    imgshow[mask] = 255
    return imgshow


# find threshold of image using numpy array masking
def threshold(img, t):
    maska = img < t
    maskb = img >= t
    img[maska] = 0
    img[maskb] = 1


# create histogram from image
def histogram(img):
    plt.subplot(212)
    plt.hist(img.ravel(), bins=256)


# fine area of image via raveling
def img_area(img):
    area = 0
    for i in img.ravel():
        if i == 1:
            area += 1
    return area


# find the centroid of entire image
def centroid(img):
    x = 0
    y = 0
    a = img_area(img)
    nrow, ncols = img.shape
    for i in range(nrow):
        for j in range(ncols):
            x += j * img[i][j]
            y += i * img[i][j]
    return x/a, y/a


# TODO need to make sure there is a upper and left pixel
def components(img):
    comps = np.zeros(img.shape)
    nrow, ncols = img.shape
    label = 1
    for i in range(nrow):
        for j in range(ncols):
            if img[i][j] == 1:
                upper = comps[i-1][j]
                left = comps[i][j-1]
                if upper != 0 and left == 0:
                    comps[i][j] = upper
                elif upper == 0 and left != 0:
                    comps[i][j] = left
                elif (upper == left) and (upper != 0) and (left != 0):
                    comps[i][j] = upper
                elif upper != 0 and left != 0:
                    comps[i][j] = upper
                    # TODO add to equivalence table
                else:
                    comps[i][j] = label
                    label += 1
    return comps

if __name__ == '__main__':
    main()
