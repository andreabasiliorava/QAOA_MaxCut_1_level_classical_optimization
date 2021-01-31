# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 10:14:48 2021

@author: AndreaB.Rava
"""

import qutip as qu
import qucompsys as qucs


def evaluate_cost_fun(z_str, edges):
    """
    This method evaluates the object function of the MaxCut problem

    Parameters
    ----------
    z_str : string
        input bit string.
    edges : list of tuples
        edges of the graph.

    Returns
    -------
    cost_fun : int
        the integer value the object function.
    """

    cost_fun = 0
    z_list = list(z_str)
    for edge in edges:
        cost_fun += (int(z_list[edge[0]])-int(z_list[edge[1]]))**2
    return cost_fun


def initial_state(n_qubits):
    """
    This method initialize the initial state\n

    Parameters
    ----------
    n_qubits : int
        number of qubits the states is composed of.

    Raises
    ------
    ValueError
        if number of qubits is less than 1.

    Returns
    -------
    init_state : an object of the Qobj class defined in qutip, tensor of n-qubits
        initial state, tensor of n qubits.

    """
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
    """
    This method generates a tensor that apply the mixing hamiltonian of the
        MaxCut problem on a state of n-qubits

    Parameters
    ----------
    n_qubits : int
        number of qubits the states is composed of.

    Raises
    ------
    ValueError
        if number of qubits is less than 2.

    Returns
    -------
    tensor(Qobj)
        a tensor that apply the mixing hamiltonian to a n-qubits state.

    """
    if n_qubits < 2:
        raise ValueError('number of qubits must be > 1, but is {}'.format(n_qubits))
    list_n_sigmax = []
    for i in range(n_qubits):
        list_n_sigmax.append(qucs.n_sigmax(n_qubits,i))
    return sum(list_n_sigmax)


def prob_hamilt(n_qubits, edges):
    """
    This method generates a tensor that apply the problem hamiltonian of the
        MaxCut problem on a state of n-qubits

    Parameters
    ----------
    n_qubits : int
        number of qubits the states is composed of.
    edges : list of tuples
        edges of the graph.

    Raises
    ------
    ValueError
        if number of qubits is less than 2..

    Returns
    -------
    tensor(Qobj)
        a tensor that apply the mixing hamiltonian to a n-qubits state.

    """
    if n_qubits < 2:
        raise ValueError('number of qubits must be > 1, but is {}'.format(n_qubits))
    list_double_sigmaz = []
    for j in range(len(edges)):
        list_double_sigmaz.append(
            qucs.n_sigmaz(n_qubits,edges[j][0])*qucs.n_sigmaz(n_qubits,edges[j][1])
            )
    return 0.5*(len(edges)*qucs.n_qeye(n_qubits)-sum(list_double_sigmaz))


def evolution_operator(n_qubits, edges, gammas, betas):
    """
    This method generates a tensor that apply the evolution operator U of the
    MaxCut problem on a state of n-qubits

    Parameters
    ----------
    n_qubits : int
        n_qubits: number of qubits is the n-qubits state among this operators acts on.
    edges : list of tuples
        edges of the graph.
    gammas : mappable type
        gammas parameters of the MaxCut.
    betas : mappable type
        betas parameters of the MaxCut.

    Raises
    ------
    ValueError
        if number of gammas is less than 1
    ValueError
        if number of betas is less than 1
    ValueError
        if number of betas is different than number of gammas
    ValueError
        if number of qubits is less than 2

    Returns
    -------
    evol_oper : tensor (Qobj)
        tensor representing the evolution operator.

    """
    if len(gammas) < 1:
        raise ValueError('number of gammas must be > 0, but is {}'.format(len(gammas)))
    if len(betas) < 1:
        raise ValueError('number of gammas must be > 0, but is {}'.format(len(betas)))
    if len(betas) != len(gammas):
        raise ValueError('number of gammas must be = number of betas')
    if n_qubits < 2:
        raise ValueError('number of qubits must be > 1, but is {}'.format(n_qubits))
    evol_oper = qucs.n_qeye(n_qubits)
    for i in range(len(gammas)):
        u_mix_hamilt_i = (-complex(0,betas[i])*mix_hamilt(n_qubits)).expm()
        u_prob_hamilt_i = (-complex(0,gammas[i])*prob_hamilt(n_qubits, edges)).expm()
        evol_oper = u_mix_hamilt_i*u_prob_hamilt_i*evol_oper
    return evol_oper
