import matplotlib.pyplot as plt
import numpy as np
from itertools import islice, chain, repeat, zip_longest, product
from matplotlib.animation import FuncAnimation

def find_factorization(x, alpha=1, beta=1):
    """Return the tuple (n, m) that best factorizes x <= n*m such that x - n*m 
    is small and n is close to m. The weights of these two goals are 
    respectively alpha, beta."""
    loss = lambda x, n, m: alpha*abs(x - n*m) + beta*abs(n - m) 
    def solve(x):
        (n_min, m_min), loss_min = (None, None), float('inf')
        for n in range(1, x + 1):
            for m in range(n, x + 1):
                fval = loss(x, n, m)
                if fval < loss_min and x <= n*m:
                    (n_min, m_min), loss_min = (n, m), fval
        return (n_min, m_min)
    return solve(x)

def neighborhoods(it, n, pad=0):
    """Given a 1D iterable it, and neighborhood width n, yields n-gram tuples 
    around each element in it padded with pad, with default 0."""
    padded_it = tuple(chain(repeat(pad, n//2), it, repeat(pad, n//2)))
    for i in range(len(it)):
        yield padded_it[i:i + n]

def binary_digits(n, width):
    """Return n in binary, padded in the front with 0s such that the binary 
    representation has width digits."""
    format_str = '{{:0{}b}}'.format(width)
    return tuple(int(c) for c in format_str.format(n))

def dec2base(n, base, width=0):
    digits = []
    while n > 0:
        digits.append(n % base)
        n //= base
    digits.extend(repeat(0, width - len(digits)))
    return tuple(reversed(digits))

class Rule(object):
    """Rule object is created from an index rule (which can be read in base 2) 
    from a lexicographic ordering of all possible rules with size look 
    around. E.g. if size == 2, and index == 0 then the rule would be 
    (0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0. Rule objects support key 
    lookups."""
    def __init__(self, index, base=2, size=3):
        self.size = size
        self.index = index
        if index == 'random':
            self.dict = {dec2base(i, base, width=size): np.random.randint(base) \
                for i in range(base**size)}
            self.index = sum(v*base**i for i, (k, v) in \
                enumerate(sorted(self.dict.items())))
        else:
            assert(index < base**(base**size))
            targets = dec2base(index, base, width=base**size)
            self.dict = {dec2base(i, base, width=size): t for i, t in \
                enumerate(reversed(targets))}
        
    def __repr__(self):
        return '{' + ',\n'.join('{}: {}'.format(k, v) for k, v in \
            sorted(self.dict.items())) + '}'

    def __getitem__(self, key):
        return self.dict[tuple(np.reshape(key, -1))]    # to allow ndarray keys

# todo: let curr_state be nD matrix
def next_state(curr_state, rule):
    new_state = []
    for pattern in neighborhoods(curr_state, rule.size):
        new_state.append(rule[pattern])
    return new_state

def plot_rules(init, rules, niter, cmap='Greys', view=0):
    """For each rule in rules (an iterable of Rule objects) plot the subplots
    of each rule performed on init for niter iterations."""
    sub_x, sub_y = find_factorization(len(rules))
    fig, axes = plt.subplots(sub_x, sub_y)
    for r, ax in zip_longest(rules, np.reshape(axes, -1)):
        ax.axis('off')
        if r is not None:
            matrix = np.zeros((niter + 1, len(init)))
            matrix[0, :] = init
            for i in range(niter):
                matrix[i + 1, :] = next_state(matrix[i, :], r)
            ax.imshow(matrix[view:, :], interpolation='nearest', cmap=cmap)
            ax.set_title('Rule: {}'.format(r.index))
    plt.show()

def wrapped_ball(A, x, reach):
    """Return the neighborhood of an nD coordinate x within an nD matrix A, 
    where the radius of one axis is reach. Out of bound indices wrap."""
    if reach == 0:
        return A[x]
    offsets = product(range(-reach, reach + 1), repeat=len(x))
    neighbor = lambda c: (sum(t) % A.shape[i] for i, t in enumerate(zip(x, c)))
    indices = zip(*(tuple(neighbor(c)) for c in offsets))
    return A[tuple(indices)]

def nball(A, x, reach=1, wrap=True, pad=0):
    assert(len(x) == len(A.shape))
    def func(*coordinate):
        offset = tuple(a + b - reach for a, b in zip(coordinate, x))
        if wrap:
            return A[tuple(t % A.shape[i] for i, t in enumerate(offset))]
        elif all(0 <= t < A.shape[i] for i, t in enumerate(offset)):
            return A[offset]
        else:
            return pad
    shape = tuple(2*reach + 1 for _ in range(len(A.shape)))
    return np.fromfunction(np.vectorize(func), shape=shape, dtype=A.dtype)

def animate_rules(init, rules, niter):
    """Similar to plot_rules(), animates subpots of each rule in rules."""
    sub_x, sub_y = find_factorization(len(rules))
    fig, axes = plt.subplots(sub_x, sub_y)
    matrices = [np.zeros((niter + 1, len(init))) for _ in range(len(rules))]
    for m in matrices:      # make it such that init can be a list of inits
        m[0, :] = init
    kwargs = {'interpolation': 'nearest', 'cmap': 'Greys'}
    ims = [ax.imshow(m, **kwargs) for m, ax in \
        zip(matrices, np.reshape(axes, -1))]
    def update(i):
        for r, m, im, ax in \
                zip_longest(rules, matrices, ims, np.reshape(axes, -1)):
            ax.axis('off')
            if r is not None:
                m[i + 1, :] = next_state(m[i, :], r)
                im.set_data(m)
                ax.set_title('Rule: {}'.format(r.index))
    ani = FuncAnimation(fig, update, frames=niter, interval=10)
    plt.show()

"""todo: allow rule to be  list of rules, and subdivide areas of axes
to be the different rules"""
def plot_rule_nD(init, rule, niter):
    sub_x, sub_y = find_factorization(niter + 1)
    fig, axes = plt.subplots(sub_x, sub_y)
    kwargs = {'interpolation': 'nearest', 'cmap': 'Greys'}     
    matrix = init   
    for i, ax in enumerate(np.reshape(axes, -1)):
        ax.axis('off')
        if i <= niter + 1:
            ax.imshow(matrix.copy(), **kwargs)
            for index, _ in np.ndenumerate(matrix):
                ball = wrapped_ball(matrix, index, reach=1)
                matrix[index] = rule[tuple(ball)]
    plt.show()

def animate_rules_nD(init, rules, niter, wrap=True):
    sub_x, sub_y = find_factorization(len(rules))
    fig, axes = plt.subplots(sub_x, sub_y)
    matrices = [init.copy() for _ in range(len(rules))]
    kwargs = {'interpolation': 'nearest', 'cmap': 'Greys'}
    ims = [ax.imshow(m, **kwargs) for m, ax in \
        zip(matrices, np.reshape(axes, -1))]
    def update(i):
        for r, m, im, ax in \
                zip_longest(rules, matrices, ims, np.reshape(axes, -1)):
            ax.axis('off')
            if r is not None:
                im.set_data(m)
                for index, _ in np.ndenumerate(m):
                    ball = nball(m, index, reach=1, wrap=wrap)
                    m[index] = r[ball]
                ax.set_title('Rule: {}'.format(r.index))
    ani = FuncAnimation(fig, update, frames=niter, interval=200, repeat=False)
    plt.show()

if __name__ == '__main__':
    pass

    niter = 200
    init = [0] * niter*2
    init[niter] = 1
    plot_rules(init, [Rule(438, base=3)], niter)





