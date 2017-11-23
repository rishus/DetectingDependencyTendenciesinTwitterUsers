# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 17:18:13 2014

@author: rishu
"""

def compute_jaccard_index(set_1, set_2):
    n = len(set_1.intersection(set_2))
    return n / float(len(set_1) + len(set_2) - n) 