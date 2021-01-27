# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 10:14:48 2021

@author: AndreaB.Rava
"""

import numpy as np
import qutip as qu

#method to evaluate object function
def evaluate_obj (z_str, edges):
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

#method to pick initial parameters
def initial_params (n_levels):
    """This method generates randomly the intial parameters near zero
    Parameters:
        n_levels: choosen levels of the QAOA algorithm
    Returns:
        an array with shape 2*n_levels 
    Raise:
        ValueError if number of levels is less than 1"""
    if n_levels < 1:
        raise ValueError('number of levels must be > 0, but is {}'.format(n_levels))
    init_params = 0.01*np.random.rand(2,n_levels)
    return init_params

#method to initialize initial state |s>
def initial_state (n_qubits):
    """This method initialize the initial state
    Parameters:
        n_qubits: number of qubits the states is composed of
    Returns:
        an object of the Qobj class defined in qutip, tensor of n-qubits
    Raise:
        ValueError if number of qubits is less than 1"""
    if n_vertices < 1:
        raise ValueError('number of vertices must be > 0, but is {}'.format(n_qubits))
    list_s = []
    i = 0
    while i < n_qubits:
        list_s.append((qu.basis(2,0) + qu.basis(2,1)).unit())
        i += 1
    init_state = qu.tensor(list_s)
    return init_state

#method to create a list that act as identity operator on a n-qubits state
def n_qeye (n_qubits):
    """This method generates a tensor that apply identity on a state
       of n-qubits
    Parameters:
        n_qubits: number of qubits the states is composed of
    Returns:
        a tensor that apply the identity to a n-qubits state
    Raise:
        ValueError if number of qubits is less than 1"""
    if n_qubits < 1:
        raise ValueError('number of qubits must be > 0, but is {}'.format(n_qubits))
    n_qeye = qu.tensor([qu.qeye(2)]*L)
    return n_qeye

#method to create a tensor which apply sigmax to a qubit of a n-qubits state
def n_sigmax (n_vertices, qubit_pos):
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
    if qubit_pos < 1 or > n_qubits:
        raise ValueError('number of vertices must be > 0 or <= n_qubits, but is {}'.format(qubit_pos))
    n_sigmax = []
    for i in range(n_vertices):
        n_sigmax.append(qu.tensor([qu.qeye(2)]*i+[qu.sigmax()]+[qu.qeye(2)]*(L-i-1)))
    return n_sigmax[qubit_pos]
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