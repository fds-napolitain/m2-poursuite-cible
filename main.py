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
        self.index = 0 # index des frames
        self.target_pixels = []
        self.reload()
        cv2.setMouseCallback("Poursuite de cible", self.create_target)

    def reload(self):
        """
        Met à jour l'image, avec la frame suivante, et met à jour l'index de la prochaine
        :return:
        """
        self.img = cv2.imread(os.path.join(self.folder, self.img_path[self.index]))  # img left
        cv2.imshow("Poursuite de cible", self.img)
        self.index = (self.index + 1) % len(self.img_path)

    def create_target(self, event, x, y, flags, param):
        """
        Select pixel on both images (same coordinates)
        :param event: click listener
        :param x: x coordinate
        :param y: y coordinate
        :param flags: useless
        :param param: useless
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.target_pixels) < 2: # tant qu'on a pas 2 points
                self.target_pixels.append((x, y))
                if len(self.target_pixels) == 2: # 2 points: rectangle
                    print(self.target_pixels)
                    self.target_img = self.img[
                        self.target_pixels[0][1]:self.target_pixels[1][1],
                        self.target_pixels[0][0]:self.target_pixels[1][0]
                    ]
                    cv2.imshow("Cible", self.target_img)
                    self.target_pixels.clear()


poursuite = Poursuite("SequenceSansVariation")
while True:
    key = cv2.waitKey(40) # 25 fps
    if key == 27: # esc
        cv2.destroyAllWindows()
    elif key == 32: # space
        poursuite.reload()
