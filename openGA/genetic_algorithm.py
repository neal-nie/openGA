"""
genetic algorithm entry
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import logging
import pandas as pd
from typing import Dict, Union, Callable
from .population import Population
from .individual import Individual
from .chromosome import Chromosome

logger = logging.getLogger('openGA')


class GeneticAlgorithm(object):
    """
    genetic algortihm framework
    """

    def __init__(self, ancient_info: Dict[str, float], capacity: int = 20):
        # create chromosome of ancient
        ancient_plasm = Chromosome(list(ancient_info.keys()))
        for i, gene_name in enumerate(ancient_info):
            ancient_plasm.update(ancient_info[gene_name], i)
        ancestors = [Individual(ancient_plasm)]
        for i in range(1, capacity):
            ancestors.append(Individual(ancient_plasm.random()))
        self._people = Population(0, ancestors, capacity)
        self._patched = False
        self._record = pd.DataFrame()

    @property
    def people(self) -> Population:
        return self._people

    @property
    def patched(self) -> bool:
        return self._patched

    @property
    def record(self) -> pd.DataFrame:
        return self._record

    def add_patch(self, fit_funct: Callable[[], float]):
        # add monkey patch
        def express(self):
            pass

        def evaluate(self):
            self._fitness = fit_funct()

        Individual.express = express
        Individual.evaluate = evaluate
        self._patched = True

    def append_ancestor(self, ancestor_info: Dict[str, float]):
        ancient_plasm = Chromosome(list(ancestor_info.keys()))
        for i, gene_name in enumerate(ancestor_info):
            ancient_plasm.update(ancestor_info[gene_name], i)
        ancestor = Individual(ancient_plasm)
        self._people.append_newcomer(ancestor)

    def run(self, gen_max: int = 40, p_crossover: float = 0.9,
            pool_size: Union[int, None] = None, tour_size: int = 2):
        if not self._patched:
            raise MemoryError('fitness function not loaded.')
        # population evolution
        for _ in range(gen_max):
            new_people = self._people.evolve(pool_size, tour_size, p_crossover)
            self._record = self._record.append(
                self._people.to_df(), ignore_index=True)
            self._people = new_people
        self._record = self._record.append(
            self._people.to_df(), ignore_index=True)

    def result(self) -> Individual:
        return self._people.curr_gen[0]
