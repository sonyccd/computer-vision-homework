from skimage import io, data
import matplotlib.pyplot as plt


def main():
    circle = io.imread('img/cir.gif')
    threshold(circle, 80)
    print(circle.shape)
    print(circle.size)
    print(img_area(circle))
    plt.imshow(circle)
    plt.show()


def threshold(img, t):
    maska = img < t
    maskb = img >= t
    img[maska] = 0
    img[maskb] = 255


def histogram(img):
    plt.subplot(212)
    plt.hist(img.ravel(), bins=256)


def img_area(img):
    area = 0
    for i in img.ravel():
        if i == 255:
            area += 1
    return area


def centroid(img):
    x = 0
    y = 0
    for i in img:
        for j in i:
            x +=


if __name__ == '__main__':
    main()
