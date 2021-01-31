# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 16:35:13 2021

@author: AndreaB.Rava
"""

import simulation
import graphs as gr
from hypothesis import given
import networkx as nx
from nose.tools import assert_equal

def test_analitical_f_1():
    #test if it gives expected result for known optimal parameters of a graph
    nodes = [0, 1, 2]
    edges = [(0,1),(1,2)]
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    optimal_gamma = 1.0472
    optimal_beta = 0.392699
    exp = 1.64952
    obs = -simulation.analitical_f_1([optimal_gamma, optimal_beta], graph, edges)
    assert_equal(exp, round(obs, 5))