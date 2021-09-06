"""
chromosome for genetic algorithm
"""
import logging
import numpy as np
from typing import Union, List, Tuple
from .utils import limit

logger = logging.getLogger('openGA')


def get_crossover_coef(eta: Union[int, float] = 20) -> float:
    u = np.random.uniform()
    k = 1 / (eta + 1)
    if u <= 0.5:
        rlt = (2 * u) ** k
    else:
        rlt = (2 * (1 - u)) ** -k
    return rlt


def get_mutation_coef(eta: Union[int, float] = 20) -> float:
    u = np.random.uniform()
    k = 1 / (eta + 1)
    if u < 0.5:
        rlt = (2 * u) ** k - 1
    else:
        rlt = 1 - (2 * (1 - u)) ** k
    return rlt


class Chromosome(object):
    """
    create chromosome with gene in [0,1]
    """

    def __init__(self, gene_names: List[str]) -> None:
        self._gene_num = len(gene_names)
        self._gene_names = gene_names.copy()
        self._gene_values = np.zeros(self._gene_num)

    @property
    def gene_values(self):
        return self._gene_values.copy()

    def _update(self, value: float, index: int):
        self._gene_values[index] = value

    def crossover(self, couple: Chromosome, eta: Union[int, float] = 20) -> Tuple[Chromosome, Chromosome]:
        offspring_0 = Chromosome(self._gene_names)
        offspring_1 = Chromosome(self._gene_names)
        for i in range(self._gene_num):
            p0_gene_val = self._gene_values[i]
            p1_gene_val = couple.gene_values[i]
            beta = get_crossover_coef(eta)
            a = 1 - beta
            b = 1 + beta
            c0_gene_val = limit(0.5 * (a * p0_gene_val + b * p1_gene_val))
            c1_gene_val = limit(0.5 * (b * p0_gene_val + a * p1_gene_val))
            offspring_0._update(c0_gene_val, i)
            offspring_1._update(c1_gene_val, i)
        return offspring_0, offspring_1

    def mutate(self, eta: Union[int, float] = 20) -> Chromosome:
        offspring = Chromosome(self._gene_names)
        for i in range(self._gene_num):
            p_gene_val = self._gene_values[i]
            theta = get_mutation_coef(eta)
            c_gene_val = limit(p_gene_val + theta)
            offspring._update(c_gene_val, i)
        return offspring
