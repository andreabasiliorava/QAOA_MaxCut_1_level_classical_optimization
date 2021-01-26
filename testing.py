# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:13:05 2021

@author: AndreaB.Rava
"""

import qaoa
from nose.tools import assert_equal
#import configuration
import numpy as np
import qutip as qu
import hypothesis
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given

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

#in the given statement we've put max n_qubits for q. computers
@given(n_vertices=st.integers(1,15))
@settings(deadline=4000)
def test_initial_state (n_vertices):
    #Initialazing the initial state"
    state = qaoa.initial_state(n_vertices) 
    #Test if the shape of the state is (2**n_vertices,1)
    exp = (2**n_vertices,1)
    obs = state.shape
    assert_equal(exp,obs)
    #Test if the dims of the state are of a n_vertices qubits
    exp = [[],[]]
    for vertex in range(n_vertices):
        exp[0].append(2)
        exp[1].append(1)
    obs = state.dims
    assert_equal(exp,obs)
    #Test if the dims of the state are of a n_vertices qubits
    exp = [[],[]]
    for vertex in range(n_vertices):
        exp[0].append(2)
        exp[1].append(1)
    obs = state.dims
    assert_equal(exp,obs)
    #Test is the state is a ket
    exp = 'ket'
    obs = state.type
    assert_equal(exp,obs)
    #Test if all coefficients are 1/sqrt(2)**n_verices
    for i in range(2**n_vertices):
        exp = 1/np.sqrt(2)**n_vertices
        obs = np.abs(state.full()[i][0])
        assert_equal(round(exp,15),round(obs,15))
    
    
        
