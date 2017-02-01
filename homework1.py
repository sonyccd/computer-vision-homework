from skimage import io, data
import matplotlib.pyplot as plt


def main():
    circle = io.imread('img/cir.gif')
    threshold(circle, 80)
    print("Shape:", circle.shape)
    print("Size:", circle.size)
    print("Image Area:", img_area(circle))
    print("Centroid:", centroid(circle))
    plt.imshow(circle)
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


if __name__ == '__main__':
    main()
