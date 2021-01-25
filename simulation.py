# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:09:06 2021

@author: AndreaB.Rava
"""

#libraries needed:
import numpy as np
import matplotlib.pyplot as plt
import qutip as qu
import configparser

#main part of the code
config = configparser.ConfigParser()
config.read('butterfly.txt')

str_n_vertices = config.get('settings', 'n_vertices')
str_edges = config.get('settings', 'edges')

n_vertices = int(str_n_vertices)

edges = []
for edge in str_edges.split(';'):
    edges.append((int(edge[1]),int(edge[3])))



