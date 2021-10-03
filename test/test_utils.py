"""
test case for utils
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import unittest

from openGA.utils import uniform_open, limit, GENE_MAX, GENE_MIN


class TestUtils(unittest.TestCase):

    def test_limit(self):
        self.assertEqual(limit(GENE_MIN-0.1), GENE_MIN)
        self.assertEqual(limit(GENE_MAX+0.2), GENE_MAX)
        half = (GENE_MIN + GENE_MAX) / 2
        self.assertEqual(limit(half), half)

    def test_uniform_open(self):
        upper = 2
        lower = 1
        for _ in range(10000):
            val = uniform_open(lower, upper)
            self.assertLess(val, upper)
            self.assertGreater(val, lower)


if __name__ == "__main__":
    unittest.main()
