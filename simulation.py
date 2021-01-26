# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:09:06 2021

@author: AndreaB.Rava
"""

import qaoa
import numpy as np
import matplotlib.pyplot as plt
import qutip as qu
import configparser

#main part of the code

#take information of the graph
config = configparser.ConfigParser()
config.read('butterfly.txt')

str_n_vertices = config.get('settings', 'n_vertices')
str_edges = config.get('settings', 'edges')

n_vertices = int(str_n_vertices)

edges = []
for edge in str_edges.split(';'):
    edges.append((int(edge[1]),int(edge[3])))

#choose QAOA-level
n_levels = 1

#pick intial parameters 
init_params = qaoa.initial_params(n_levels)

# initial state |s>:
init_state = qaoa.initial_state(n_vertices)







