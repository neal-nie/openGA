"""
define common used components
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

import numpy as np
from typing import Union

GENE_MAX = 1
GENE_MIN = 0


def limit(x, up=GENE_MAX, low=GENE_MIN) -> Union[int, float]:
    return max(low, min(x, up))


def uniform_open(low: float = 0.0, high: float = 1.0) -> float:
    """generate a random float in open interval (low, high) and obey uniform distribution.

    Args:
        low (float, optional): lower boundary, exclusive. Defaults to 0.0.
        high (float, optional): higher boundary, exclusive. Defaults to 1.0.

    Returns:
        float: random value in (low, high).
    """
    mid = (low + high) / 2
    right = np.random.uniform(mid, high)
    left = 2 * mid - right
    rlt = np.random.choice([right, left])
    return rlt
