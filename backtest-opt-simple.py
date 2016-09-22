# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 19:19:54 2016

@author: stn821
"""

import cvxpy
import dccp
import pandas as pd
import numpy as np

df=pd.DataFrame({'pos':[1.0,-1.0,1.0,-1.0,1.0]})
df1=pd.DataFrame({'pos':[1.0,0.0,-1.0,0.0,1.0,0.0,-1.0,0.0,1.0]})

class backtestoptimize(object):
    
    def __init__(self):
        self.cfg_strat_leverage = 2.0
        self.cfg_strat_capital = 100e6
    
    def optimize_pos_basic(self, df):

        w_target = df['pos']/df['pos'].abs().sum()
        w_target = w_target.values
        
        nassets=df.shape[0]
        w = cvxpy.Variable(nassets)
        
        obj = cvxpy.Minimize(cvxpy.norm(w-w_target))
        constraints = [cvxpy.sum_entries(cvxpy.abs(w)) == 1.0]
        constraints += [cvxpy.abs(cvxpy.sum_entries(w)) <= 0.1]
        constraints += [cvxpy.abs(w) <= 1.0/nassets]
        #constraints += [w >= 0]
        prob = cvxpy.Problem(obj, constraints)
        prob.solve(verbose=False, method='dccp')
        
        return np.reshape(w.value, [nassets])
        
    def get_pos_sizing(self, df):
        
        df['weight'] = 0.0
        idx_pos = (df['pos'] != 0.0)
        df.ix[idx_pos, 'weight'] = self.optimize_pos_basic(df.ix[idx_pos])
        
        df['net_dollar_entry'] = df['weight'] * self.cfg_strat_capital * self.cfg_strat_leverage
        
        return df

b=backtestoptimize()
print b.get_pos_sizing(df1) 

