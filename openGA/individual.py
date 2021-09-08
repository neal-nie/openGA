"""
individual for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import logging
from typing import List
from .chromosome import Chromosome

logger = logging.getLogger('openGA')


class Individual(object):
    """
    individual carray chromosomes, express feature and show fittness.
    """

    def __init__(self, gen_id: int, idv_id: int, gene_names: List[str], check:bool=True) -> None:
        self._check = check
        self._gen_id = gen_id
        self._idv_id = idv_id
        self._fittness = None
        self._plasm = Chromosome(gene_names, self._check)

    @property
    def fittness(self):
        if self._fittness is None:
            raise ValueError('fittness not available, need evaluate in prior.')
        return self._fittness
    
    def is_growup(self):
        return not self._fittness is None

    @property
    def plasm(self):
        return self._plasm.copy()

    @plasm.setter
    def plasm(self, info: Chromosome):
        if self._check:
            if not self._plasm.is_couple(info):
                raise ValueError('can not extract info for mismatch chromosome')
        for i in range(self._plasm._gene_num):
            self._plasm._update(info.gene_values[i], i)

    def _express(self):
        raise NotImplementedError(
            'express() of Individual need to implement by monkey patch')

    def evaluate(self):
        raise NotImplementedError(
            'evaluate() of Individual need to implement by monkey patch')

    def copy(self):
        twin = Individual(self._gen_id, self._idv_id, self._plasm._gene_names, self._check)
        for i in range(self._plasm._gene_num):
            twin._plasm._update(self._plasm.gene_values[i], i)
        return twin