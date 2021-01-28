# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:13:05 2021

@author: AndreaB.Rava
"""

from nose.tools import assert_equal
#import configuration
import numpy as np
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
    for vertex in range(n_qubits):
        exp[0].append(2)
        exp[1].append(1)
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
    exp = qucs.n_sigmax(n_qubits,0)*gen_state
    for i in range(1,n_qubits):
        exp += qucs.n_sigmax(n_qubits,i)*gen_state
    assert_equal(obs,exp)
        
        
if __name__ == "main":
    pass        

        
    
        
