"""
define common used components
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

GENE_MAX = 1
GENE_MIN = 0

def limit(x, up=GENE_MAX, low=GENE_MIN):
    return max(low, min(x, up))