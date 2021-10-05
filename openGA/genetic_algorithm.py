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
    genetic algortihm framework to seach optimal control variables combination to get max fitness.
    """

    def __init__(self, solution: Dict[str, float], capacity: int = 20):
        """create genetic algorithm instance.

        Args:
            solution (Dict[str, float]): initial combination of control variable name and its value in [0, 1].
            capacity (int, optional): max number of solution in each iteration. Defaults to 20.
        """
        # create chromosome of ancient
        ancient_plasm = Chromosome(list(solution.keys()))
        for i, gene_name in enumerate(solution):
            ancient_plasm.update(solution[gene_name], i)
        ancestors = [Individual(ancient_plasm)]
        for i in range(1, capacity):
            ancestors.append(Individual(ancient_plasm.random()))
        self._people = Population(0, ancestors, capacity)
        self._patched = False
        self._record = pd.DataFrame()

    @property
    def people(self) -> Population:
        """get current evolution status of ga.

        Returns:
            Population: people of genetic algorithm.
        """
        return self._people

    @property
    def patched(self) -> bool:
        """get patched status of genetic algorith.

        Returns:
            bool: True, ga is patched already. False, on the contrary.
        """
        return self._patched

    @patched.setter
    def patched(self, flag: bool):
        self._patched = flag

    @property
    def record(self) -> pd.DataFrame:
        """get ga evolution process record in data frame.
        """
        return self._record

    def add_patch(self, fit_funct: Callable[[], float]):
        """add callback function as monkey patch of ga.

        Args:
            fit_funct (Callable[[], float]): callback to get fitness with no input args.
        """

        # add monkey patch
        def express(self):
            pass

        def evaluate(self):
            self._fitness = fit_funct()

        Individual.express = express
        Individual.evaluate = evaluate
        self._patched = True

    def append(self, solution: Dict[str, float]):
        """append solution choice into ga.

        Args:
            solution (Dict[str, float]): combination of control variable name and its value in [0, 1].
        """
        ancient_plasm = Chromosome(list(solution.keys()))
        for i, gene_name in enumerate(solution):
            ancient_plasm.update(solution[gene_name], i)
        ancestor = Individual(ancient_plasm)
        self._people.append_newcomer(ancestor)

    def run(self, gen_max: int = 40, p_crossover: float = 0.9,
            pool_size: Union[int, None] = None, tour_size: int = 2):
        """run ga. to seach optimal solution.

        Args:
            gen_max (int, optional): max number of iteration. Defaults to 40.
            p_crossover (float, optional): cross-over probability. Defaults to 0.9.
            pool_size (Union[int, None], optional): number of parents. Defaults to None(1/2 of current generate individuals).
            tour_size (int, optional): number of individual for tournament to be parents. Defaults to 2.

        Raises:
            MemoryError: error message of `fitness function not loaded.`, if ga not patched.
        """
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
        """get optimal solution of ga.

        Returns:
            Individual: individual contains control variable combination as gene and objective variable as fitness.
        """
        return self._people.curr_gen[0]
