# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 12:27:15 2021

@author: AndreaB.Rava
"""

import graphs as gr
from nose.tools import assert_equal
#import configuration
import numpy as np
import qutip as qu
#import hypothesis
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
import qucompsys as qucs
import networkx as nx

@given(n_nodes=st.integers(2,5))
def test_random_graph(n_nodes):
    # test if random_graph has n_nodes
    obs = len(list(gr.random_graph(n_nodes).nodes))
    exp = n_nodes
    assert_equal(exp, obs)
    # test if has at leat one edge
    obs = len(list(gr.random_graph(n_nodes).edges))
    assert obs > 0
    
    
def test_node_degree():
    #test for a know graph the expected degrees
    nodes = [0, 1, 3]
    edges = [(0,1),(1,2)]
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    assert 1 == gr.node_degree(graph, 0)
    assert 2 == gr.node_degree(graph, 1)
    assert 1 == gr.node_degree(graph, 2)