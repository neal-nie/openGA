"""
test cases for individual
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import unittest
import numpy as np

from openGA import Individual, Chromosome


def express(self):
    self._fittness = 2


def evaluate(self, val):
    self._fittness = val


class TestIndividual(unittest.TestCase):

    def setUp(self) -> None:
        self.gene_name = ['a', 'b', 'c', 'd']
        self.plasm_0 = Chromosome(self.gene_name, check=False)
        self.plasm_0.random()
        self.plasm_0.update(0.1, 0)
        plasm_1 = self.plasm_0.copy().mutate()
        self.idv_0 = Individual(0, 0, plasm=self.plasm_0)
        self.idv_1 = Individual(0, 1, plasm=plasm_1)

    def test_init(self):
        self.assertEqual(self.idv_0.gen_id, 0)
        self.assertEqual(self.idv_0.idv_id, 0)
        self.idv_1.gen_id = 2
        self.idv_1.idv_id = 5
        self.assertEqual(self.idv_1.gen_id, 2)
        self.assertEqual(self.idv_1.idv_id, 5)
        with self.assertRaises(ValueError):
            self.idv_0.fittness
        self.assertIs(self.idv_0._fittness, None)
        self.assertFalse(self.idv_1.is_growup())

    def test_plasm(self):
        plasm = self.idv_0.plasm
        self.assertListEqual(plasm._gene_names, self.gene_name)
        self.assertTrue(np.all(plasm.gene_values == self.plasm_0.gene_values))
        print(f'\norigin genes: {self.idv_1.plasm}')
        self.idv_1.plasm = plasm
        print(f'after set: {self.idv_1.plasm}')
        self.assertListEqual(plasm._gene_names, self.idv_1.plasm._gene_names)
        self.assertTrue(np.all(plasm.gene_values ==
                        self.idv_1.plasm.gene_values))

    def test_copy(self):
        person_clone = self.idv_0.copy()
        self.assertEqual(person_clone.gen_id, self.idv_0.gen_id)
        self.assertEqual(person_clone.idv_id, self.idv_0.idv_id)
        self.assertEqual(person_clone._check, self.idv_0._check)
        self.assertEqual(person_clone.plasm, self.idv_0.plasm)

    def test_express(self):
        with self.assertRaises(NotImplementedError):
            self.idv_0.express()
        Individual.express = express
        self.idv_1.express()
        self.assertEqual(self.idv_1.fittness, 2)

    def test_evaluate(self):
        Individual.evaluate = evaluate
        self.idv_0.evaluate(4)
        self.assertEqual(self.idv_0.fittness, 4)


if __name__ == "__main__":
    unittest.main()
