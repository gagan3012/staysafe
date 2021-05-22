import cv2
import numpy as np
import pickle, os, sqlite3, random

image_x, image_y = 50, 50


def get_hand_hist():
    with open("hist", "rb") as f:
        hist = pickle.load(f)
    return hist
