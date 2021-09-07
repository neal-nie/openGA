"""
population for genetic algorithm
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import logging
from .individual import Individual

logger = logging.getLogger('openGA')

class Population(object):
    """
    population contain current generation(includes adults, children) and next generateion
    """
    def __init__(self) -> None:
        super().__init__()