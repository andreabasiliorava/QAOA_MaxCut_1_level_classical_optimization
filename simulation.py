# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:09:06 2021

@author: AndreaB.Rava
"""

import qaoa
import graphs as gr
import qucompsys as qucs
import numpy as np
import matplotlib.pyplot as plt
import qutip as qu
import configparser
import networkx as nx
from   networkx.generators.random_graphs import erdos_renyi_graph

#main part of the code

#STEP 1: take information of the graph
"""
#METHOD 1: define it manually
#butterfly graph
n_nodes = 5
nodes = []
for i in range(n_nodes):
    nodes.append(i)
edges = [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]
n_qubits = n_nodes
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)
"""

"""
#METHOD 2: take information from a file
config = configparser.ConfigParser()
config.read('graphs.txt')
str_graph = 'square'
str_n_nodes = config.get(str_graph, 'n_nodes')
str_edges = config.get(str_graph, 'edges')
n_nodes = int(str_n_nodes)
n_qubits = n_nodes
edges = []
for edge in str_edges.split(';'):
    edges.append((int(edge[1]),int(edge[3])))
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)
"""

#METHOD 3: generate a random graph
#generate random graph with at least one edge
n_nodes = 6
n_qubits = n_nodes
prob = 0.5
graph = erdos_renyi_graph(n_nodes, prob)
while len(list(graph.edges)) < 1:
    graph = erdos_renyi_graph(n_nodes, prob)
edges = list(graph.edges)


#STEP 3: define analitical expectation coat function
def analitical_f_1(parameters, graph, edges):
    """
    This function returns the value of the estimated cost function for specific
    gamma and beta of a given graph (with opposite sign)

    Parameters
    ----------
    parameters : numpy.ndarray
        1-D array containing the parameters of the function.
    graph : networkx.classes.graph.Graph
        graph defined in the library networkx belonging to the class Graph.
    edges : list of tuples
        edges of the graph.

    Returns
    -------
    -f_1: float
        estimated cost function with opposite sign.

    """
    f_1 = 0
    gamma = parameters[0]
    beta = parameters[1]
    for edge in edges:
        degree_u = gr.node_degree(graph, edge[0])
        degree_v = gr.node_degree(graph, edge[1])
        lambda_uv = gr.common_neighbours(graph, edge[0], edge[1])
        c_uv = 0.5+0.25*np.sin(4*beta)*np.sin(gamma)*(np.cos(gamma)**(degree_u-1) + np.cos(gamma)**(degree_v-1))
        -0.25*np.sin(beta)**2*np.cos(gamma)**(degree_u+degree_v-2-2*lambda_uv)*(1-np.cos(2*gamma)**lambda_uv)
        f_1 += c_uv
    return -f_1



"""
# initial state (as density matrix):
init_state = qaoa.initial_state(n_qubits)
dm_init_state = qu.ket2dm(init_state)

# define MaxCut hamiltonian operators
mix_ham = qaoa.mix_hamilt(n_qubits)
prob_ham = qaoa.prob_hamilt(n_qubits, edges)

# obtain final state (as density matrix)
fin_state = qaoa.evolution_operator(n_qubits, edges, gammas, betas)*init_state
dm_fin_state = qu.ket2dm(fin_state)
"""