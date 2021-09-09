"""
individual for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import logging
import numpy as np
from typing import List, Tuple, Union
from .chromosome import Chromosome

logger = logging.getLogger('openGA')


class Individual(object):
    """
    individual carray chromosomes, express feature and show fittness.
    """

    def __init__(self, gen_id: int, idv_id: int, gene_names: List[str], check: bool = True) -> None:
        self._check = check
        self._gen_id = gen_id
        self._idv_id = idv_id
        self._fittness = None
        self._plasm = Chromosome(gene_names, self._check)

    @property
    def idv_id(self):
        return self._idv_id

    @idv_id.setter
    def idv_id(self, id: int):
        self._idv_id = id

    @property
    def fittness(self) -> Union[None, float]:
        if self._fittness is None:
            raise ValueError('fittness not available, need evaluate in prior.')
        return self._fittness

    def is_growup(self) -> bool:
        return not self._fittness is None

    @property
    def plasm(self) -> Chromosome:
        return self._plasm.copy()

    @plasm.setter
    def plasm(self, info: Chromosome):
        if self._check:
            if not self._plasm.is_couple(info):
                raise ValueError(
                    'can not extract info for mismatch chromosome')
        for i in range(self._plasm._gene_num):
            self._plasm._update(info.gene_values[i], i)

    def _express(self):
        raise NotImplementedError(
            'express() of Individual need to implement by monkey patch')

    def evaluate(self):
        raise NotImplementedError(
            'evaluate() of Individual need to implement by monkey patch')

    def copy(self) -> Individual:
        twin = Individual(self._gen_id, self._idv_id,
                          self._plasm._gene_names, self._check)
        for i in range(self._plasm._gene_num):
            twin._plasm._update(self._plasm.gene_values[i], i)
        return twin

    def sexual_reproduce(self, couple: Individual, p_mutation: float = 0.05) -> Tuple(Individual, Individual):
        offspring_0 = self.copy()
        offspring_1 = couple.copy()
        plasm_0, plasm_1 = self.plasm.crossover(couple.plasm)
        
        if np.random.uniform() < p_mutation:
            plasm_0 = plasm_0.mutate()
        if np.random.uniform() < p_mutation:
            plasm_1 = plasm_1.mutate()
        
        offspring_0.plasm = plasm_0
        offspring_1.plasm = plasm_1

        return offspring_0, offspring_1

