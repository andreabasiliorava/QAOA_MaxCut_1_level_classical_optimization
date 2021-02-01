# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:09:06 2021

@author: AndreaB.Rava
"""

import scipy
import qutip as qu
import qaoa
import graphs as gr
import qucompsys as qucs
import numpy as np
import matplotlib.pyplot as plt
import configparser
import networkx as nx

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
config.read('graphs.txt')
str_graph = 'square'
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
#"""

"""
#METHOD 3: generate a random graph
#generate random graph with at least one edge
N_NODES = 6
N_QUBITS = N_NODES
graph = gr.random_graph(N_NODES)
edges = list(graph.edges)
"""

#Plot the graph
colors = ['r' for node in graph.nodes()]
pos = nx.circular_layout(graph)
graph_drawing = nx.draw_networkx(graph, node_color=colors, node_size=200, alpha=1, pos=pos, with_labels=True)
plt.show()

#STEP 2: find optimal parameters
optimal_params = scipy.optimize.minimize(qaoa.analitical_f_1, [0.0, 0.0], args = (graph, edges), method='Nelder-Mead')['x']
optimal_gamma = optimal_params[0]
optimal_beta = optimal_params[1]


#STEP 3: obtain final state with solutions
# initial state (as density matrix):
init_state = qaoa.initial_state(N_QUBITS)
dm_init_state = qu.ket2dm(init_state)

# define MaxCut hamiltonian operators
mix_ham = qaoa.mix_hamilt(N_QUBITS)
prob_ham = qaoa.prob_hamilt(N_QUBITS, edges)

# obtain final state (as density matrix)
fin_state = qaoa.evolution_operator(N_QUBITS, edges, [optimal_gamma], [optimal_beta])*init_state
dm_fin_state = qu.ket2dm(fin_state)

#plot probability distributions of configurations in final state
prob_dist_fin_state = qucs.comp_basis_prob_dist(fin_state)
plt.figure(figsize = (2**N_QUBITS/2.5,20))
plt.xticks(rotation=45)
xticks = range(0,2**(N_QUBITS-1))
xtick_labels = list(map(lambda x: format(x, "0"+str(N_QUBITS)+'b'), xticks))
plt.bar(xtick_labels,prob_dist_fin_state[:2**(N_QUBITS-1)],width = 0.5)
