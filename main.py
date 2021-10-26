import os
import cv2


class Poursuite:
    def __init__(self, folder):
        """
        Construct a flux of images with the intention of tracking points on different frames
        :param img_path: path to folder of images
        """
        self.folder = folder
        self.img_path = os.listdir(folder)  # path, window name
        self.img_path.sort()
        self.index = 0  # index des frames
        self.target_pixels = []
        self.img = cv2.imread(os.path.join(self.folder, self.img_path[self.index]))  # img left
        self.height, self.width, self.depth = self.img.shape
        self.target_img = 0
        self.target_height, target_width, target_depth = 0
        self.reload()
        cv2.setMouseCallback("Poursuite de cible", self.create_target)

    def reload(self):
        """
        Met à jour l'image, avec la frame suivante, et met à jour l'index de la prochaine
        :return:
        """
        self.img = cv2.imread(os.path.join(self.folder, self.img_path[self.index]))  # img left
        self.find_area()
        cv2.imshow("Poursuite de cible", self.img)
        self.index = (self.index + 1) % len(self.img_path)

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
                    print(self.target_pixels)
                    self.target_img = self.img[
                        self.target_pixels[0][1]:self.target_pixels[1][1],
                        self.target_pixels[0][0]:self.target_pixels[1][0]
                    ]
                    self.target_height, target_width, target_depth = self.target_img.shape
                    cv2.imshow("Cible", self.target_img)
                    cv2.rectangle(self.img, self.target_pixels[0], self.target_pixels[1], (0, 0, 255), 2)
                    cv2.imshow("Poursuite de cible", self.img)
            else:
                self.target_pixels.clear()

    def correlation_pearson(self, img2):
        """
        Doit retourner un coefficient de corrélation entre deux images
        À appliquer sur toutes les images segmentant l'image I, de même taille que l'image cible.
        :param img2 image to compare target with
        :return:
        """
        mean_img1 = self.target_img.mean()
        mean_img2 = img2.mean()
        var_img1 = self.target_img.var()
        var_img2 = img2.var()
        return ((self.target_img - mean_img1).sum() * (img2 - mean_img2).sum()) / (var_img1 * var_img2) ** 0.5

    def find_area(self):
        """
        Doit montrer (rectangle rouge) la zone trouvée correspondante au plus haute coefficient
        de corrélation de Pearson.
        :return:
        """


poursuite = Poursuite("SequenceSansVariation")
while True:
    key = cv2.waitKey(40)  # 25 fps
    if key == 27:  # esc
        cv2.destroyAllWindows()
    elif key == 32:  # space
        poursuite.reload()
