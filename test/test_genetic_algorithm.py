"""
test case for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import unittest
from unittest.case import skip
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
        self.raw_express = Individual.express
        self.raw_evaluate = Individual.evaluate

    def tearDown(self) -> None:
        rec_df = self.ga.record
        print(f'\nga record is:')
        print(rec_df)
        Individual.express = self.raw_express
        Individual.evaluate = self.raw_evaluate

    # @unittest.skip('debug')
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

    def test_append(self):
        origin_size = self.ga.people.size()
        base_gene = {
            'a': 0.8,
            'b': 0.9,
            'c': 0.2,
            'd': 0.7
        }
        self.ga.append(base_gene)
        new_size = self.ga.people.size()
        self.assertEqual(new_size, origin_size + 1)
        self.assertDictEqual(
            base_gene, self.ga.people.curr_gen[-1].plasm.to_dict())
        self.assertIsNot(
            base_gene, self.ga.people.curr_gen[-1].plasm.to_dict())


if __name__ == "__main__":
    unittest.main()
