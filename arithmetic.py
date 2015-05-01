from random import choice
from itertools import product, repeat
from functools import partial
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt

plt.style.use('ggplot')

def primesfrom2to(n):
    # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    assert(n >= 6)
    sieve = np.ones(n//3 + (n % 6 == 2), dtype=np.bool)
    sieve[0] = False
    for i in range(int(n**0.5)//3 + 1):
        if sieve[i]:
            k = (3*i + 1) | 1
            sieve[((k*k)//3) :: 2*k] = False
            sieve[(k*k + 4*k - 2*k*(i & 1))//3 :: 2*k] = False
    return np.r_[2, 3, ((3*np.nonzero(sieve)[0] + 1) | 1)]

def get_graph(f, p):
	graph = {}
	for x in range(p):
		graph[x] = f(x) % p
	return graph

def ncomponents(graph):
	t = 1
	pool = set(graph.keys())
	node = None
	while pool:
		if node is None:
			node = pool.pop()	
		else:
			node = graph[node]
			if node not in pool:
				node = None
				t += 1
			else:
				pool.remove(node)
	return t

def avg_components(p, deg):
	a = []
	for coefs in product(*repeat(range(p), deg + 1)):
		f = lambda x: sum(c*x**i for i, c in enumerate(coefs))
		a.append(ncomponents(get_graph(f, p)))
	return np.mean(a)

def collect_avgs(deg, plist, processes=None):
	if processes is None:
		processes = max(1, mp.cpu_count() - 1)
	pool = mp.Pool(processes=processes)
	avgs = pool.map(partial(avg_components, deg=deg), plist)
	return avgs

def plot_avgs(deg, max_p):
	primes = primesfrom2to(max_p)
	plt.plot(primes, collect_avgs(deg, primes), '-o')
	plt.xticks(primes, rotation=30, ha='right')
	plt.title('Mean components, degree: {}'.format(deg))
	plt.ylabel('mean components')
	plt.xlabel('polynomial modulus')
	plt.show()


if __name__ == '__main__':
	plot_avgs(deg=1, max_p=100)




