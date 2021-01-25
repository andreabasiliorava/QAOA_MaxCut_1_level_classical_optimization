# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:13:05 2021

@author: AndreaB.Rava
"""

import QAOA
from nose.tools import assert_equal


def test_evaluate_C ():
    exp = 4
    obs = QAOA.evaluate_C('00100',
                          [(0,1),(0,2),(1,2),(2,3),(2,4),(3,4)]
                          )
    assert_equal(exp,obs)

    
        
