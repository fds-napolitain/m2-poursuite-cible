import math
from algos.motifs.AbstractArea import AbstractArea


class SSD(AbstractArea):
    """
    Configuration de l'algorithme par des écarts quadratiques.
    """

    def __init__(self):
        self.best_starting_point = math.inf

    def compare_with(self, x, best_x):
        return x < best_x

    def evaluate(self, target_img, comparison_img, normalized=False):
        """
        Retourne la somme des écarts quadratiques des distances entre deux images
        :return:
        """
        return pow(target_img - comparison_img, 2).mean()
