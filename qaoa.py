# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 10:14:48 2021

@author: AndreaB.Rava
"""

import numpy as np
import qutip as qu
import qucompsys as qucs
import graphs as gr


def evaluate_cost_fun(configuration, edges):
    """
    This method evaluates the object function of the MaxCut problem

    Parameters
    ----------
    configuration : string or 1-D array-like element
        input mappable element with configuration informations.
    edges : list of tuples
        edges of the graph.

    Returns
    -------
    cost_fun : int
        the integer value the object function.
    """

    cost_fun = 0
    z_list = list(configuration)
    for edge in edges:
        cost_fun += (int(z_list[edge[0]])-int(z_list[edge[1]]))**2
    return cost_fun


def analitical_f_1(gamma, beta, graph, edges):
    """
    This function returns the value of the estimated cost function for specific
    gamma and beta of a given graph (with opposite sign)

    Parameters
    ----------
    parameters : numpy.ndarray
        1-D array containing the parameters of the function.
    graph : networkx.classes.graph.Graph
        graph defined in the library networkx belonging to the class Graph.
    edges : list of tuples
        edges of the graph.

    Returns
    -------
    -f_1: float
        estimated cost function with opposite sign.

    """
    f_1 = 0
    for edge in edges:
        degree_u = gr.node_degree(graph, edge[0])
        degree_v = gr.node_degree(graph, edge[1])
        lambda_uv = gr.common_neighbours(graph, edge[0], edge[1])
        c_uv = 0.5+0.25*np.sin(4*beta)*np.sin(gamma)*(np.cos(gamma)**(degree_u-1) + np.cos(gamma)**(degree_v-1))-0.25*np.sin(beta)**2*np.cos(gamma)**(degree_u+degree_v-2-2*lambda_uv)*(1-np.cos(2*gamma)**lambda_uv)
        f_1 += c_uv
    return f_1


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

def grid_search(function, args=(), interval=(0.0, np.pi), step_size=0.01):
    """
    This method find the maximum of an analitic function with two parameters with
    a search grid method.

    Parameters
    ----------
    function : function
        two parameters function which is to be maximized.
    args : tuple, optional
        arguments of the function in addition to the two parameters, if there's any. The default is ().
    interval : tuple, optional
        interval of the range of the parameters of the grid search. The default is (0.0, np.pi).
    step_size : float, optional
        step size of the grid search. The default is 0.01.

    Returns
    -------
    optimal_par1 : float
        optimal paramets 1.
    optimal_par2 : flaot
        optimal parameter 2.

    """
    if not isinstance(args, tuple):
        args = (args,)
    a_par1         = np.arange(interval[0], interval[1], step_size)
    a_par2        = np.arange(interval[0], interval[1], step_size)
    a_par1, a_par2 = np.meshgrid(a_par1, a_par2, indexing='xy')
    grid_f_1 = function(a_par1, a_par2, *args)
    result = np.where(grid_f_1 == np.amax(grid_f_1))
    a      = list(zip(result[0],result[1]))[0]
    optimal_par1   = a[1]*step_size
    optimal_par2  = a[0]*step_size
    return optimal_par1, optimal_par2