# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 10:14:48 2021

@author: AndreaB.Rava
"""

import numpy as np
import qutip as qu
import qucompsys as qucs


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


def mix_hamilt(n_qubits):
    """This method generates a tensor that apply the mixing hamiltonian of the 
        MaxCut problem on a state of n-qubits\n
    Parameters:\n
        n_qubits: number of qubits the states is composed of\n
    Returns:\n
        a tensor that apply the mixing hamiltonian to a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 2"""
    if n_qubits < 2:
        raise ValueError('number of vertices must be > 1, but is {}'.format(n_qubits))
    list_n_sigmax = []
    for i in range(n_qubits):
        list_n_sigmax.append(qucs.n_sigmax(n_qubits,i))
    return sum(list_n_sigmax)


def prob_hamilt(vertices, edges):
    """This method generates a tensor that apply the problem hamiltonian of the 
        MaxCut problem on a state of n-qubits\n
    Parameters:\n
        vertices: number of vertices of the graph
        edges: list of tuples corresponding to the edges of the graph\n
    Returns:\n
        a tensor that apply the problem hamiltonian to a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 2"""
    if n_qubits < 2:
        raise ValueError('number of vertices must be > 1, but is {}'.format(n_qubits))
    list_double_sigmaz = []
    for j in range(len(edges)):
        list_double_sigmaz.append(qucs.n_sigmaz(vertices,edges[j][0])*qucs.n_sigmaz(vertices,edges[j][1]))
    return 0.5*(len(edges)*qucs.n_qeye(vertices)-sum(list_double_sigmaz))
                                 







