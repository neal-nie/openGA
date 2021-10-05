"""
chromosome for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

from __future__ import annotations
import logging
import numpy as np
from typing import Dict, Union, List, Tuple
from .utils import limit, uniform_open, GENE_MIN, GENE_MAX

logger = logging.getLogger('openGA')

GENE_PRECISION = 4


def dist_crossover(r: float, eta: Union[int, float] = 20) -> float:
    """distribution of cross-over coefficiency $\beta$. mean = 1.

    Args:
        r (float): random factor in (0, 1).
        eta (Union[int, float], optional): distribution index. Defaults to 20.

    Returns:
        float: cross-over factor $\beta$
    """
    k = 1 / (eta + 1)
    if r <= 0.5:
        rlt = (2 * r) ** k
    else:
        rlt = (2 * (1 - r)) ** -k
    return rlt


def dist_mutation(r: float, eta: Union[int, float] = 20) -> float:
    """distribution of mutation coefficiency $\theta$. mean = 0.

    Args:
        r (float): random factor in (0, 1).
        eta (Union[int, float], optional): distribution index. Defaults to 20.

    Returns:
        float: mutation factor $\theta$
    """
    k = 1 / (eta + 1)
    if r < 0.5:
        rlt = (2 * r) ** k - 1
    else:
        rlt = 1 - (2 * (1 - r)) ** k
    return rlt


def get_crossover_coef(eta: Union[int, float] = 20) -> float:
    """calc. cross-over coefficiency $\beta$.

    Args:
        eta (Union[int, float], optional): distribution index. Defaults to 20.

    Returns:
        float: cross-over coefficiency.
    """
    u = uniform_open()
    return dist_crossover(u, eta)


def get_mutation_coef(eta: Union[int, float] = 20) -> float:
    """calc. mutation coefficiency $\theta$.

    Args:
        eta (Union[int, float], optional): distribution index. Defaults to 20.

    Returns:
        float: mutation coefficiency.
    """
    u = uniform_open()
    return dist_mutation(u, eta)


class Chromosome(object):
    """
    chromosome with real-number(in [0,1]) encoded genes. 
    """

    def __init__(self, gene_names: List[str], check: bool = True) -> Chromosome:
        """create chromosome.

        Args:
            gene_names (List[str]): list of gene name.
            check (bool, optional): True, check genes couple or not in genetic operation. False, on the contrary. Defaults to True.

        Returns:
            Chromosome: new chromosome object.
        """
        self._check = check
        self._gene_num = len(gene_names)
        self._gene_names = gene_names.copy()
        self._gene_values = np.zeros(self._gene_num)

    def to_dict(self) -> Dict[str, float]:
        """convert chromosome into dict with gene name as key and gene value as dict value.

        Returns:
            Dict[str, float]: chromosome in dict format.
        """
        rlt = {}
        for i in range(self._gene_num):
            rlt[self._gene_names[i]] = self._gene_values[i]
        return rlt

    def __str__(self) -> str:
        return str(self.to_dict())

    def __format__(self, format_spec: str) -> str:
        return str(self)

    def __eq__(self, o: Chromosome) -> bool:
        if self._gene_num != o._gene_num:
            return False
        if self._check != o._check:
            return False
        if self._gene_names != o._gene_names:
            return False
        if np.any(self._gene_values != o._gene_values):
            return False
        return True

    def size(self) -> int:
        """get number of gene in chromosome.

        Returns:
            int: gene number.
        """
        return self._gene_num

    @property
    def check(self) -> bool:
        """check flag of chromosome. 

        Returns:
            bool: True, check couple or not during genetic operation. False, on the contrary.
        """
        return self._check

    @check.setter
    def check(self, active: bool):
        self._check = active

    @property
    def gene_values(self) -> np.ndarray:
        """get a deep copy of gene value in array.

        Returns:
            np.ndarray: gene value array.
        """
        return self._gene_values.copy()

    def update(self, value: float, index: int):
        """update gene value at specific index.

        Args:
            value (float): gene value in [0, 1]
            index (int): index gene, started from ZERO.
        """
        if not GENE_MIN <= value <= GENE_MAX and self._check:
            value_set = limit(value)
            logger.warning(
                'get out of boundary value [%6.4f], limit to [%6.4f]' % (value, value_set))
        else:
            value_set = value
        self._gene_values[index] = round(value_set, GENE_PRECISION)

    def is_couple(self, couple: Chromosome) -> bool:
        """check other chromosome is couple or not.

        Args:
            couple (Chromosome): the other chromosome.

        Returns:
            bool: True, able to generate offspring. False, on the contrary.
        """
        if self._gene_num != couple._gene_num:
            logger.info('Not couple for unbalance gene number')
            return False
        for i in range(self._gene_num):
            if self._gene_names[i] != couple._gene_names[i]:
                logger.info('Not couple for unmatch gene name at [%d]: [%s]-[%s]' % (
                    i, self._gene_names[i], couple._gene_names[i]))
                return False
        return True

    def random(self, inplace=False) -> Chromosome:
        """randomize gene value of chromosome.

        Args:
            inplace (bool, optional): True, `this` chromosome will be randomized. False, `this` one stay the same. Defaults to False.

        Returns:
            Chromosome: randomized chromosome object.
        """
        mock = self.copy()
        for i in range(mock._gene_num):
            val = np.random.uniform(GENE_MIN, GENE_MAX)
            val = round(val, GENE_PRECISION)
            mock.update(val, i)
            if inplace:
                self.update(val, i)
        return mock

    def crossover(self, couple: Chromosome, eta: Union[int, float] = 20) -> Tuple[Chromosome, Chromosome]:
        """generate offspring with cross-over operation.

        Args:
            couple (Chromosome): couple chromosome.
            eta (Union[int, float], optional): cross-over coefficiency distribution index. Defaults to 20.

        Raises:
            ValueError: if couple check failed, raise ValueError with message of `couple unmatch, can not crossover`.

        Returns:
            Tuple[Chromosome, Chromosome]: offspring chromosomes.
        """
        if self._check:
            if not self.is_couple(couple):
                raise ValueError('couple unmatch, can not crossover')
        offspring_0 = Chromosome(self._gene_names, self._check)
        offspring_1 = Chromosome(self._gene_names, self._check)
        for i in range(self._gene_num):
            p0_gene_val = self._gene_values[i]
            p1_gene_val = couple.gene_values[i]
            beta = get_crossover_coef(eta)
            a = 1 - beta
            b = 1 + beta
            c0_gene_val = limit(0.5 * (a * p0_gene_val + b * p1_gene_val))
            c1_gene_val = limit(0.5 * (b * p0_gene_val + a * p1_gene_val))
            offspring_0.update(c0_gene_val, i)
            offspring_1.update(c1_gene_val, i)
        return offspring_0, offspring_1

    def mutate(self, eta: Union[int, float] = 20) -> Chromosome:
        """generate offspring with mutation operation.

        Args:
            eta (Union[int, float], optional): mutation coefficiency distribution index. Defaults to 20.

        Returns:
            Chromosome: offspring chromosome.
        """
        offspring = Chromosome(self._gene_names)
        for i in range(self._gene_num):
            p_gene_val = self._gene_values[i]
            theta = get_mutation_coef(eta)
            c_gene_val = limit(p_gene_val + theta)
            offspring.update(c_gene_val, i)
        return offspring

    def copy(self) -> Chromosome:
        """create deep copy of `this` chromosome.

        Returns:
            Chromosome: cloned chromosome.
        """
        twin = Chromosome(self._gene_names, self._check)
        for i in range(self._gene_num):
            twin.update(self._gene_values[i], i)
        return twin
