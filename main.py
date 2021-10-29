"""
Poursuite de cible
- méthode par corrélation de Pearson, par bloc
- méthode par flot optique
"""
import math
import os
from cv2 import cv2


class Poursuite:
    def __init__(self, folder):
        """
        Construct a flux of images with the intention of tracking points on different frames
        :param img_path: path to folder of images
        """
        self.folder = folder
        self.img_path = os.listdir("sequences/" + folder)  # path, window name
        self.img_path.sort()
        self.index = 0  # index des frames
        self.target_pixels = []
        self.target_pixels_saved = [[0,0], [0,0]]
        self.img = cv2.imread(os.path.join("sequences/" + self.folder, self.img_path[self.index]))
        self.height, self.width, self.depth = self.img.shape
        self.target_img = None
        self.target_height, self.target_width, self.target_depth = [0, 0, 0]
        self.reload()
        cv2.setMouseCallback(folder, self.create_target)

    def reload(self):
        """
        Met à jour l'image, avec la frame suivante, et met à jour l'index de la prochaine
        :return:
        """
        self.img = cv2.imread(os.path.join("sequences/" + self.folder, self.img_path[self.index]))
        if len(self.target_pixels) == 2:
            self.find_area_pearson()
        cv2.imshow(self.folder, self.img)
        self.index += 1
        if self.index % len(self.img_path) == 0:
            self.index %= len(self.img_path)
            self.target_pixels = [
                [
                    self.target_pixels_saved[0][0],
                    self.target_pixels_saved[0][1]
                ],
                [
                    self.target_pixels_saved[1][0],
                    self.target_pixels_saved[1][1]
                ]
            ]

    def create_target(self, event, x, y, flags, param):
        """
        Create crop of image, which is target to track
        :param event: click listener
        :param x: x coordinate
        :param y: y coordinate
        :param flags: useless
        :param param: useless
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.target_pixels) < 2:  # tant qu'on a pas 2 points
                self.target_pixels.append((x, y))
                if len(self.target_pixels) == 2:  # 2 points: rectangle
                    self.target_pixels_saved = [
                        [
                            self.target_pixels[0][0],
                            self.target_pixels[0][1]
                        ],
                        [
                            self.target_pixels[1][0],
                            self.target_pixels[1][1]
                        ]
                    ]
                    self.target_img = self.img[
                                      self.target_pixels[0][1]:self.target_pixels[1][1],
                                      self.target_pixels[0][0]:self.target_pixels[1][0]
                                      ]
                    self.target_height, self.target_width, self.target_depth = self.target_img.shape
                    cv2.imshow(self.folder + ": cible", self.target_img)
                    cv2.rectangle(self.img, self.target_pixels[0], self.target_pixels[1], (0, 0, 255), 2)
                    cv2.imshow(self.folder, self.img)
                    print("target: " + str(self.target_pixels))
            else:
                self.target_pixels.clear()

    def correlation_pearson(self, img2):
        """
        Doit retourner un coefficient de corrélation entre deux images
        À appliquer sur toutes les images segmentant l'image I, de même taille que l'image cible.
        :param img2 image to compare target with
        :return: Between -1 and 1
        """
        mean_img1 = self.target_img.mean()
        mean_img2 = img2.mean()
        var_img1 = self.target_img.var()
        var_img2 = img2.var()
        return ((self.target_img - mean_img1).sum() * (img2 - mean_img2).sum()) / ((var_img1 * var_img2) ** 0.5)

    def dist_SAD(self, img2):
        """
        Retourne la somme absolue des distances entre deux images
        :return:
        """
        return abs(self.target_img - img2).mean()

    def dist_SSD(self, img2):
        """
        Retourne la somme des écarts quadratiques des distances entre deux images
        :return:
        """
        return pow(self.target_img - img2, 2).mean()

    def find_area_pearson(self):
        """
        Doit montrer (rectangle rouge) la zone trouvée correspondante au plus haute coefficient
        de corrélation de Pearson.
        :return:
        """
        tmp = [ # zone de recherche, a diminuer avec plusieurs itérations
            [
                max(self.target_pixels[0][0]-int(self.width/10),0),
                max(self.target_pixels[0][1]-int(self.height/10),0)
            ]
        ]
        tmp.append([tmp[0][0]+self.target_width, tmp[0][1]+self.target_height])
        best_x = math.inf # algorithme de recherche par distance/bloc
        best_tmp: list
        while tmp[1][1] < min(self.target_pixels[1][1]+int(self.height/10),self.height):
            while tmp[1][0] < min(self.target_pixels[1][0]+int(self.width/10),self.width):
                x = self.dist_SSD(self.img[tmp[0][1]:tmp[1][1],tmp[0][0]:tmp[1][0]])
                if x < best_x:
                    best_tmp = [[tmp[0][0], tmp[0][1]], [tmp[1][0], tmp[1][1]]]
                    best_x = x
                tmp[0][0] += round(self.target_width / 50)
                tmp[1][0] += round(self.target_width / 50)
            tmp[0][0] = max(self.target_pixels[0][0]-int(self.width/10),0)
            tmp[1][0] = tmp[0][0]+self.target_width
            tmp[0][1] += round(self.target_height / 50)
            tmp[1][1] += round(self.target_height / 50)
        cv2.rectangle(self.img, best_tmp[0], best_tmp[1], (0, 0, 255), 2)
        self.target_pixels = [[x,y] for [x,y] in best_tmp]
        return best_x


poursuite = Poursuite("Ghost3")
while True:
    key = cv2.waitKey(40)  # 25 fps
    if key == 27:  # esc
        cv2.destroyAllWindows()
        exit(0)
    elif key == 32:  # space
        poursuite.reload()
