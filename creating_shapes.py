import cv2
import numpy as np
from random import random, randint, shuffle
from scipy import ndimage
import os
import time
import string
import shutil


def convert_bg_fg(img):
    rn_color_fg = (randint(0, 256), randint(0, 256), randint(0, 256))
    rn_color_bg = (randint(0, 256), randint(0, 256), randint(0, 256))
    x = np.full(shape=(img.shape[0], img.shape[1], 3), fill_value=0, dtype=np.uint8)
    for z in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[z, j] == 0:
                x[z, j] = rn_color_bg
            else:
                x[z, j] = rn_color_fg

    return x


def apply_transformation(img):
    img = ndimage.rotate(img, randint(-360, 345))
    affine_matrix = np.float32([[1, 0, randint(0, 50)], [0, 1, randint(0, 50)]])
    x = ndimage.affine_transform(img, matrix=affine_matrix)
    blur = cv2.erode(x, np.ones((3, 3), np.uint8), iterations=2)
    y = convert_bg_fg(blur)
    return cv2.resize(y, (150, 150))


def random_file_genartor():
    return "".join([string.ascii_letters[randint(0, 50)]
                    for x in range(randint(5, 15))]) + str(randint(0, 100000))


def create_dict(dict_name):
    try:
        os.mkdir(dict_name)
    except FileExistsError:
        shutil.rmtree(dict_name)
        os.mkdir(dict_name)
    print("We have created a dictionary called", dict_name)


def main():
    array_pic = []
    parent_name = "shapes"
    shapes = os.listdir("shapes")
    for i in shapes:
        shape_path = os.path.join(parent_name, i)
        shape_path_dir = os.listdir(shape_path)
        create_dict(i.capitalize())
        for j in shape_path_dir:
            pic_path = os.path.join(shape_path, j)
            pic = cv2.resize(cv2.imread(pic_path, 0), (250, 250))
            thresh = cv2.threshold(pic, 1, 255, cv2.THRESH_BINARY_INV)[1]
            array_pic.append([thresh, i])

    count = 0
    for i in array_pic:
        print("We are starting with ")
        start = time.time()
        for j in range(1000):
            img_copy = i[0].copy()
            shape_transformed = apply_transformation(img_copy)
            file_name = os.path.join(i[1].capitalize(),
                                     f"{i[1].capitalize()}_{j}{count}{random_file_genartor()}.png")
            print(file_name)
            cv2.imwrite(file_name, shape_transformed)
            img_copy = None
        print("Time to process 100 images", time.time() - start)
        count += 1


if __name__ == "__main__":
    main()