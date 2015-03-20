from lsystem import eval_rules, Drawer

pythag_rules = {'1': '11', '0': '1[0]0'}
pythag_draw_rules = {'1': lambda **kws: kws['t'].forward(kws['step']), 
        '[': lambda **kws: kws['t'].left(45), ']': lambda **kws: kws['t'].right(45), 
        '0': lambda **kws: kws['t'].forward(kws['step']/2)}
niter = 5
pythag_seq = eval_rules(pythag_rules, niter, init='0')
Drawer(pythag_seq, pythag_draw_rules).draw()