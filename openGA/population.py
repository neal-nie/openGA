"""
population for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import logging
import numpy as np
from typing import List
from .individual import Individual

logger = logging.getLogger('openGA')
CHILD_ID_OFFSET = 1000

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

    @staticmethod
    def _evaluate(group: List[Individual]):
        for persone in group:
            if not persone.is_growup():
                persone.evaluate()

    def select(self, pool_size: int = None, tour_size: int = 2):
        if pool_size is None:
            pool_size = int(self._size/2)
        # evaluate parents
        self._evaluate(self._curr_gen)
        parents_idx_list = []
        for _ in range(pool_size):
            # select candidates
            candidate_idx_set = set()
            for j in range(tour_size):
                while not len(candidate_idx_set) > j:
                    rnd_idx = np.random.randint(0, self._size)
                    if rnd_idx not in parents_idx_list:
                        candidate_idx_set.add(rnd_idx)
            # candidates compete
            parent_idx = None
            for candidate_idx in candidate_idx_set:
                if parent_idx is None:
                    parent_idx = candidate_idx
                    continue
                if self._curr_gen[parent_idx].fittness < self._curr_gen[candidate_idx]:
                    parent_idx = candidate_idx
            parents_idx_list.append(parent_idx)
        self._parents = []
        for i in parents_idx_list:
            self._parents.append(self._curr_gen[i])

    def reproduce(self, cross_prob: float = 0.9):
        if not 0 <= cross_prob <= 1:
            raise ValueError(
                'invalid cross_prob. Must in [0,1], got %6.4f' % cross_prob)

        self._children = []
        n_parents = len(self._parents)
        for i in range(n_parents):
            if np.random.uniform(0, 1) < cross_prob:
                # select parents
                p0_idx = np.random.randint(0, n_parents)
                p1_idx = p0_idx
                while p1_idx == p0_idx:
                    p1_idx = np.random.randint(0, n_parents)
                
                # sexual produce
                c0, c1 = self._parents[p0_idx].sexual_reproduce(self._parents[p1_idx])
                c0.idv_id = CHILD_ID_OFFSET + i
                c1.idv_id = CHILD_ID_OFFSET + i + 1
                self._children.append(c0)
                self._children.append(c1)
        # evaluate children
        self._evaluate(self._children)

