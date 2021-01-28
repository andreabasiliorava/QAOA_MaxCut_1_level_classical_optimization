# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 01:46:32 2021

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
import operators


@given(n_qubits=st.integers(2,5))
def test_n_qeye(n_qubits):
    #generate a generic n-qubits state
    dimensions = [[],[]]
    for vertex in range(n_qubits):
        dimensions[0].append(2)
        dimensions[1].append(1) 
    gen_state = qu.rand_ket(2**n_qubits,dims=dimensions)
    #Test if it remain the same after been applied to it n_qeye
    exp = gen_state
    obs = operators.n_qeye(n_qubits)*gen_state
    assert_equal(exp,obs)
    

@given(n_qubits=st.integers(2,5))
def test_n_sigmax(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = []
    i = 0
    coeffs_real = np.random.random((2,n_qubits))
    coeffs_imm = np.random.random((2,n_qubits))
    basis_elem = np.random.randint(0,2,(2,n_qubits))
    while i < n_qubits:
        gen_qubit = (complex(coeffs_real[0][i],coeffs_imm[0][i])*qu.basis(2,basis_elem[0][i])
                     + complex(coeffs_real[1][i],coeffs_imm[1][i])*qu.basis(2,basis_elem[1][i])).unit()
        list_gen_state.append(gen_qubit)
        i += 1
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
    obs = operators.n_sigmax(n_qubits,qubit_pos)*gen_state
    assert_equal(exp, obs)
    
    
@given(n_qubits=st.integers(2,5))
def test_n_sigmay(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = []
    i = 0
    coeffs_real = np.random.random((2,n_qubits))
    coeffs_imm = np.random.random((2,n_qubits))
    basis_elem = np.random.randint(0,2,(2,n_qubits))
    while i < n_qubits:
        gen_qubit = (complex(coeffs_real[0][i],coeffs_imm[0][i])*qu.basis(2,basis_elem[0][i])
                     + complex(coeffs_real[1][i],coeffs_imm[1][i])*qu.basis(2,basis_elem[1][i])).unit()
        list_gen_state.append(gen_qubit)
        i += 1
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
    obs = operators.n_sigmay(n_qubits,qubit_pos)*gen_state
    assert_equal(exp, obs)
    
    
@given(n_qubits=st.integers(2,5))
def test_n_sigmaz(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = []
    i = 0
    coeffs_real = np.random.random((2,n_qubits))
    coeffs_imm = np.random.random((2,n_qubits))
    basis_elem = np.random.randint(0,2,(2,n_qubits))
    while i < n_qubits:
        gen_qubit = (complex(coeffs_real[0][i],coeffs_imm[0][i])*qu.basis(2,basis_elem[0][i])
                     + complex(coeffs_real[1][i],coeffs_imm[1][i])*qu.basis(2,basis_elem[1][i])).unit()
        list_gen_state.append(gen_qubit)
        i += 1
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
    obs = operators.n_sigmaz(n_qubits,qubit_pos)*gen_state
    assert_equal(exp, obs)
    
    
@given(n_qubits=st.integers(2,5))
def test_n_proj0(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = []
    i = 0
    coeffs_real = np.random.random((2,n_qubits))
    coeffs_imm = np.random.random((2,n_qubits))
    basis_elem = np.random.randint(0,2,(2,n_qubits))
    while i < n_qubits:
        gen_qubit = (complex(coeffs_real[0][i],coeffs_imm[0][i])*qu.basis(2,basis_elem[0][i])
                     + complex(coeffs_real[1][i],coeffs_imm[1][i])*qu.basis(2,basis_elem[1][i])).unit()
        list_gen_state.append(gen_qubit)
        i += 1
    gen_state = qu.tensor(list_gen_state)
    #Test if n_proj0 projects qubit in qubit_pos on state |0>
    qubit_pos = np.random.randint(0,n_qubits)
    list_exp = []
    for i in range(n_qubits):
        if i == qubit_pos:
            list_exp.append(qu.ket('0').proj()*list_gen_state[i])
        else:
            list_exp.append(list_gen_state[i])
    exp = qu.tensor(list_exp)
    obs = operators.n_proj0(n_qubits,qubit_pos)*gen_state
    assert_equal(exp, obs)
    
    
@given(n_qubits=st.integers(2,5))
def test_n_proj1(n_qubits):
    #generate a generic n-qubits state
    list_gen_state = []
    i = 0
    coeffs_real = np.random.random((2,n_qubits))
    coeffs_imm = np.random.random((2,n_qubits))
    basis_elem = np.random.randint(0,2,(2,n_qubits))
    while i < n_qubits:
        gen_qubit = (complex(coeffs_real[0][i],coeffs_imm[0][i])*qu.basis(2,basis_elem[0][i])
                     + complex(coeffs_real[1][i],coeffs_imm[1][i])*qu.basis(2,basis_elem[1][i])).unit()
        list_gen_state.append(gen_qubit)
        i += 1
    gen_state = qu.tensor(list_gen_state)
    #Test if n_proj1 projects qubit in qubit_pos on state |1>
    qubit_pos = np.random.randint(0,n_qubits)
    list_exp = []
    for i in range(n_qubits):
        if i == qubit_pos:
            list_exp.append(qu.ket('1').proj()*list_gen_state[i])
        else:
            list_exp.append(list_gen_state[i])
    exp = qu.tensor(list_exp)
    obs = operators.n_proj1(n_qubits,qubit_pos)*gen_state
    assert_equal(exp, obs)