# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:12:05 2021

@author: AndreaB.Rava
"""


#Define C
def evaluate_C (z_str, edges):
    C = 0
    z = list(z_str)
    for edge in edges:
        C += ((int(z[edge[0]])-int(z[edge[1]])**2)
    return C
