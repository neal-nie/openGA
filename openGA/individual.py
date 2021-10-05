"""
individual for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

from __future__ import annotations
import logging
import numpy as np
from typing import Dict, List, Tuple, Union
from .chromosome import Chromosome

logger = logging.getLogger('openGA')


class Individual(object):
    """
    individual to carry chromosomes, express feature and show fitness.
    """

    def __init__(self, plasm: Chromosome) -> Individual:
        """create individual.

        Args:
            plasm (Chromosome): chromosome carried by individual.

        Returns:
            Individual: new individual object.
        """
        self._gen_id = -1
        self._idv_id = -1
        self._fitness = None
        self._plasm = plasm.copy()
        self._check = self._plasm.check

    def to_dict(self, default_fit: float = np.nan) -> Dict[str, float]:
        """convert individual into dict with `gen_id`, `idv_id`, `fitness` and ${gene_names} of plasm as keys.

        Args:
            default_fit (float, optional): default value for fitness when indvidual not grow-up. Defaults to np.nan.

        Returns:
            Dict[str, float]: individual in dict format.
        """
        rlt = {}
        rlt['gen_id'] = self._gen_id
        rlt['idv_id'] = self._idv_id
        rlt['fitness'] = default_fit if self._fitness is None else self._fitness
        rlt.update(self._plasm.to_dict())
        return rlt

    def __str__(self) -> str:
        return f"person({self._gen_id:d}, {self._idv_id:d}): [{self._fitness}] {self._plasm}"

    def __format__(self, format_spec: str) -> str:
        return str(self)

    @property
    def gen_id(self) -> int:
        """get generate id of `this` individual.

        Returns:
            int: generate id.
        """
        return self._gen_id

    @gen_id.setter
    def gen_id(self, gen: int):
        self._gen_id = gen

    @property
    def idv_id(self) -> int:
        """get individual id of `this` individual.

        Returns:
            int: individual id.
        """
        return self._idv_id

    @idv_id.setter
    def idv_id(self, id: int):
        self._idv_id = id

    @property
    def fitness(self) -> float:
        """get fitness value of `this` individual.

        Raises:
            ValueError: error message of `fitness not available, need evaluate in prior.` when individual not grow-up.

        Returns:
            float: fitness value.
        """
        if self._fitness is None:
            raise ValueError('fitness not available, need evaluate in prior.')
        return self._fitness

    def is_growup(self) -> bool:
        """get grow-up flag of `this` individual.

        Returns:
            bool: True, fitness is updated. False, fitness is None.
        """
        return not self._fitness is None

    @property
    def plasm(self) -> Chromosome:
        """get a deep copy of plasm of `this` individual.

        Returns:
            Chromosome: deep copy of plasm.
        """
        return self._plasm.copy()

    @plasm.setter
    def plasm(self, info: Chromosome):
        if self._check:
            if not self._plasm.is_couple(info):
                raise ValueError(
                    'can not extract info for mismatch chromosome')
        for i in range(self._plasm._gene_num):
            self._plasm.update(info.gene_values[i], i)

    def express(self):
        """express individual's plasm into feature. Need monkey path in prior to be called.
        """
        raise NotImplementedError(
            'express() of Individual need to implement by monkey patch')

    def evaluate(self):
        """evaluate individual's fitness. Need monkey path in prior to be called.
        """
        raise NotImplementedError(
            'evaluate() of Individual need to implement by monkey patch')

    def copy(self) -> Individual:
        """create a deep copy of `this` individual.

        Returns:
            Individual: clone of `this` individual.
        """
        clone = Individual(self._plasm)
        for i in range(self._plasm._gene_num):
            clone._plasm.update(self._plasm.gene_values[i], i)
        clone.gen_id = self._gen_id
        clone.idv_id = self._idv_id
        return clone

    def sexual_reproduce(self, couple: Individual, p_mutation: float = 0.05) -> Tuple[Individual, Individual]:
        """generate offspring individual with the other individual by cross-over and mutation.

        Args:
            couple (Individual): the other individual for mating.
            p_mutation (float, optional): probability of mutation. Defaults to 0.05.

        Returns:
            Tuple[Individual, Individual]: offspring individuals.
        """
        offspring_0 = self.copy()
        offspring_1 = couple.copy()
        plasm_0, plasm_1 = self._plasm.crossover(couple._plasm)
        if np.random.uniform() < p_mutation:
            plasm_0 = plasm_0.mutate()
        if np.random.uniform() < p_mutation:
            plasm_1 = plasm_1.mutate()
        offspring_0.plasm = plasm_0
        offspring_1.plasm = plasm_1

        return offspring_0, offspring_1

    def asexual_reproduce(self, p_mutation: float = 0.1) -> Individual:
        """generate offspring individual by `this` individual itself with clone and mutation.

        Args:
            p_mutation (float, optional): probability of mutation. Defaults to 0.1.

        Returns:
            Individual: offspring individual.
        """
        offspring = self.copy()
        if np.random.uniform() < p_mutation:
            plasm = self._plasm.mutate()
            offspring.plasm = plasm
        return offspring
