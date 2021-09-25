# -*- coding: UTF-8 -*-
"""
example to search max in single peak problem
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import numpy as np
from openGA import GeneticAlgorithm, Individual


def object_funct(x: float, y: float) -> float:
    """single peak sine objective funciton

    Args:
        x (float): x direction var in [0,1]
        y (float): y direction var in [0,1]

    Returns:
        float: object value, in [-1,1]
    """
    x_rad = x * np.pi * 2
    y_rad = y * np.pi * 2
    t = (np.sin(x_rad) + 1) * (np.sin(y_rad) + 1)
    return t


def patch_funct(self):
    arg0 = self.plasm.to_dict()['x']
    arg1 = self.plasm.to_dict()['y']
    self._fitness = object_funct(arg0, arg1)


def dummy_funct(self):
    pass


if __name__ == "__main__":
    Individual.evaluate = patch_funct
    Individual.express = dummy_funct
    base_gene = {
        'x': 0.7,
        'y': 0.2
    }
    ga = GeneticAlgorithm(base_gene)
    ga._patched = True
    print("at initial condition")
    print(ga.people)
    ga.run(gen_max=100)
    print("after evolution:")
    print(f"{ga.people}")
    print("evolution result:")
    print(f"{ga.result()}")
