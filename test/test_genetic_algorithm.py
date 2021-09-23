"""
test case for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import unittest
import numpy as np

from openGA import GeneticAlgorithm
from openGA import Individual


def get_fitness():
    return round(np.random.uniform(), 4)


class TestGeneticAlgorithm(unittest.TestCase):

    def setUp(self) -> None:
        base_gene = {
            'a': 0.5,
            'b': 0.7,
            'c': 0.1,
            'd': 0.3
        }
        self.ga = GeneticAlgorithm(base_gene)

    def test_init(self):
        self.assertFalse(self.ga._patched)
        self.assertFalse(self.ga.patched)
        print(self.ga.people)

    def test_run(self):
        self.ga.add_patch(get_fitness)
        self.assertTrue(self.ga.patched)
        print(f"\ndefine fit funciton {get_fitness}")
        print(f"evaluate in Individual {Individual.evaluate}")
        # self.assertTrue(get_fitness is Individual.evaluate)
        print("before evoluation:")
        print(f"{self.ga.people}")
        self.ga.run()
        print("after evolution:")
        print(f"{self.ga.people}")
        print("evolution result:")
        print(f"{self.ga.result()}")


if __name__ == "__main__":
    unittest.main()
