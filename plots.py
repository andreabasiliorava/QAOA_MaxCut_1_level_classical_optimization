# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:43:11 2021

@author: AndreaB.Rava
"""

# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import sys
import configparser
import networkx as nx

configu = configparser.ConfigParser()
configu.read(sys.argv[1])
str_graph = sys.argv[2]
str_N_NODES = configu.get(str_graph, 'N_NODES')
str_edges = configu.get(str_graph, 'edges')
N_NODES = int(str_N_NODES)
N_QUBITS = N_NODES
nodes = np.arange(0, N_NODES, 1)
edges = []
for edge in str_edges.split(';'):
    edges.append((int(edge[1]),int(edge[3])))
graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

source1 = configu.get('paths','my_prob_dist')

destination1 = configu.get('paths','graph_pic')
destination2 = configu.get('paths','prob_dist_pic')


#Plot the graph
def graphPlot():
    """
    This method plot the graph
    """
    #graph = np.load(source1)
    #fig = plt.figure(figsize=(18, 18))
    #nx.draw(graph)
    #fig.savefig(destination1)
    nx.draw(graph, with_labels=True)
    plt.savefig(destination1, dpi=300, bbox_inches='tight')
    
    
def prob_distPlot():
    """ 
    This method plots the probability distribution of the final state 
    which contain the MaxCut solutions.
    """
    prob_dist_fin_state = np.load(source1)
    N_QUBITS = len(list(graph.nodes))
    #fig = plt.figure(figsize=(18, 18)) # plot the calculated values    
    fig = plt.figure(figsize = (2**N_QUBITS,10))
    plt.xticks(rotation=45)
    xticks = range(0,2**(N_QUBITS-1))
    xtick_labels = list(map(lambda x: format(x, "0"+str(N_QUBITS)+'b'), xticks))
    plt.bar(xtick_labels,prob_dist_fin_state[:2**(N_QUBITS-1)],width = 0.5)
    fig.savefig(destination2)

graphPlot()
prob_distPlot()
