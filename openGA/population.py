"""
population for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import logging
from typing import List
from .individual import Individual

logger = logging.getLogger('openGA')


class Population(object):
    """
    population contain current generation(includes adults, children) and next generateion
    """

    def __init__(self, gen_id: int, size: int, curr_gen: List[Individual]) -> None:
        self._gen_id = gen_id
        self._size = size
        self._curr_gen = curr_gen.copy()
        self._parents = None
        self._children = None
        self._next_gen = None

    @property
    def curr_gen(self):
        return self._curr_gen.copy()

    @property
    def parents(self):
        if self._parents is None:
            raise ValueError('parents not avialable, need select() in prior.')

    @property
    def children(self):
        if self._children is None:
            raise ValueError(
                'children not available, need reproduce() in prior.')
        return self._children.copy()

    @property
    def next_gen(self):
        if self._next_gen is None:
            raise ValueError(
                'next generation not available, need elimate() in prior.')
        return self._next_gen.copy()

