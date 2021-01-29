# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:13:05 2021

@author: AndreaB.Rava
"""

from nose.tools import assert_equal
#import configuration
import numpy as np
from networkx.generators.random_graphs import erdos_renyi_graph
import qutip as qu
#import hypothesis
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
import qaoa
import qucompsys as qucs


#@given(N=st.integers(1,configuration.N), M = st.integers(1,configuration.M))
#@settings(max_examples = 1)
def test_evaluate_obj():
    #test some possible z_str inputs for butterfly graph
    exp = 4
    obs = qaoa.evaluate_obj('00100',
                          [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]
                          )
    assert_equal(exp,obs)
    exp = 0
    obs = qaoa.evaluate_obj('00000',
                          [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]
                          )
    assert_equal(exp,obs)
    exp = 4
    obs = qaoa.evaluate_obj('0101',
                          [(0,1),(1,2),(2,3),(3,0)]
                          )
    assert_equal(exp,obs)

@given(n_levels=st.integers(2,5))
def test_initial_params(n_levels):
    #Initialazing the initial state
    params = qaoa.initial_params(n_levels)
    #Test shape of params
    exp = (2,n_levels)
    obs = params.shape
    assert_equal(exp,obs)

@given(n_qubits=st.integers(1,5))
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

@given(n_qubits=st.integers(2,5))
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


@given(n_qubits=st.integers(2,5))
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


@given(n_qubits=st.integers(2,5),n_levels=st.integers(2,5))
@settings(deadline=None)
def test_evolution_operator(n_qubits, n_levels):
    #generate random parameters
    params = qaoa.initial_params(n_levels)
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
    assert_equal(exp, obs)
    #test if it evolves a state for known parameters
    exp = qu.qload('final_state_simple_graph_p=1')
    obs = qaoa.evolution_operator(3, [(0,1),(1,2)], [1.0], [0.4])*qaoa.initial_state(3)
    


if __name__ == "main":
    pass
