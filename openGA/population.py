"""
population for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

from __future__ import annotations
import logging
import numpy as np
import pandas as pd
from typing import List, Union
from copy import deepcopy
from .individual import Individual

logger = logging.getLogger('openGA')


class Population(object):
    """
    population contains individuals of current generation(includes adults, children) and next generation.
    """

    def __init__(self, gen_id: int, curr_gen: List[Individual], capacity: int = 20) -> Population:
        """create population.

        Args:
            gen_id (int): generate id of current generation.
            curr_gen (List[Individual]): list of individual of current generation.
            capacity (int, optional): max individual could live in environment. Defaults to 20.

        Returns:
            Population: new population object.
        """
        self._capacity = capacity
        self._gen_id = gen_id
        self._size = len(curr_gen)
        self._curr_gen = deepcopy(curr_gen)
        self._parents = []
        self._children = []
        self._next_gen = []
        for i in range(self._size):
            self._curr_gen[i].gen_id = gen_id
            self._curr_gen[i].idv_id = i

    def to_df(self, default_fit: float = np.nan) -> pd.DataFrame:
        """convert population into dataframe with row of each individual of current generation.

        Args:
            default_fit (float, optional): default value for fitness when individual not grow-up. Defaults to np.nan.

        Returns:
            pd.DataFrame: population in dataframe format.
        """
        l = []
        for p in self._curr_gen:
            l.append(p.to_dict(default_fit=default_fit))
        rlt = pd.DataFrame(l)
        return rlt

    def __str__(self) -> str:
        rlt_str = f"population({self._size:d}/{self._capacity}):\n"
        rlt_str += f"current generation @{self._gen_id:d}:\n"
        for p in self._curr_gen:
            rlt_str += f"{p}\n"
        rlt_str += f"parents [{len(self._parents):d}]:\n"
        for p in self._parents:
            rlt_str += f"{p}\n"
        rlt_str += f"children [{len(self._children):d}]:\n"
        for p in self._children:
            rlt_str += f"{p}\n"
        rlt_str += f"next generation [{len(self._next_gen):d}]:\n"
        for p in self._next_gen:
            rlt_str += f"{p}\n"
        return rlt_str

    def __format__(self, format_spec: str) -> str:
        return str(self)

    @property
    def gen_id(self) -> int:
        """get generate id of `this` individual.

        Returns:
            int: generate id.
        """
        return self._gen_id

    @property
    def curr_gen(self) -> List[Individual]:
        """get shallow copy of individuals in current generation.

        Returns:
            List[Individual]: list of individuals.
        """
        return self._curr_gen.copy()

    @property
    def parents(self) -> List[Individual]:
        """get shallow copy of parent individuals.

        Raises:
            ValueError: error message of `parents not avialable, need select() in prior.`.

        Returns:
            List[Individual]: list of parent individuals.
        """
        if not self._parents:
            raise ValueError('parents not avialable, need select() in prior.')
        return self._parents.copy()

    @property
    def children(self) -> List[Individual]:
        """get shallow copy of children individuals.

        Raises:
            ValueError: error message of `children not available, need reproduce() in prior.`.

        Returns:
            List[Individual]: list of children individuals.
        """
        if not self._children:
            raise ValueError(
                'children not available, need reproduce() in prior.')
        return self._children.copy()

    @property
    def next_gen(self) -> List[Individual]:
        """get shallow copy of individuals in next generation.

        Raises:
            ValueError: error message of `next generation not available, need elimate() in prior.`.

        Returns:
            List[Individual]: list of individuals in next generation.
        """
        if not self._next_gen:
            raise ValueError(
                'next generation not available, need elimate() in prior.')
        return self._next_gen.copy()

    @staticmethod
    def evaluate(group: List[Individual]):
        """Static Method. evaluate performance of individuals to update fitness.

        Args:
            group (List[Individual]): individuals for evalutation.
        """
        for person in group:
            if not person.is_growup():
                person.express()
                person.evaluate()

    def size(self) -> int:
        """get number of individuals in current generation.
        """
        return self._size

    def append_newcomer(self, newcomer: Individual):
        """add new individual into current generation as adult.

        Args:
            newcomer (Individual): new individual to be added.

        Raises:
            ValueError: error message of `invalid newcomer.`, if newcomer's plasm not match with that of individual in current generation.
        """
        person = newcomer.copy()
        person.gen_id = self._gen_id
        person.idv_id = self._size
        if self._curr_gen:
            if not person.plasm.is_couple(self._curr_gen[0].plasm):
                raise ValueError('invalid newcomer as reproduction isolation')
        self._curr_gen.append(person)
        self._size += 1

    def _append_newborn(self, newborn: Individual):
        """add new individual into current generation as child.

        Args:
            newborn (Individual): new individual to be added.
        """
        person = newborn.copy()
        person.gen_id = self._gen_id
        person.idv_id = self._size
        self._children.append(person)
        self._size += 1

    def select(self, pool_size: Union[int, None] = None, tour_size: int = 2) -> List[Individual]:
        """select indvidual from current generation as parents for reproduce.

        Args:
            pool_size (Union[int, None], optional): number of parents. Defaults to None(1/2 of current generate individuals).
            tour_size (int, optional): number of individual for tournament to be parents. Defaults to 2.

        Returns:
            List[Individual]: shallow copy of list of parent individuals.
        """
        if pool_size is None:
            pool_size = int(self._size/2)
        # evaluate parents
        self.evaluate(self._curr_gen)
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
                if self._curr_gen[parent_idx].fitness < self._curr_gen[candidate_idx].fitness:
                    parent_idx = candidate_idx
            parents_idx_list.append(parent_idx)
        self._parents = []
        for i in parents_idx_list:
            self._parents.append(self._curr_gen[i])
        return self._parents.copy()

    def reproduce(self, cross_prob: float = 0.9) -> List[Individual]:
        """generate child individuals from parent by sexual reproduction.

        Args:
            cross_prob (float, optional): cross-over probability. Defaults to 0.9.

        Raises:
            ValueError: error message of `invalid cross_prob.`, when cross_prob not in [0, 1].

        Returns:
            List[Individual]: shallow copy of list of child indivudals.
        """
        if not 0 <= cross_prob <= 1:
            raise ValueError(
                'invalid cross_prob. Must in [0,1], got %6.4f' % cross_prob)
        self._children = []
        n_parents = len(self._parents)
        for _ in range(n_parents):
            if np.random.uniform(0, 1) < cross_prob:
                # select parents
                p0_idx = np.random.randint(0, n_parents)
                p1_idx = p0_idx
                while p1_idx == p0_idx:
                    p1_idx = np.random.randint(0, n_parents)
                # sexual produce
                c0, c1 = self._parents[int(p0_idx)].sexual_reproduce(
                    self._parents[int(p1_idx)], p_mutation=0)
                self._append_newborn(c0)
                self._append_newborn(c1)
            else:
                # asexual produce mutation
                p_idx = np.random.randint(0, n_parents)
                c = self._parents[int(p_idx)].asexual_reproduce(p_mutation=1)
                c.idv_id = len(self._children) + self._size
                self._append_newborn(c)
        # evaluate children
        self.evaluate(self._children)
        return self._children.copy()

    def eliminate(self) -> List[Individual]:
        """generate individuals in next generation by eliminating individuals with lower fitness in current generation and children group.

        Returns:
            List[Individual]: survivors in next generation with number of capacity.
        """
        self._combine = self._curr_gen.copy()
        self._combine.extend(self._children)
        combine_fit_list = [idv.fitness for idv in self._combine]
        combine_idx_list = list(range(len(self._combine)))
        joint_raw = zip(combine_fit_list, combine_idx_list)
        # sort individual on fitness from high to low
        joint_sort = sorted(joint_raw, reverse=True)
        # get the top size
        self._next_gen = []
        for i in range(self._capacity):
            next_idv = deepcopy(self._combine[joint_sort[i][1]])
            next_idv.idv_id = i
            next_idv.gen_id = self._gen_id + 1
            self._next_gen.append(next_idv)
        return self._next_gen.copy()

    def evolve(self, pool_size: Union[int, None] = None, tour_size: int = 2, cross_prob: float = 0.9) -> Population:
        """`this` population evolve into new population by select(), reproduce() and eliminate().

        Args:
            pool_size (Union[int, None], optional): number of parents. Defaults to None(1/2 of current generate individuals).
            tour_size (int, optional): number of individual for tournament to be parents. Defaults to 2.
            cross_prob (float, optional): cross-over probability. Defaults to 0.9.

        Returns:
            Population: new population after evolution.
        """
        self.select(pool_size, tour_size)
        self.reproduce(cross_prob)
        survivors = self.eliminate()
        next_gen_id = self._gen_id + 1
        next_population = Population(next_gen_id, survivors, self._capacity)
        return next_population
