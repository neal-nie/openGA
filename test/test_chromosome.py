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
        cls.plasm = Chromosome(cls.names)

    def setUp(self) -> None:
        self.plasm = Chromosome(['a', 'b'], check=False)

    def test_eq(self):
        self.assertFalse(TestChromosome.plasm == self.plasm)
        t0 = Chromosome(['a', 'b'], check=False)
        self.assertTrue(t0 == self.plasm)
        t0.check = True
        self.assertTrue(t0._check)
        self.assertFalse(t0 == self.plasm)
        self.plasm.check = True
        t0.update(.8, 1)
        self.assertTrue(t0 != self.plasm)
        t1 = Chromosome(['a', 'c'], check=False)
        self.assertFalse(t0 == t1)

    def test_gene_num(self):
        self.assertEqual(len(TestChromosome.names),
                         TestChromosome.plasm._gene_num)

    def test_gene_name(self):
        self.assertListEqual(TestChromosome.names,
                             TestChromosome.plasm._gene_names)

    def test_init_genes(self):
        self.assertTrue(np.all(self.plasm.gene_values == 0))

    def test_update_no_check(self):
        self.plasm.update(2, 1)
        self.assertEqual(self.plasm.gene_values[1], 2)

    def test_update_check(self):
        self.plasm.check = True
        self.plasm.update(2, 1)
        self.assertEqual(self.plasm.gene_values[1], 1)

    def test_not_couple(self):
        self.assertFalse(self.plasm.is_couple(TestChromosome.plasm))
        test_plasm = Chromosome(['a', 'c'])
        self.assertFalse(self.plasm.is_couple(test_plasm))

    def test_is_couple(self):
        test_plasm = Chromosome(['a', 'b'])
        self.assertTrue(self.plasm.is_couple(test_plasm))

    def test_copy(self):
        test_plasm = self.plasm.copy()
        self.assertEqual(self.plasm.check, test_plasm.check)
        self.assertTrue(
            np.all(self.plasm.gene_values == test_plasm.gene_values))
        self.assertFalse(self.plasm._gene_values is test_plasm._gene_values)

    def test_random(self):
        origin_genes = self.plasm.gene_values
        print(f'\norigin chromosome: {self.plasm}')
        self.plasm.random()
        print(f'randomized chromosome: {self.plasm}')
        self.assertFalse(np.all(origin_genes == self.plasm.gene_values))

    def test_crossover_unmatch(self):
        self.plasm.check = True
        with self.assertRaises(ValueError):
            self.plasm.crossover(TestChromosome.plasm)

    def test_crossover(self):
        self.plasm.update(0.5, 1)
        self.plasm.update(0.8, 0)
        c0, c1 = self.plasm.crossover(TestChromosome.plasm)
        print(f'\nparent0 chromosome: {self.plasm}')
        print(f'parent1 chromosome: {TestChromosome.plasm}')
        print(f'child0 chromosome: {c0}')
        print(f'child1 chromosome: {c1}')
        self.assertEqual(self.plasm._gene_num, c0._gene_num)
        self.assertEqual(self.plasm._gene_num, c1._gene_num)
        self.assertEqual(self.plasm.check, c0.check)
        self.assertEqual(self.plasm.check, c1.check)

    def test_mutate(self):
        test_plasm = self.plasm.mutate()
        print(f'\norigin chromosome: {self.plasm}')
        print(f'mutate chromosome: {test_plasm}')

    def test_size(self):
        names = ['a', 'b']
        test_plasm = Chromosome(names)
        self.assertEqual(test_plasm.size(), len(names))


if __name__ == "__main__":
    import sys
    print(sys.executable)
    unittest.main()
