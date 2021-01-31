# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 12:03:35 2021

@author: AndreaB.Rava
"""

from   networkx.generators.random_graphs import erdos_renyi_graph


def random_graph (n_nodes, prob=0.5):
    """
    This method generate a random graph, with n_nodes and at least one edge

    Parameters
    ----------
    n_nodes : int
        number of nodes of the graph.
    prob : float, optional
        probability, that two edges are linked during the creation, must be in [0, 1].
        The default is 0.5.

    Returns
    -------
    graph : networkx.classes.graph.Graph
        Returns a $G_{n,p}$ random graph, also known as an Erdős-Rényi graph or a binomial graph.
        The $G_{n,p}$ model chooses each of the possible edges with probability 0.5.

    """
    graph = erdos_renyi_graph(n_nodes, prob)
    while len(list(graph.edges)) < 1:
        graph = erdos_renyi_graph(n_nodes, prob)
    return graph

def node_degree(graph, node_u):
    """
    This method gives the degree of a node in a graph

    Parameters
    ----------
    graph : networkx.classes.graph.Graph
        graph defined in the library networkx belonging to the class Graph.
    node_u : int
        node of the graph.

    Returns
    -------
    node_degree : int
        degrre of the node u.

    """
    return len(graph[node_u])

def common_neighbours (graph, node_u, node_v):
    """
    This method return the number of common neighbours of two nodes linked by an edge in a graph

    Parameters
    ----------
    graph : networkx.classes.graph.Graph
        graph defined in the library networkx belonging to the class Graph.
    node_u : int
        node u
    node_v : int
        node v.

    Returns
    -------
    common_neighbours : int
        return number of common neighbours of the nodes u and v.

    """
    common_neigh = 0
    for node_w in graph[node_u]:
        if (node_w in graph[node_v]) and (node_w not in (node_u, node_v)):
            common_neigh +=1
    return common_neigh
