from lsystem import eval_rules
from random import choice
from numpy import arange
from numpy.random import normal

rules = {'1': '11', '0': '1[0[0]]0'}
seq = eval_rules(rules, niter=4, init='0')
draw_rules = {'1': lambda **kw: kw['t'].forward(kw['step']), 
	'[': lambda **kw: kw['t'].left(normal(kw['depth']*0.1, 20)), \
	']': lambda **kw: kw['t'].right(normal(kw['depth']*0.1, 20)), 
	'0': lambda **kw: kw['t'].forward(kw['step']/max(1, normal(kw['depth'], 1e-1)))}
