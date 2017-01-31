from skimage import io, data
import matplotlib.pyplot as plt


def main():
    teeth = io.imread('img/teeth.jpg')
    threshold(teeth, 80)
    plt.imshow(teeth)
    plt.show()


def threshold(img, t):
    maska = img < t
    maskb = img >= t
    img[maska] = 255
    img[maskb] = 0

if __name__ == '__main__':
    main()
