import matplotlib.pyplot as plt
import numpy as np
from itertools import islice, chain, repeat, zip_longest, product
import matplotlib.animation as animation

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
    padded_it = chain(repeat(pad, n//2), it, repeat(pad, n//2))
    yield tuple(chain(repeat(pad, n//2), it[:n//2 + 1]))
    yield from zip(*(it[i:] for i in range(n)))
    yield tuple(chain(repeat(pad, n//2), it[:n//2 + 1]))


def binary_digits(n, width):
    """Return n in binary, padded in the front with 0s such that the binary 
    representation has width digits."""
    format_str = '{{:0{}b}}'.format(width)
    return tuple(int(c) for c in format_str.format(n))

class Rule(object):
    """Rule object is created from an index rule (which can be read in base 2) 
    from a lexicographic ordering of all possible rules with neighbors look 
    around. E.g. if neighbors == 2, and index == 0 then the rule would be 
    (0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0. Rule objects support key 
    lookups."""
    def __init__(self, index, neighbors=3):
        assert(index < 2**(2**neighbors))
        self.index = index
        self.neighbors = neighbors
        targets = binary_digits(index, 2**neighbors)
        self.dict = {binary_digits(i, neighbors): t for i, t in \
            enumerate(targets)}
        
    def __repr__(self):
        return '{' + ', '.join('{}: {}'.format(k, v) for k, v in \
            sorted(self.dict.items())) + '}'

    def __getitem__(self, key):
        return self.dict[key]

def plot_rules(init, rules, niter):
    """For each rule in rules (an iterable of Rule objects) plot the subplots
    of each rule performed on init for niter iterations."""
    sub_x, sub_y = find_factorization(len(rules))
    fig, axes = plt.subplots(sub_x, sub_y)
    for r, ax in zip_longest(rules, np.reshape(axes, -1)):
        if r is None:
            ax.axis('off')
        else:
            matrix = np.zeros((niter + 1, len(init)))
            matrix[0, :] = init
            for i in range(niter):
                curr_state = matrix[i , :]
                new_state = []
                for pattern in neighborhoods(curr_state, r.neighbors):
                    new_state.append(r[pattern])
                matrix[i + 1, :] = new_state
            ax.imshow(matrix, interpolation='nearest', cmap='Greys', \
                aspect='equal')
            ax.axis('off')
            ax.set_title('Rule: {}'.format(r.index))
            ax.set_aspect('equal')
    plt.show()

def wrapped_neighbood(A, x, reach):
    """Return the neighborhood of an nD coordinate within an nD matrix A, where
    the radius of one axis is reach. OUt of bound indices wrap."""
    offsets = product(range(-reach, reach - 1), repeat=len(x))
    neighbor = lambda c: (sum(t) % A.shape[i] for i, t in enumerate(zip(x, c)))
    indices = zip(*(tuple(neighbor(c)) for c in offsets))
    return A[tuple(indices)]

def plot2D():
    """To-do."""
    pass

if __name__ == '__main__':
    A = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    print(wrapped_neighbood(A, (3, 3), 1))


