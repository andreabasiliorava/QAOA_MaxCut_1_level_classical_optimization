# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 12:27:15 2021

@author: AndreaB.Rava
"""

import graphs as gr
from nose.tools import assert_equal
#import configuration
import numpy as np
import qutip as qu
#import hypothesis
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given
import qucompsys as qucs

@given(n_nodes=st.integers(1,5))
def test_random_graph(n_nodes):
    # test if random_graph has n_nodes
    obs = gr.random_graph(n_nodes).nodes
    exp = n_nodes
    assert_equal(exp, obs)
    # test if has at leat one edge
    #obs = len(list(gr.random_graph(n_nodes).edges))
    #assert obs > 0