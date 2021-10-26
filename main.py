import os
import cv2
import numpy as np


class Poursuite:
    def __init__(self, folder):
        """
        Construct a flux of images with the intention of tracking points on different frames
        :param img_path: path to folder of images
        """
        self.folder = folder
        self.img_path = os.listdir(folder)  # path, window name
        self.img_path.sort()
        self.index = 0
        self.reload()

    def reload(self):
        self.img = cv2.imread(os.path.join(self.folder, self.img_path[self.index]))  # img left
        cv2.imshow("Poursuite d'image", self.img)
        self.index = (self.index + 1) % len(self.img_path)


poursuite = Poursuite("SequenceSansVariation")
while True:
    key = cv2.waitKey(40) # 25 fps
    if key == 27: # esc
        cv2.destroyAllWindows()
    elif key == 32: # space
        poursuite.reload()
