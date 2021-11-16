import math
from algos.motifs.AbstractArea import AbstractArea


class SAD(AbstractArea):
    """
    Configuration de l'algorithme par somme absolue des distances.
    """

    def __init__(self):
        self.best_starting_point = math.inf

    def compare_with(self, x, best_x):
        return x < best_x

    def evaluate(self, target_img, comparison_img, normalized=False):
        """
        Retourne la somme absolue des distances entre deux images
        :return:
        """
        return abs(target_img - comparison_img).mean()
