"""
test cases for individual
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import unittest
import numpy as np

from openGA import Individual, Chromosome


def express(self):
    self._fitness = 2


def evaluate(self, val):
    self._fitness = val


class TestIndividual(unittest.TestCase):

    def setUp(self) -> None:
        self.gene_name = ['a', 'b', 'c', 'd']
        self.plasm_0 = Chromosome(self.gene_name, check=False)
        self.plasm_0.random(inplace=True)
        self.plasm_0.update(0.1, 0)
        plasm_1 = self.plasm_0.copy().mutate()
        self.idv_0 = Individual(plasm=self.plasm_0)
        self.idv_1 = Individual(plasm=plasm_1)
        self.raw_express = Individual.express
        self.raw_evaluate = Individual.evaluate

    def tearDown(self) -> None:
        Individual.express = self.raw_express
        Individual.evaluate = self.raw_evaluate

    def test_init(self):
        self.assertEqual(self.idv_0.gen_id, -1)
        self.assertEqual(self.idv_0.idv_id, -1)
        self.idv_1.gen_id = 2
        self.idv_1.idv_id = 5
        self.assertEqual(self.idv_1.gen_id, 2)
        self.assertEqual(self.idv_1.idv_id, 5)
        with self.assertRaises(ValueError):
            self.idv_0.fitness
        self.assertIs(self.idv_0._fitness, None)
        self.assertFalse(self.idv_1.is_growup())

    def test_to_dict(self):
        d = self.idv_0.to_dict()
        self.assertTrue(d['fitness'] is np.nan)
        print(f'\ndict is {d}')

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
        self.assertFalse(person_clone is self.idv_0)

    def test_express(self):
        with self.assertRaises(NotImplementedError):
            self.idv_0.express()
        Individual.express = express
        self.idv_1.express()
        self.assertEqual(self.idv_1.fitness, 2)

    def test_evaluate(self):
        with self.assertRaises(NotImplementedError):
            self.idv_0.evaluate()
        Individual.evaluate = evaluate
        self.idv_0.evaluate(4)
        self.assertEqual(self.idv_0.fitness, 4)
        self.assertFalse(self.idv_0.to_dict()['fitness'] is np.nan)

    def test_str_format(self):
        print('\n%s' % self.idv_0)
        print(self.idv_1)

    def test_fitness(self):
        with self.assertRaises(ValueError):
            self.idv_0.fitness
        self.assertIs(self.idv_1._fitness, None)

    def test_sexual_reproduce(self):
        print(f'\nfather: {self.idv_0}')
        print(f'mother: {self.idv_1}')
        son, daughter = self.idv_1.sexual_reproduce(self.idv_0)
        print(f'son: {son}')
        print(f'daughter: {daughter}')
        print(f'father: {self.idv_0}')
        print(f'mother: {self.idv_1}')

    def test_asexual_reproduce(self):
        print(f'\nparent: {self.idv_0}')
        offspring = self.idv_0.asexual_reproduce(.9)
        print(f'offspring: {offspring}')
        print(f'parent: {self.idv_0}')


if __name__ == "__main__":
    unittest.main()
