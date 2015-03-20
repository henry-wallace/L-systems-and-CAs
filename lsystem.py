import turtle
from queue import LifoQueue
from itertools import takewhile
from math import log
from matplotlib.colors import rgb2hex

def eval_rules(rules, niter=10, init='0'):
	""" Evaluates the rules (a dictionary from strings to strings) for niter
	iterations, starting with init as the initial string.
	"""
	seq = init
	for _ in range(niter):
		new_seq = ''
		for c in seq:
			if c in rules:
				try:
					new_seq += rules[c]()
				except TypeError:
					new_seq += rules[c]
			else:
				new_seq += c
		seq = new_seq
	return seq

class Drawer(object):
	""" Base Drawer object initializes a turtle drawer with step size for use in
	forward porportional to screen_x/step_scale, where screen_x is the screen
	size. The position is also scaled similarly. Drawer only needs a sequence and
	a drawing rule dictionary from symbols to lambda functions or tuples of 
	lambda functions.
	"""
	def __init__(self, seq, draw_rules, speed=10, cmap=None, pensize=1, \
			pushpop='[]', margin_scale=1/5, init_angle=90):
		self.seq = seq
		self.draw_rules = draw_rules
		turtle.mode(mode='world')
		turtle.setup(width=400, height=400)
		self.margin_scale = margin_scale
		self.screen = turtle.getscreen()
		self.t = turtle.getturtle()
		self.t.pensize(pensize)
		self.t.speed(speed)
		self.t.setheading(init_angle)
		self.push, self.pop = pushpop
		if cmap is None:
			self.colors = ['black']*len(seq)
		else:
			self.colors = [rgb2hex(c) for c in (cmap(i/len(seq)) for i in \
				range(len(seq)))]

	def _strokes(self, seq, draw_rules, step):
		""" Draws a seq with draw_rules when there is Lifo stacking. """
		queue, depth = LifoQueue(), 0
		for c in seq:
			if c == self.push:
				queue.put((self.t.heading(), self.t.position()))
				depth += 1
			elif c == self.pop:
				heading, pos = queue.get()
				depth -= 1
				self.t.penup()
				self.t.setheading(heading)
				self.t.setpos(pos)
				self.t.pendown()
			if c in draw_rules:
				try:
					draw_rules[c](t=self.t, step=step, depth=depth)
				except:
					raise
					for func in draw_rules[c]:
						func(self.t, step)
			yield

	def draw(self):
		""" Draws the entire sequence according to self.draw_rules. It uses the
		subroutine self.parse_seq to do the drawing.
		"""
		self.t.pencolor(self.colors[0])
		borders = (-1, -1, 1, 1)
		rescale = 1.2
		step = 0.1
		turtle.setworldcoordinates(*borders)
		(xmin, ymin), (xmax, ymax) = self.t.pos(), self.t.pos()
		try:
			for i, _ in enumerate(\
					self._strokes(self.seq, self.draw_rules, step)):
				tx, ty = self.t.pos()
				xmin, ymin, xmax, ymax = min(xmin, tx), min(ymin, ty), \
					max(xmax, tx), max(ymax, ty)
				xdist, ydist = xmax - xmin, ymax - ymin
				maxdist = max(xdist, ydist)
				xhang, yhang = maxdist - xdist, maxdist - ydist
				margin = maxdist*self.margin_scale
				borders = (xmin - (xhang + margin)/2, ymin - (yhang + margin)/2, \
					xmax + (xhang + margin)/2, ymax + (yhang + margin)/2)
				turtle.setworldcoordinates(*borders)
				self.t.pencolor(self.colors[i])
			self.t.hideturtle()
			turtle.done()
		except:
			raise
			turtle.bye()


if __name__ == '__main__':
	pass
