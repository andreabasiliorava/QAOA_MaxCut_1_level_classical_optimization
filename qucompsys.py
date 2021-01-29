# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 01:43:16 2021

@author: AndreaB.Rava
"""
import numpy as np
import qutip as qu

def n_rand_qubits(n_qubits):
    """This method generates a list of random n qubits\n
    Parameters:\n
        n_qubits: number of qubits\n
    Returns:\n
        a list of n qubits\n
    Raise:\n
        ValueError if number of qubits is less than 1"""
    if n_qubits < 1:
        raise ValueError('number of qubits must be > 0, but is {}'.format(n_qubits))
    list_n_rand_qubits = []
    i = 0
    coeffs_real = np.random.random_sample((2,n_qubits))
    coeffs_imm = np.random.random_sample((2,n_qubits))
    basis_elem = np.random.randint(0,2,(2,n_qubits))
    for i in range(n_qubits):
        gen_qubit = (complex(coeffs_real[0][i],coeffs_imm[0][i])*qu.basis(2,basis_elem[0][i])
                     + complex(coeffs_real[1][i],coeffs_imm[1][i])*qu.basis(2,basis_elem[1][i])).unit()
        list_n_rand_qubits.append(gen_qubit)
    return list_n_rand_qubits


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
    return qu.tensor([qu.qeye(2)]*n_qubits)


def n_sigmax(n_qubits, qubit_pos):
    """This method generates a tensor(Qobj) wich perform a single-qubit sigmax operation
       on a state of n-qubits\n
    Parameters:\n
        n_vertices: number of qubits the states is composed of\n
        qubit_pos: qubit on which the sigmax operator acts (position starts at '0')\n
    Returns:\n
        a tensor that apply sigmax on the nth-qubit of a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 2\n
        ValueError if qubit position is < 0 or > n_qubits-1 """
    if n_qubits < 1:
        raise ValueError('number of vertices must be > 0, but is {}'.format(n_qubits))
    if qubit_pos < 0 or qubit_pos > n_qubits-1:
        raise ValueError('qubit position must be > 0 or < n_qubits-1, but is {}'.format(qubit_pos))
    list_n_sigmax = []
    for i in range(n_qubits):
        list_n_sigmax.append(qu.tensor([qu.qeye(2)]*i+[qu.sigmax()]+[qu.qeye(2)]*(n_qubits-i-1)))
    return list_n_sigmax[qubit_pos]


def n_sigmay(n_qubits, qubit_pos):
    """This method generates a tensor(Qobj) wich perform a single-qubit sigmay operation
       on a state of n-qubits\n
    Parameters:\n
        n_vertices: number of qubits the states is composed of\n
        qubit_pos: qubit on which the sigmay operator acts (position starts at '0')\n
    Returns:\n
        a tensor that apply sigmay on the nth-qubit of a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 2\n
        ValueError if qubit position is < 0 or > n_qubits-1 """
    if n_qubits < 1:
        raise ValueError('number of vertices must be > 0, but is {}'.format(n_qubits))
    if qubit_pos < 0 or qubit_pos > n_qubits-1:
        raise ValueError('qubit position must be > 0 or < n_qubits-1, but is {}'.format(qubit_pos))
    list_n_sigmay = []
    for i in range(n_qubits):
        list_n_sigmay.append(qu.tensor([qu.qeye(2)]*i+[qu.sigmay()]+[qu.qeye(2)]*(n_qubits-i-1)))
    return list_n_sigmay[qubit_pos]


def n_sigmaz(n_qubits, qubit_pos):
    """This method generates a tensor(Qobj) wich perform a single-qubit sigmaz operation
       on a state of n-qubits\n
    Parameters:\n
        n_vertices: number of qubits the states is composed of\n
        qubit_pos: qubit on which the sigmaz operator acts (position starts at '0')\n
    Returns:\n
        a tensor that apply sigmaz on the nth-qubit of a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 2\n
        ValueError if qubit position is < 0 or > n_qubits-1 """
    if n_qubits < 1:
        raise ValueError('number of vertices must be > 0, but is {}'.format(n_qubits))
    if qubit_pos < 0 or qubit_pos > n_qubits-1:
        raise ValueError('qubit position must be > 0 or < n_qubits-1, but is {}'.format(qubit_pos))
    list_n_sigmaz = []
    for i in range(n_qubits):
        list_n_sigmaz.append(qu.tensor([qu.qeye(2)]*i+[qu.sigmaz()]+[qu.qeye(2)]*(n_qubits-i-1)))
    return list_n_sigmaz[qubit_pos]


def n_proj0(n_qubits, qubit_pos):
    """This method generates a tensor(Qobj) wich perform a single-qubit projection
        operation on basis state |0> on a state of n-qubits\n
    Parameters:\n
        n_vertices: number of qubits the states is composed of\n
        qubit_pos: qubit on which the projector operator acts (position starts at '0')\n
    Returns:\n
        a tensor that apply the projector on the nth-qubit of a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 2\n
        ValueError if qubit position is < 0 or > n_qubits-1 """
    if n_qubits < 1:
        raise ValueError('number of vertices must be > 0, but is {}'.format(n_qubits))
    if qubit_pos < 0 or qubit_pos > n_qubits-1:
        raise ValueError('qubit position must be > 0 or < n_qubits-1, but is {}'.format(qubit_pos))
    list_n_proj0 = []
    for i in range(n_qubits):
        list_n_proj0.append(qu.tensor([qu.qeye(2)]*i+[qu.ket('0').proj()]+[qu.qeye(2)]*(n_qubits-i-1)))
    return list_n_proj0[qubit_pos]


def n_proj1(n_qubits, qubit_pos):
    """This method generates a tensor(Qobj) wich perform a single-qubit projection
        operation on basis state |1> on a state of n-qubits\n
    Parameters:\n
        n_vertices: number of qubits the states is composed of\n
        qubit_pos: qubit on which the projector operator acts (position starts at '0')\n
    Returns:\n
        a tensor that apply the projector on the nth-qubit of a n-qubits state\n
    Raise:\n
        ValueError if number of qubits is less than 2\n
        ValueError if qubit position is < 0 or > n_qubits-1 """
    if n_qubits < 1:
        raise ValueError('number of vertices must be > 0, but is {}'.format(n_qubits))
    if qubit_pos < 0 or qubit_pos > n_qubits-1:
        raise ValueError('qubit position must be > 0 or < n_qubits-1, but is {}'.format(qubit_pos))
    list_n_proj1 = []
    for i in range(n_qubits):
        list_n_proj1.append(qu.tensor([qu.qeye(2)]*i+[qu.ket('1').proj()]+[qu.qeye(2)]*(n_qubits-i-1)))
    return list_n_proj1[qubit_pos]
