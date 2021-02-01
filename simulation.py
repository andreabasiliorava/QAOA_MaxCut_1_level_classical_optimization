# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:09:06 2021

@author: AndreaB.Rava
"""

import scipy
import qutip as qu
import qaoa
import graphs as gr
#import qucompsys as qucs
#import numpy as np
#import matplotlib.pyplot as plt
#import configparser
#import networkx as nx

#main part of the code

#STEP 1: take information of the graph
"""
#METHOD 1: define it manually
#butterfly graph
N_NODES = 5
nodes = []
for i in range(N_NODES):
    nodes.append(i)
edges = [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]
N_QUBITS = N_NODES
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)
"""

"""
#METHOD 2: take information from a file
config = configparser.ConfigParser()
config.read('graphs.txt')
str_graph = 'square'
str_N_NODES = config.get(str_graph, 'N_NODES')
str_edges = config.get(str_graph, 'edges')
N_NODES = int(str_N_NODES)
N_QUBITS = N_NODES
edges = []
for edge in str_edges.split(';'):
    edges.append((int(edge[1]),int(edge[3])))
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)
"""

#METHOD 3: generate a random graph
#generate random graph with at least one edge
N_NODES = 6
N_QUBITS = N_NODES
graph = gr.random_graph(N_NODES)
edges = list(graph.edges)


#STEP 4: find optimal parameters
optimal_params = scipy.optimize.minimize(qaoa.analitical_f_1, [0.0, 0.0], args = (graph, edges), method='Nelder-Mead')['x']
optimal_gamma = optimal_params[0]
optimal_beta = optimal_params[1]


#STEP 5: obtain final state with solutions
# initial state (as density matrix):
init_state = qaoa.initial_state(N_QUBITS)
dm_init_state = qu.ket2dm(init_state)

# define MaxCut hamiltonian operators
mix_ham = qaoa.mix_hamilt(N_QUBITS)
prob_ham = qaoa.prob_hamilt(N_QUBITS, edges)

# obtain final state (as density matrix)
fin_state = qaoa.evolution_operator(N_QUBITS, edges, [optimal_gamma], [optimal_beta])*init_state
dm_fin_state = qu.ket2dm(fin_state)
