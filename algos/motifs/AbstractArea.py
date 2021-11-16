from abc import ABC, abstractmethod


class AbstractArea(ABC):
    """
    Classe abstraite qui sera implémenté par Pearson, SAD, SSD.
    """

    @abstractmethod
    def compare_with(self, x, best_x):
        pass

    @abstractmethod
    def evaluate(self, target_img, comparison_img, normalized=False):
        pass
