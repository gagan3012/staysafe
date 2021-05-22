import cv2
from glob import glob
import numpy as np
import random
from sklearn.utils import shuffle
import pickle
import os

def pickle_images_labels():
	images_labels = []
	images = glob("gestures/*/*.jpg")
	images.sort()
	for image in images:
		print(image)
		label = image[image.find(os.sep)+1: image.rfind(os.sep)]
		img = cv2.imread(image, 0)
		images_labels.append((np.array(img, dtype=np.uint8), int(label)))
	return images_labels
