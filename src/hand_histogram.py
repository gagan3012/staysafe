import cv2
import numpy as np
import pickle


def build_squares(img):
    x, y, w, h = 420, 140, 10, 10
    d = 10
    imgCrop = None
    crop = None
    for i in range(10):
        for j in range(5):
            if np.any(imgCrop == None):
                imgCrop = img[y:y + h, x:x + w]
            else:
                imgCrop = np.hstack((imgCrop, img[y:y + h, x:x + w]))
            # print(imgCrop.shape)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            x += w + d
        if np.any(crop == None):
            crop = imgCrop
        else:
            crop = np.vstack((crop, imgCrop))
        imgCrop = None
        x = 420
        y += h + d
    return crop
