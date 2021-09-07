"""
define common used components
"""
# Copyright (c) 2015-2021 Neal Nie. All rights reserved.

def limit(x, up=1, low=0):
    return max(low, min(x, up))