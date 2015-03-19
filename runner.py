import argparse
from lsystem import eval_rules, Drawer
from automaton import plot_rules, Rule
from itertools import chain, takewhile
from palettable.colorbrewer.sequential import *

parser = argparse.ArgumentParser(description='Command-line tool plotting \
	iterative functions.')
parser.add_argument('-l', '--lname', nargs=1, dest='lname', help='Name of \
	l-system, viz.: plant, pythag, koch, dragon, sierp.')
parser.add_argument('-f', '--fromfile', dest='fromfile', action='store_true', \
	help='Filename to retrieve seq, draw_rules and additional Draw kwargs.')
parser.add_argument('-c', '--cname', dest='cname', nargs='+', help="Rule \
	numbers for CA, e.g. '-c 100 102 120-130'.")
parser.add_argument('-n', '--niter', dest='niter', type=int, help='Number of \
	iterations.')
parser.add_argument('-i', '--init', dest='init', nargs='?', \
	help="Initialization for CA, e.g. '-i 0001000'. If unspecified then an \
	array of 2*niter 0s with a 1 in the center will be used.")
parser.add_argument('--cmap', dest='cmap', nargs='*', help='colorbrewer sequential \
	cmap name to be used for drawing the l-system, e.g..: GnBu_7, etc. See \
	https://jiffyclub.github.io/palettable/colorbrewer/sequential/ for more \
	details.')
parser.add_argument('-p', '--pensize', dest='pensize', type=int, default=3, \
	help='Define pensize for l-system drawer in range 1-10.')

args = parser.parse_args()

# L-SYSTEM DRAWING
if args.cmap is not None:
	if args.cmap == []:
		args.cmap = eval('YlOrRd_9').mpl_colormap
	else:
		args.cmap = eval(args.cmap).mpl_colormap

if args.fromfile:
	assert(args.lname[0].endswith('.py'))
	exec('from {} import *'.format(args.lname[0].split('.py')[0]))
	try:
		if 'cmap' not in kwargs: kwargs['cmap'] = args.cmap
		if 'pensize' not in kwargs: kwargs['pensize'] = args.pensize
	except:
		kwargs = {'cmap': args.cmap, 'pensize': args.pensize}
	finally:
		Drawer(seq, draw_rules, **kwargs).draw()
else:
	if args.lname == ['plant']:
		if args.niter is None:
			args.niter = 3	
		plant_rules = {'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'}
		seq = eval_rules(plant_rules, niter=args.niter, init='X')
		draw_rules = {'F': lambda t, step: t.forward(step), 
			'-': lambda t, step: t.left(25), 
			'+': lambda t, step: t.right(25)}
		Drawer(seq, draw_rules, cmap=args.cmap, pensize=args.pensize).draw()
	elif args.lname == ['pythag']:
		if args.niter is None:
			args.niter = 5
		pythag_rules = {'1': '11', '0': '1[0]0'}
		seq = eval_rules(pythag_rules, niter=args.niter, init='0')
		draw_rules = {'1': lambda t, step: t.forward(step), 
			'[': lambda t, step: t.left(45), ']': lambda t, step: t.right(45), 
			'0': lambda t, step: t.forward(step/2)}
		Drawer(seq, draw_rules, cmap=args.cmap, pensize=args.pensize).draw()
	elif args.lname == ['koch']:
		if args.niter is None:
			args.niter = 3
		koch_rules = {'F': 'F+F-F-F+F'}
		seq = eval_rules(koch_rules, niter=args.niter, init='F')
		draw_rules = {'F': lambda t, step: t.forward(step),
			'-': lambda t, step: t.right(90),
			'+': lambda t, step: t.left(90)}
		koch_len = 3**(args.niter - 1)
		Drawer(seq, draw_rules, cmap=args.cmap, pensize=args.pensize, init_angle=0).draw()
	elif args.lname == ['dragon']:
		if args.niter is None:
			args.niter = 6
		dragon_rules = {'X': 'X+YF+', 'Y': '-FX-Y'}
		seq = eval_rules(dragon_rules, niter=args.niter, init='FX')
		draw_rules = {'F': lambda t, step: t.forward(step), 
			'+': lambda t, step: t.right(90), '-': lambda t, step: t.left(90), 
			'X': (), 'Y': ()}
		Drawer(seq, draw_rules, cmap=args.cmap, pensize=args.pensize).draw()
	elif args.lname == ['sierp']:
		if args.niter is None:
			args.niter = 4
		sierpinski_rules = {'A': 'B-A-B', 'B': 'A+B+A'}
		seq = eval_rules(sierpinski_rules, niter=args.niter, init='A')
		draw_rules = {'A': lambda t, step: t.forward(step), 
			'B': lambda t, step: t.forward(step), 
			'+': lambda t, step: t.left(60), '-': lambda t, step: t.right(60)}
		Drawer(seq, draw_rules, cmap=args.cmap, pensize=args.pensize, init_angle=0).draw()

# CA DRAWING
if args.cname is not None:
	if args.niter is None: args.niter = 30
	try:
		rule_groups = [[int(c) for c in x.split('-')] for x in args.cname]
	except ValueError:
		print('Must input rule indices, e.g. -c 100 102 120-130.')
		exit()
	rules = []
	for rg in rule_groups:
		if len(rg) == 2:
			rules += [Rule(i) for i in range(rg[0], rg[1])]
		else:
			rules.append(Rule(rg[0]))
	if args.init is not None:
		init = [int(c) for c in args.init]
	else:
		init = [1 if i == args.niter else 0 for i in range(2*args.niter)]
	plot_rules(init, rules, args.niter)




