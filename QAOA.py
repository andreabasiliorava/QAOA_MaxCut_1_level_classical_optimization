# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:12:05 2021

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

#method to initialize initial state |s>
def initial_state (n_vertices):
    """This method initialize the intial state
    Parameters
        n_vertices: number of qubits the states is composed of
    Returns
        an object of the Qobj class defined in qutip, tensor of n-qubits"""
    list_s = []
    for i in range(n_vertices):
        list_s.append((qu.basis(2,0) + qu.basis(2,1)).unit())
    init_state = qu.tensor(list_s) 
    return init_state


