from lsystem import *
from random import choice
from numpy import arange
from numpy.random import normal

rules = {'1': '11', '0': '1[0][0[0]]0'}
seq = eval_rules(rules, niter=4	, init='0')
draw_rules = {'1': lambda t, step: t.forward(step/normal(3, 0.1)), 
	'[': lambda t, step: t.left(normal(45, 15)), \
	']': lambda t, step: t.right(normal(45, 15)), 
	'0': lambda t, step: t.forward(step/normal(5, 0.1))}
