# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 15:43:11 2021

@author: AndreaB.Rava
"""

# -*- coding: utf-8 -*-

import configparser
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

Path("plots").mkdir(parents=True, exist_ok=True)
configu = configparser.ConfigParser()
configu.read(sys.argv[1])
str_graph = sys.argv[2]
str_N_NODES = configu.get(str_graph, 'n_nodes')
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

source1 = configu.get('paths',f"my_prob_dist_{str_graph}")

destination1 = configu.get('paths',f"{str_graph}_graph_pic")
destination2 = configu.get('paths',f"{str_graph}_prob_dist_pic")


#Plot the graph
def graph_plot():
    """
    This method plot the graph
    """
    colors = ['r' for node in graph.nodes()]
    pos = nx.circular_layout(graph)
    nx.draw_networkx(graph, node_color=colors, node_size=200, pos = pos, alpha=1, with_labels=True)
    plt.title(f"{str_graph} graph", size=20)
    plt.savefig(destination1, dpi=300, bbox_inches='tight')


def prob_dist_plot():
    """
    This method plots the probability distribution of the final state
    which contain the MaxCut solutions.
    """
    prob_dist_fin_state = np.load(source1)
    fig = plt.figure(figsize = (2**N_QUBITS,20))
    plt.xlabel('configuration', size=20)
    plt.ylabel('probablity', size=30)
    plt.title(f"probabily distribution configurations for {str_graph} graph", size=40)
    plt.xticks(rotation=45, size=20)
    plt.yticks(size=30)
    xticks = range(0,2**(N_QUBITS-1))
    xtick_labels = list(map(lambda x: format(x, "0"+str(N_QUBITS)+'b'), xticks))
    plt.bar(xtick_labels,prob_dist_fin_state[:2**(N_QUBITS-1)],width = 0.5)
    fig.savefig(destination2, bbox_inches='tight')

graph_plot()
prob_dist_plot()
