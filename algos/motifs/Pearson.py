from algos.motifs.AbstractArea import AbstractArea


class Pearson(AbstractArea):
    """
    Configuration de l'algorithme de corrélation de Pearson
    """

    def __init__(self):
        self.best_starting_point = 0

    def compare_with(self, x, best_x):
        return x > best_x

    def evaluate(self, target_img, comparison_img, normalized=False):
        """
        Doit retourner un coefficient de corrélation entre deux images
        À appliquer sur toutes les images segmentant l'image I, de même taille que l'image cible.
        :param target_img:
        :param comparison_img image to compare target with
        :param normalized:
        :return: Between -1 and 1
        """
        if not normalized:
            return (target_img*comparison_img).mean()
        else:
            mean_target_img = target_img.mean()
            mean_comparison_img = comparison_img.mean()
            var_target_img = target_img.var()
            var_comparison_img = comparison_img.var()
            # img - mean_img -> applique pour chaque pixel p € I: p = p - moyenne(I)
            return (target_img - mean_target_img) * (comparison_img - mean_comparison_img)

