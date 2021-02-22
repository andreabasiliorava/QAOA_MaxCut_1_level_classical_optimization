# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 17:58:47 2021

@author: AndreaB.Rava
"""

import numpy as np
import networkx as nx
from networkx.generators.random_graphs import erdos_renyi_graph
import qutip as qu
from nose.tools import assert_equal
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
import qaoa
import qucompsys as qucs
import graphs as gr


def test_evaluate_cost_fun():
    #test some possible z_str inputs for butterfly graph
    exp = 4
    obs = qaoa.evaluate_cost_fun('00100',
                          [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]
                          )
    assert_equal(exp,obs)
    exp = 0
    obs = qaoa.evaluate_cost_fun('00000',
                          [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]
                          )
    assert_equal(exp,obs)
    exp = 4
    obs = qaoa.evaluate_cost_fun('0101',
                          [(0,1),(1,2),(2,3),(3,0)]
                          )
    assert_equal(exp,obs)


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
    obs = qaoa.analitical_f_1(optimal_gamma, optimal_beta, graph, edges)
    assert_equal(exp, round(obs, 5))


@given(n_qubits=st.integers(1,8))
@settings(deadline=None)
def test_initial_state(n_qubits):
    #Initialazing the initial state
    state = qaoa.initial_state(n_qubits)
    #Test if the shape of the state is (2**n_qubits,1)
    exp = (2**n_qubits,1)
    obs = state.shape
    assert_equal(exp,obs)
    #Test if the dims of the state are of a n_vertices qubits
    exp = [[],[]]
    i=0
    while i < n_qubits:
        exp[0].append(2)
        exp[1].append(1)
        i+=1
    obs = state.dims
    assert_equal(exp,obs)
    #Test if the state is a ket
    exp = 'ket'
    obs = state.type
    assert_equal(exp,obs)
    #Test if all coefficients are 1/sqrt(2)**n_verices
    for i in range(2**n_qubits):
        exp = 1/np.sqrt(2)**n_qubits
        obs = np.abs(state.full()[i][0])
        assert_equal(round(exp,15),round(obs,15))

@given(n_qubits=st.integers(2,8))
@settings(deadline=None)
def test_mix_hamilt(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = qucs.n_rand_qubits(n_qubits)
    gen_state = qu.tensor(list_gen_state)
    #test is ìf the result is the one expected
    obs = qaoa.mix_hamilt(n_qubits)*gen_state
    list_exp = []
    for i in range(0,n_qubits):
        list_exp.append(qucs.n_sigmax(n_qubits,i)*gen_state)
    exp = sum(list_exp)
    assert_equal(obs,exp)


@given(n_qubits=st.integers(2,8))
@settings(deadline=None)
def test_prob_hamilt(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = qucs.n_rand_qubits(n_qubits)
    gen_state = qu.tensor(list_gen_state)
    #generate a random graph of n-vertices
    edges = []
    while len(edges) < 1:
        prob = 0.5
        graph = erdos_renyi_graph(n_qubits, prob)
        edges = list(graph.edges)
    #test is ìf the result is the one expected
    obs = qaoa.prob_hamilt(n_qubits,edges)*gen_state
    list_exp = []
    for j in range(0,len(edges)):
        list_exp.append(0.5*(qucs.n_qeye(n_qubits)
               -qucs.n_sigmaz(n_qubits,edges[j][0])*qucs.n_sigmaz(n_qubits,edges[j][1]))*gen_state)
    exp = sum(list_exp)
    assert_equal(obs,exp)


@given(n_qubits=st.integers(2,8),n_levels=st.integers(2,5))
@settings(deadline=None)
def test_evolution_operator(n_qubits, n_levels):
    #generate random parameters
    params = 0.01*np.random.rand(2, n_levels)
    gammas = params[0]
    betas = params[1]
    #generate random graph
    edges = []
    while len(edges) < 1:
        prob = 0.5
        graph = erdos_renyi_graph(n_qubits, prob)
        edges = list(graph.edges)
    #generate random n-qubits state
    list_gen_state = qucs.n_rand_qubits(n_qubits)
    gen_state = qu.tensor(list_gen_state)
    #Test if it works as expected
    obs = qaoa.evolution_operator(n_qubits, edges, gammas, betas)*gen_state
    exp = gen_state
    for i in range(len(gammas)):
        u_mix_hamilt_i = (-complex(0,betas[i])*qaoa.mix_hamilt(n_qubits)).expm()
        u_prob_hamilt_i = (-complex(0,gammas[i])*qaoa.prob_hamilt(n_qubits, edges)).expm()
        exp = u_mix_hamilt_i*u_prob_hamilt_i*exp
    assert (np.round(np.array(exp.full()), 8) == (np.round(np.array(obs.full()), 8))).all()
    #test if it evolves a state for known parameters
    exp = qu.qload('final_state_simple_graph_p=1')
    obs = qaoa.evolution_operator(3, [(0,1),(1,2)], [1.0], [0.4])*qaoa.initial_state(3)


@given(n_qubits=st.integers(1,8))
@settings(deadline=None)
def test_n_ranf_qubits(n_qubits):
    #Initialazing the initial state
    list_qubits = qucs.n_rand_qubits(n_qubits)
    #Test if the shape of each qubit is (2,1)
    for i in range(n_qubits):
        exp = (2,1)
        obs = list_qubits[i].shape
        assert_equal(exp,obs)
    #Test if each qubit is a ket
    for i in range(n_qubits):
        exp = 'ket'
        obs = list_qubits[i].type
        assert_equal(exp,obs)


@given(n_qubits=st.integers(2,8))
@settings(deadline=None)
def test_n_qeye(n_qubits):
    #generate a generic n-qubits state
    dimensions = [[],[]]
    i = 0
    while i < n_qubits:
        dimensions[0].append(2)
        dimensions[1].append(1)
        i+=1
    gen_state = qu.rand_ket(2**n_qubits,dims=dimensions)
    #Test if it remain the same after been applied to it n_qeye
    exp = gen_state
    obs = qucs.n_qeye(n_qubits)*gen_state
    assert_equal(exp,obs)


@given(n_qubits=st.integers(2,8))
@settings(deadline=None)
def test_n_sigmax(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = qucs.n_rand_qubits(n_qubits)
    gen_state = qu.tensor(list_gen_state)
    #Test if n_sigmax applies sigmax on qubit in qubit_pos
    qubit_pos = np.random.randint(0,n_qubits)
    list_exp = []
    for i in range(n_qubits):
        if i == qubit_pos:
            list_exp.append(qu.sigmax()*list_gen_state[i])
        else:
            list_exp.append(list_gen_state[i])
    exp = qu.tensor(list_exp)
    obs = qucs.n_sigmax(n_qubits,qubit_pos)*gen_state
    assert_equal(exp, obs)


@given(n_qubits=st.integers(2,8))
@settings(deadline=None)
def test_n_sigmay(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = qucs.n_rand_qubits(n_qubits)
    gen_state = qu.tensor(list_gen_state)
    #Test if n_sigmay applies sigmay on qubit in qubit_pos
    qubit_pos = np.random.randint(0,n_qubits)
    list_exp = []
    for i in range(n_qubits):
        if i == qubit_pos:
            list_exp.append(qu.sigmay()*list_gen_state[i])
        else:
            list_exp.append(list_gen_state[i])
    exp = qu.tensor(list_exp)
    obs = qucs.n_sigmay(n_qubits,qubit_pos)*gen_state
    assert_equal(exp, obs)


@given(n_qubits=st.integers(2,8))
@settings(deadline=None)
def test_n_sigmaz(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = qucs.n_rand_qubits(n_qubits)
    gen_state = qu.tensor(list_gen_state)
    #Test if n_sigmaz applies sigmaz on qubit in qubit_pos
    qubit_pos = np.random.randint(0,n_qubits)
    list_exp = []
    for i in range(n_qubits):
        if i == qubit_pos:
            list_exp.append(qu.sigmaz()*list_gen_state[i])
        else:
            list_exp.append(list_gen_state[i])
    exp = qu.tensor(list_exp)
    obs = qucs.n_sigmaz(n_qubits,qubit_pos)*gen_state
    assert_equal(exp, obs)


@given(n_nodes=st.integers(2,8))
@settings(deadline=None)
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
    nodes = [0, 1, 2]
    edges = [(0,1),(1,2)]
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    assert gr.node_degree(graph, 0) == 1
    assert gr.node_degree(graph, 1) == 2
    assert gr.node_degree(graph, 2) == 1


def test_common_neighbours():
    #test for a know graph the expected degrees
    nodes = [0, 1, 2, 3]
    edges = [(0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    assert gr.common_neighbours(graph, 0, 2) == 1
    assert gr.common_neighbours(graph, 0, 3) == 1
    assert gr.common_neighbours(graph, 1, 2) == 1
    assert gr.common_neighbours(graph, 1, 3) == 1
    assert gr.common_neighbours(graph, 2, 3) == 2


@given(n_qubits=st.integers(2,5))
def test_comp_basis_prob_dist(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = qucs.n_rand_qubits(n_qubits)
    gen_state = qu.tensor(list_gen_state)
    #Test that, gor a generic qstate, sum probabilities is 1
    exp = 1.0
    obs = round(sum(qucs.comp_basis_prob_dist(gen_state)), 14)
    assert_equal(exp, obs)


def test_grid_search():
    #test that it find known optimal parameters for a graph
    nodes = [0, 1, 2]
    edges = [(0,1),(1,2)]
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    exp = 1.05, 0.39
    obs = qaoa.grid_search(qaoa.analitical_f_1,(graph, edges))
    assert_equal(exp, obs)
    #test for 2D parabola
    exp = 0.00, 0.00
    obs = qaoa.grid_search(lambda x, y : -x**2 + -y*2)
    assert_equal(exp, obs)
