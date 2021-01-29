# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:09:06 2021

@author: AndreaB.Rava
"""

import qaoa
#import qucompsys as qucs
#import numpy as np
#import matplotlib.pyplot as plt
#import qutip as qu
import configparser

#main part of the code

#take information of the graph
config = configparser.ConfigParser()
config.read('graphs.txt')

#str_graph = input ("telle me the kind of graph",)
str_graph = 'square'
str_n_vertices = config.get(str_graph, 'n_vertices')
str_edges = config.get(str_graph, 'edges')

n_vertices = int(str_n_vertices)
n_qubits = n_vertices

edges = []
for edge in str_edges.split(';'):
    edges.append((int(edge[1]),int(edge[3])))

#choose QAOA-level
n_levels = 1

#pick intial parameters 
init_params = qaoa.initial_params(n_levels)
gammas = init_params[0]
betas = init_params[1]

# initial state |s>:
init_state = qaoa.initial_state(n_qubits)

# define MaxCut hamiltonian operators
mix_ham = qaoa.mix_hamilt(n_qubits)
prob_ham = qaoa.prob_hamilt(n_vertices, edges)

# obtain final state
fin_state = qaoa.evolution_operator(n_qubits, edges, gammas, betas)*init_state








