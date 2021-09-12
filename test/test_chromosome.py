"""
test case for chromosome
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import unittest
import numpy as np

from openGA import Chromosome


class TestChromosome(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.names = ['c-0', 'c-1', 'c-2', 'c-3']
        cls.palsm = Chromosome(cls.names)

    def setUp(self) -> None:
        self.palsm = Chromosome(['a', 'b'], check=False)

    def test_gene_num(self):
        self.assertEqual(len(TestChromosome.names),
                         TestChromosome.palsm._gene_num)

    def test_gene_name(self):
        self.assertListEqual(TestChromosome.names,
                             TestChromosome.palsm._gene_names)

    def test_init_genes(self):
        self.assertTrue(np.all(self.palsm.gene_values == 0))

    def test_update_no_check(self):
        self.palsm._update(2, 1)
        self.assertEqual(self.palsm.gene_values[1], 2)

    def test_update_check(self):
        self.palsm.check = True
        self.palsm._update(2, 1)
        self.assertEqual(self.palsm.gene_values[1], 1)

    def test_not_couple(self):
        self.assertFalse(self.palsm.is_couple(TestChromosome.palsm))
        test_palsm = Chromosome(['a', 'c'])
        self.assertFalse(self.palsm.is_couple(test_palsm))

    def test_is_couple(self):
        test_palsm = Chromosome(['a', 'b'])
        self.assertTrue(self.palsm.is_couple(test_palsm))

    def test_copy(self):
        test_palsm = self.palsm.copy()
        self.assertEqual(self.palsm.check, test_palsm.check)
        self.assertTrue(
            np.all(self.palsm.gene_values == test_palsm.gene_values))
        self.assertFalse(self.palsm._gene_values is test_palsm._gene_values)

    def test_random(self):
        origin_genes = self.palsm.gene_values
        self.palsm.random()
        print(f'\norigin chromosome: {origin_genes}')
        print(f'randomized chromosome: {self.palsm.gene_values}')
        self.assertFalse(np.all(origin_genes == self.palsm.gene_values))

    def test_crossover_unmatch(self):
        self.palsm.check = True
        with self.assertRaises(ValueError):
            self.palsm.crossover(TestChromosome.palsm)

    def test_crossover(self):
        self.palsm._update(0.5, 1)
        self.palsm._update(0.8, 0)
        c0, c1 = self.palsm.crossover(TestChromosome.palsm)
        print(f'\nparent0 chromosome: {self.palsm.gene_values}')
        print(f'parent1 chromosome: {TestChromosome.palsm.gene_values}')
        print(f'child0 chromosome: {c0.gene_values}')
        print(f'child1 chromosome: {c1.gene_values}')
        self.assertEqual(self.palsm._gene_num, c0._gene_num)
        self.assertEqual(self.palsm._gene_num, c1._gene_num)
        self.assertEqual(self.palsm.check, c0.check)
        self.assertEqual(self.palsm.check, c1.check)

    def test_mutate(self):
        test_palsm = self.palsm.mutate()
        print(f'\norigin chromosome: {self.palsm.gene_values}')
        print(f'mutate chromosome: {test_palsm.gene_values}')


if __name__ == "__main__":
    import sys
    print(sys.executable)
    unittest.main()
