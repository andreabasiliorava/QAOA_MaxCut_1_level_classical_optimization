# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 10:14:48 2021

@author: AndreaB.Rava
"""

import numpy as np
import qutip as qu


def evaluate_obj(z_str, edges):
    """This method evaluates the object function of the MaxCut problem
    Parameters
        z_str : input bit string
        edges : edges of the graph
    Returns
        the integer value the object function"""
    obj = 0
    z_list = list(z_str)
    for edge in edges:
        obj += (int(z_list[edge[0]])-int(z_list[edge[1]]))**2
    return obj


def initial_params(n_levels):
    """This method generates randomly the intial parameters near zero\n
    Parameters:\n
        n_levels: choosen levels of the QAOA algorithm\n
    Returns:\n
        an array with shape 2*n_levels (gammas and betas)\n
    Raise:\n
        ValueError if number of levels is less than 1"""
    if n_levels < 1:
        raise ValueError('number of levels must be > 0, but is {}'.format(n_levels))
    init_params = 0.01*np.random.rand(2, n_levels)
    return init_params


def initial_state(n_qubits):
    """This method initialize the initial state\n
    Parameters:\n
        n_qubits: number of qubits the states is composed of\n
    Returns:\n
        an object of the Qobj class defined in qutip, tensor of n-qubits\n
    Raise:\n
        ValueError if number of qubits is less than 1"""
    if n_qubits < 1:
        raise ValueError('number of vertices must be > 0, but is {}'.format(n_qubits))
    list_s = []
    i = 0
    while i < n_qubits:
        list_s.append((qu.basis(2, 0) + qu.basis(2, 1)).unit())
        i += 1
    init_state = qu.tensor(list_s)
    return init_state


def generic_state(n_qubits):
    """This method initialize the a genric n-qubits state\n
    Parameters:\n
        n_qubits: number of qubits the states is composed of\n
    Returns:\n
        an object of the Qobj class defined in qutip, tensor of n-qubits\n
    Raise:\n
        ValueError if number of qubits is less than 1"""
    list_gen_state = []
    i = 0
    coeffs = np.random.random((2,n_qubits))
    basis_elem = np.random.randint(0,2,(2,n_qubits))
    while i < n_qubits:
        gen_qubit = (coeffs[0][i]*qu.basis(2,basis_elem[0][i])
                     + coeffs[1][i]*qu.basis(2,basis_elem[1][i])).unit()
        list_gen_state.append(gen_qubit)
        i += 1
    gen_state = qu.tensor(list_gen_state)


def n_qeye(n_qubits):
    """This method generates a tensor that apply identity on a state\n
       of n-qubits
    Parameters:\n
        n_qubits: number of qubits the states is composed of\n
    Returns:\n
        a tensor that apply the identity to a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 1"""
    if n_qubits < 1:
        raise ValueError('number of qubits must be > 0, but is {}'.format(n_qubits))
    n_qeye = qu.tensor([qu.qeye(2)]*n_qubits)
    return n_qeye


def n_sigmax(n_vertices, qubit_pos):
    """This method generates a tenosor(Qobj) wich perform a single-qubit sigmax operation
       on a state of n-qubits\n
    Parameters:\n
        n_vertices: number of qubits the states is composed of\n
        qubit_pos: qubit on which the sigmax operator acts\n
    Returns:\n
        a list of n_vertex elements, each is an operator of the qutip class Qobj\n
    Raise:\n
        ValueError if number of qubits is less than 1\n
        ValueError if qubit position is < 1 or > n_qubits """
    if n_qubits < 1:
        raise ValueError('number of vertices must be > 0, but is {}'.format(n_qubits))
    if qubit_pos < 1 or qubit_pos > n_qubits:
        raise ValueError('number of vertices must be > 0 or <= n_qubits, but is {}'.format(qubit_pos))
    n_sigmax = []
    for i in range(n_vertices):
        n_sigmax.append(qu.tensor([qu.qeye(2)]*i+[qu.sigmax()]+[qu.qeye(2)]*(L-i-1)))
    return n_sigmax[qubit_pos]


"""
Y = []
for i in range(L):
    Y.append(qu.tensor([qu.qeye(2)]*i+[qu.sigmay()]+[qu.qeye(2)]*(L-i-1)))
Z = []
for i in range(L):
    Z.append(qu.tensor([qu.qeye(2)]*i+[qu.sigmaz()]+[qu.qeye(2)]*(L-i-1)))
P0 = []
for i in range(L):
    P0.append(qu.tensor([qu.qeye(2)]*i + [qu.ket('0').proj()] + [qu.qeye(2)]*(L-i-1))) 
P1 = []
for i in range(L):
    P1.append(qu.tensor([qu.qeye(2)]*i + [qu.ket('1').proj()] + [qu.qeye(2)]*(L-i-1))) 
"""