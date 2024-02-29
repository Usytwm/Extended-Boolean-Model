import numpy as np


class BEM:
    def __init__(self) -> None:
        pass

    # Funciones de similitud
    def sim_or(self, weights, p=2):
        return np.power(np.sum(np.power(weights, p)) / len(weights), 1 / p)

    def sim_and(self, weights, p=2):
        return 1 - np.power(np.sum(np.power(1 - weights, p)) / len(weights), 1 / p)
