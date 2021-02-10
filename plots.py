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

source1 = configu.get('paths','my_graph')
source2 = configu.get('paths','my_prob_dist')

destination1 = configu.get('paths','graph_pic')
destination2 = configu.get('paths','prob_dist_pic')


#Plot the graph
def graphPlot():
    """
    This method plot the graph
    """
    graph = np.load(source1)
    colors = ['r' for node in graph.nodes()]
    pos = nx.circular_layout(graph)
    graph_drawing = nx.draw_networkx(graph, node_color=colors, node_size=200, alpha=1, pos=pos, with_labels=True)
    graph_drawing.savefig(destination1)
    
    
def prob_distPlot():
    """ 
    This method plots the probability distribution of the final state 
    which contain the MaxCut solutions.
    """
    prob_dist_fin_state = np.load(source2)   
    graph = np.load(source1)
    N_QUBITS = len(list(graph.nodes))
    #fig = plt.figure(figsize=(18, 18)) # plot the calculated values    
    fig = plt.figure(figsize = (2**N_QUBITS/2.5,20))
    plt.xticks(rotation=45)
    xticks = range(0,2**(N_QUBITS-1))
    xtick_labels = list(map(lambda x: format(x, "0"+str(N_QUBITS)+'b'), xticks))
    plt.bar(xtick_labels,prob_dist_fin_state[:2**(N_QUBITS-1)],width = 0.5)
    fig.savefig(destination2)

graphPlot()
prob_distPlot()
