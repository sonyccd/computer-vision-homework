import math

import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage.draw import polygon_perimeter, circle_perimeter


def main():
    print("Loading image...")
    circles = io.imread('img/bw.jpg')
    print("Shape:", circles.shape)
    print("Size:", circles.size)
    threshold(circles, 128)
    c_img, c_set = components(circles, 20)
    draw_final = equalize(c_img)
    print("Number of components:", len(c_set))
    print("")
    for c in c_set:
        print("Component ID:", c)
        print("Image Area:", img_area(c_img, c))
        center = centroid(c_img, c)
        draw_centroid(draw_final, center)
        print("Centroid:", center)
        bb = bounding_box(c_img, c)
        draw_bounding_box(draw_final, bb)
        print("Boundary Box [row][col]:", bb)
        print("Orientation:", orientation(c_img, c))
        print("Eccentricity:", eccentricity(c_img, c))
        print("")
    plt.imshow(draw_final)
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
    return img


# create histogram from image
def histogram(img):
    plt.subplot(212)
    plt.hist(img.ravel(), bins=256)


# fine area of image via raveling
def img_area(img, component_id):
    area = 0
    for i in img.ravel():
        if i == component_id:
            area += 1
    return area


# find the centroid of entire image
def centroid(img, component_id):
    x = 0
    y = 0
    a = img_area(img, component_id)
    nrow, ncols = img.shape
    for i in range(nrow):
        for j in range(ncols):
            x += j * (1 if img[i][j] == component_id else 0)
            y += i * (1 if img[i][j] == component_id else 0)
    return x / a, y / a


def draw_centroid(img, points):
    rr, cc = circle_perimeter(int(points[1]), int(points[0]), radius=5, shape=img.shape)
    img[rr, cc] = 255
    return img


def components(img, size: int = None):
    comps = np.zeros(img.shape)
    nrow, ncols = img.shape
    label = 1
    labels = Labels()
    set_of_labels = set()
    for i in range(nrow):
        for j in range(ncols):
            if img[i][j] == 1:
                if i == 0 and j == 0:
                    upper = 0
                    left = 0
                else:
                    upper = comps[i - 1][j]
                    left = comps[i][j - 1]

                if upper != 0 and left == 0:
                    comps[i][j] = upper
                elif upper == 0 and left != 0:
                    comps[i][j] = left
                elif upper == left and (upper != 0) and (left != 0):
                    comps[i][j] = upper
                elif (upper != left) and (upper != 0) and (left != 0):
                    comps[i][j] = upper
                    labels.link(max(upper, left), min(upper, left))
                elif upper == 0 and left == 0:
                    comps[i][j] = label
                    labels.add(label)
                    label += 1

    for i in range(nrow):
        for j in range(ncols):
            if comps[i][j] != 0:
                v = labels.root(comps[i][j])
                comps[i][j] = v
                set_of_labels.add(v)
    final_labels = set_of_labels.copy()
    for c in set_of_labels:
        if size is not None:
            if img_area(comps, c) < size:
                mask = comps == c
                comps[mask] = 0
                final_labels.remove(c)
    return comps, final_labels


class Labels:
    def __init__(self):
        self.l = []

    def exists(self, label: int):
        for i in self.l:
            if i.component_id == label:
                return i
        return None

    def add(self, label: int, parent: int = None):
        if self.exists(label) is None:
            self.l.append(Connection(label, self.exists(parent)))

    def link(self, label: int, parent: int):
        self.exists(label).parent = self.exists(parent)

    def root(self, label: int):
        return self.exists(label).root()


class Connection:
    def __init__(self, component_id, parent=None):
        self.component_id = component_id
        self.parent = parent

    def root(self):
        if self.parent is None:
            return self.component_id
        else:
            return self.parent.root()


def equalize(img):
    temp = img.copy()
    unique_values_np = np.unique(temp)
    unique_values = list(unique_values_np)
    unique_values.pop(0)
    eq = np.linspace(25, 200, len(unique_values), dtype=int)
    nrow, ncols = temp.shape
    for i in range(nrow):
        for j in range(ncols):
            if temp[i][j] != 0:
                index = unique_values.index(temp[i][j])
                temp[i][j] = eq[index]
    return temp


def bounding_box(img, component_id):
    nrow, ncols = img.shape
    t = nrow
    b = 0
    l = ncols
    r = 0
    for i in range(nrow):
        for j in range(ncols):
            if img[i][j] == component_id:
                if i < t:
                    t = i
                if j < l:
                    l = j
                if b < i:
                    b = i
                if r < j:
                    r = j
    return [t, b, b, t], [l, l, r, r]


def draw_bounding_box(img, points):
    rr, cc = polygon_perimeter(points[0], points[1], img.shape)
    img[rr, cc] = 255
    return img


# Moore-Neighbor Tracing
def boundary(img, component_id):
    b_pixels = []
    s = None
    p = None
    c = None
    nrow, ncols = img.shape
    for i in range(nrow):
        for j in range(ncols):
            if img[i][j] == component_id and s is None:
                s = (i, j)
                b_pixels.append(s)
                p = s

                break
            else:
                return


def second_moments(img, component_id):
    a = 0
    b = 0
    c = 0
    ic, jc = centroid(img, component_id)
    nrow, ncols = img.shape
    for i in range(nrow):
        for j in range(ncols):
            a += math.pow(i - ic, 2) * (1 if img[i][j] == component_id else 0)
            b += ((i - ic) * (j - jc)) * (1 if img[i][j] == component_id else 0)
            c += math.pow(j - jc, 2) * (1 if img[i][j] == component_id else 0)
    return a, 2 * b, c


def eccentricity(img, component_id):
    a, b, c = second_moments(img, component_id)

    def sin2theta():
        return b / (math.sqrt(math.pow(b, 2) + math.pow((a - c), 2)))

    def cos2theta():
        return (a - c) / (math.sqrt(math.pow(b, 2) + math.pow((a - c), 2)))

    xmin = .5 * (a + c) + .5 * (a - c) * cos2theta() + .5 * b * sin2theta()
    xmax = .5 * (a + c) + .5 * (a - c) * -cos2theta() + .5 * b * -sin2theta()

    return xmax / xmin


def orientation(img, component_id):
    a, b, c = second_moments(img, component_id)
    if a == c:
        return None
    else:
        return 0.5 * math.atan(b / (a - c))


if __name__ == '__main__':
    main()
