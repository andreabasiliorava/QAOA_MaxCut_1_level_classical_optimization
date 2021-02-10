# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:09:06 2021

@author: AndreaB.Rava
"""

import qutip as qu
import qaoa
import qucompsys as qucs
import numpy as np
import configparser
import networkx as nx
import sys

#main part of the code

#STEP 1: take information of the graph
"""
#METHOD 1: define it manually
#butterfly graph
N_NODES = 5
nodes = np.arange(0, N_NODES, 1)
edges = [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]
N_QUBITS = N_NODES
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)
"""

#"""
#METHOD 2: take information from a file
config = configparser.ConfigParser()
config.read(sys.argv[1])
str_graph = sys.argv[2]
str_N_NODES = config.get(str_graph, 'N_NODES')
str_edges = config.get(str_graph, 'edges')
N_NODES = int(str_N_NODES)
N_QUBITS = N_NODES
nodes = np.arange(0, N_NODES, 1)
edges = []
for edge in str_edges.split(';'):
    edges.append((int(edge[1]),int(edge[3])))
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

destination1 = config.get('paths','my_prob_dist')
#"""

"""
#METHOD 3: generate a random graph
#generate random graph with at least one edge
N_NODES = 6
N_QUBITS = N_NODES
graph = gr.random_graph(N_NODES)
edges = list(graph.edges)
"""


#STEP 2: find optimal parameters
# Grid search for the maximizing variables
step_size = 0.01
a_gamma         = np.arange(0.0, np.pi, step_size)
a_beta          = np.arange(0.0, np.pi/2, step_size)
a_gamma, a_beta = np.meshgrid(a_gamma, a_beta, indexing='xy')
grid_f_1 = qaoa.analitical_f_1(a_gamma, a_beta, graph, edges)
result = np.where(grid_f_1 == np.amax(grid_f_1))
a      = list(zip(result[0],result[1]))[0]
optimal_gamma   = a[1]*step_size
optimal_beta  = a[0]*step_size
print(optimal_gamma)
print(optimal_beta)

#STEP 3: obtain final state with solutions
# initial state (as density matrix):
init_state = qaoa.initial_state(N_QUBITS)
dm_init_state = qu.ket2dm(init_state)

# obtain final state (as density matrix)
fin_state = qaoa.evolution_operator(N_QUBITS, edges, [optimal_gamma], [optimal_beta])*init_state
dm_fin_state = qu.ket2dm(fin_state)

#probability distributions of configurations in final state
prob_dist_fin_state = qucs.comp_basis_prob_dist(fin_state)

np.save(destination1, prob_dist_fin_state)
