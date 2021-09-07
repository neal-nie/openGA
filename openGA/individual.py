"""
individual for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import logging
import numpy as np
from typing import Protocol, Union, List, Tuple
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
        self._fittness = 0
        self._plasm = Chromosome(gene_names, self._check)

    @property
    def plasm(self):
        return self._plasm

    @plasm.setter
    def plasm(self, info: Chromosome):
        if self._check:
            if not self._plasm.is_couple(info):
                raise ValueError('can not extract info for mismatch chromosome')
        for i in range(self._plasm._gene_num):
            self._plasm._update(info.gene_values[i], i)

    def express(self):
        raise NotImplementedError(
            'express() of Individual need to implement by monkey patch')

    def evaluate(self):
        raise NotImplementedError(
            'evaluate() of Individual need to implement by monkey patch')
