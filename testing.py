# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:13:05 2021

@author: AndreaB.Rava
"""

from nose.tools import assert_equal
#import configuration
import numpy as np
#import qutip as qu
#import hypothesis
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
import qaoa

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
    
@given(n_levels=st.integers(1,5))
def test_initial_params(n_levels):
    #Initialazing the initial state
    params = qaoa.initial_params(n_levels)
    #Test shape of params
    exp = (2,n_levels)
    obs = params.shape
    assert_equal(exp,obs)

#in the given statement we've put max n_qubits for q. computers
@given(n_qubits=st.integers(1,15))
@settings(deadline=None)
def test_initial_state (n_qubits):
    #Initialazing the initial state
    state = qaoa.initial_state(n_vertices) 
    #Test if the shape of the state is (2**n_qubits,1)
    exp = (2**n_qubits,1)
    obs = state.shape
    assert_equal(exp,obs)
    #Test if the dims of the state are of a n_vertices qubits
    exp = [[],[]]
    for vertex in range(n_qubits):
        exp[0].append(2)
        exp[1].append(1)
    obs = state.dims
    assert_equal(exp,obs)
    #Test if the dims of the state are of a n_vertices qubits
    exp = [[],[]]
    vertex = 0
    while vertex < n_qubits:
        exp[0].append(2)
        exp[1].append(1)
        vertex += 1
    obs = state.dims
    assert_equal(exp,obs)
    #Test is the state is a ket
    exp = 'ket'
    obs = state.type
    assert_equal(exp,obs)
    #Test if all coefficients are 1/sqrt(2)**n_verices
    for i in range(2**n_qubits):
        exp = 1/np.sqrt(2)**n_qubits
        obs = np.abs(state.full()[i][0])
        assert_equal(round(exp,15),round(obs,15))
        
@given(n_qubuts=st.integers(1,5))
def test_n_qeye(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = []
    i = 0
    coeffs = np.random.random((2,n_qubits))
    basis_elem = np.random.randint(0,2,(2,n_qubits))
    while i < n_qubits:
        gen_qubit = coeffs[0][i]*qu.basis(2,basis_elem[0][i]) + coeffs[1][i]*qu.basis(2,basis_elem[1][i])
        list_gen_state.append(gen_qubit)
        i += 1
    gen_state = qu.tensor(list_gen_state)
    #Test is it remain the same after been applied to it n_qeye
    exp = gen_state
    obs = qaoa.n_qeye(n_qubits)*gen_state
    assert_equal(exp,obs)

        
if __name__ == "main":
    pass        

        
    
        
