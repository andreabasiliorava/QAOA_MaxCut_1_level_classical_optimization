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
        raise ValueError('number of qubits must be > 0, but is {}'.format(n_qubits))
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
        raise ValueError('number of qubits must be > 1, but is {}'.format(n_qubits))
    list_n_sigmax = []
    for i in range(n_qubits):
        list_n_sigmax.append(qucs.n_sigmax(n_qubits,i))
    return sum(list_n_sigmax)


def prob_hamilt(n_qubits, edges):
    """This method generates a tensor that apply the problem hamiltonian of the 
        MaxCut problem on a state of n-qubits\n
    Parameters:\n
        vertices: number of vertices of the graph
        edges: list of tuples corresponding to the edges of the graph\n
    Returns:\n
        a tensor that apply the problem hamiltonian to a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 2"""
    if n_vertices < 2:
        raise ValueError('number of qubits must be > 1, but is {}'.format(n_qubits))
    list_double_sigmaz = []
    for j in range(len(edges)):
        list_double_sigmaz.append(qucs.n_sigmaz(n_vertices,edges[j][0])*qucs.n_sigmaz(n_qubits,edges[j][1]))
    return 0.5*(len(edges)*qucs.n_qeye(n_qubits)-sum(list_double_sigmaz))


def evolution_operator(n_qubits, edges, gammas, betas):
    """
    This method generates a tensor that apply the evolution operator U of the 
        MaxCut problem on a state of n-qubits\n
    Parameters:\n
        n_qubits: number of qubits is the n-qubits state among this operators acts on\n
        edges: edges of the graph of the MaxCut that define the problem hamiltonian
        gammas: gamma parameters of the MaxCut\n
        betas: betas parameters of the MaxCut\n
    Returns:\n
        a tensor that apply the evolution operator to a n-qubits state\n
    Raise:\n
        ValueError if number of gammas is less than 1\n
        ValueError if number of betas is less than 1\n
        ValueError if number of betas is different than number of gammas\n
        ValueError if number of qubits is less than 2        
    """
    if len(gammas) < 1:
        raise ValueError('number of gammas must be > 0, but is {}'.format(len(gammas)))
    if len(betas) < 1:
        raise ValueError('number of gammas must be > 0, but is {}'.format(len(betas)))
    if len(betas) != len(gamma):
        raise ValueError('number of gammas must be = number of betas, but they are {}'.format(len(betas),len(gammas)))
    if n_qubits < 2:
        raise ValueError('number of qubits must be > 1, but is {}'.format(n_qubits))
    evol_oper = n_qeye(n_qubits)
    for i in range(len(gammas)):
        u_mix_hamilt_i = (-complex(0,betas[i])*mix_hamilt(n_qubits)).expm()
        u_prob_hamilt_i = (-complex(0,gammas[i])*prob_hamilt(n_qubits, edges)).expm()
        evol_oper = u_mix_hamilt_i*u_prob_hamilt_i*evol_oper
    return evol_oper



        
    
                             







