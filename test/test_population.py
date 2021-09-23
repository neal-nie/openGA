"""
test case for population
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import unittest
import numpy as np

from openGA import Population, Individual, Chromosome


def express(self):
    self._fitness = 0


def evaluate(self):
    self._fitness += np.random.uniform()


class TestPopulation(unittest.TestCase):

    def setUp(self) -> None:
        self.base_plasm = Chromosome(['a', 'b', 'c', 'd'])
        self.ancestor = Individual(self.base_plasm)
        self.people_0 = Population(0, [])
        self.people_1 = Population(1, [self.ancestor])
        p_list = []
        chm = self.ancestor.plasm
        print('\nancestor: %s' % self.ancestor)
        for i in range(10):
            p = Individual(chm.random())
            p._fitness = i * 2
            p_list.append(p)
        self.people_test = Population(3, p_list, capacity=10)
        self.raw_express = Individual.express
        self.raw_evaluate = Individual.evaluate

    def tearDown(self) -> None:
        Individual.express = self.raw_express
        Individual.evaluate = self.raw_evaluate

    def test_init(self):
        self.assertEqual(self.people_0.gen_id, 0)
        self.assertEqual(self.people_1._gen_id, 1)
        self.assertEqual(self.people_0._size, 0)
        self.assertEqual(self.people_1.size(), 1)
        self.assertEqual(self.people_0.size(), 0)
        for i, p in enumerate(self.people_1.curr_gen):
            print(p)
            self.assertEqual(p.gen_id, 1)
            self.assertEqual(p.idv_id, i)
        self.assertListEqual(self.people_0._parents, [])
        self.assertListEqual(self.people_1._children, [])
        self.assertListEqual(self.people_0._next_gen, [])

        with self.assertRaises(ValueError):
            self.people_0.parents
        with self.assertRaises(ValueError):
            self.people_1.children
        with self.assertRaises(ValueError):
            self.people_0.next_gen

    def test_str(self):
        print(self.people_0)
        print(self.people_1)
        print(self.people_test)

    def test_evaluate(self):
        with self.assertRaises(NotImplementedError):
            Population.evaluate(self.people_1.curr_gen)
        Individual.express = express
        Individual.evaluate = evaluate
        Population.evaluate(self.people_1.curr_gen)
        self.assertTrue(0 <= self.people_1.curr_gen[0].fitness <= 1)

    def test_append(self):
        immigrant = self.ancestor.copy()
        self.people_1.append_newcomer(immigrant)
        self.assertEqual(self.people_1.size(), 2)
        self.assertEqual(
            self.people_1.curr_gen[1].gen_id, self.people_1.gen_id)
        self.assertEqual(self.people_1.curr_gen[1].idv_id, 1)

    # @unittest.skip('ignore this case')
    def test_select(self):
        self.assertEqual(self.people_test.size(), 10)
        print('current generation:')
        for i in self.people_test.curr_gen:
            print(i)
        self.people_test.select()
        print('selected parents:')
        for i in self.people_test.parents:
            print(i)
        print(self.people_test)
        self.people_test.select(3)
        print('selected parenet:')
        for i in self.people_test.parents:
            print(i)

    def test_reproduce(self):
        Individual.express = express
        Individual.evaluate = evaluate
        parent = self.people_test.select()
        print(f'\nparents:')
        for p in parent:
            print(p)
        children = self.people_test.reproduce()
        print(self.people_test)
        print('children:')
        for c in children:
            print(c)
        self.assertTrue(0 < len(children) <= self.people_test.size())

    def test_eliminate(self):
        print(f'\ncurrent generation:')
        for p in self.people_test.curr_gen:
            print(p)
        Individual.express = express
        Individual.evaluate = evaluate
        parent = self.people_test.select()
        children = self.people_test.reproduce()
        print('parent:')
        for p in parent:
            print(p)
        print('children:')
        for p in children:
            print(p)
        next_generation = self.people_test.eliminate()
        print('next generation:')
        for p in next_generation:
            print(p)
        self.assertEqual(
            next_generation[0].gen_id, self.people_test.gen_id + 1)
        self.assertTrue(next_generation[0].is_growup())

    def test_evolve(self):
        print(f'\ncurrent generation:')
        for p in self.people_test.curr_gen:
            print(p)
        Individual.express = express
        Individual.evaluate = evaluate
        next_generation = self.people_test.evolve()
        del self.people_test
        print('next generation:')
        for p in next_generation.curr_gen:
            print(p)


if __name__ == "__main__":
    unittest.main()
