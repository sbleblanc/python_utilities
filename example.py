import numpy as np
from stats import PowersetBuilder
import timeit
import time
from utils.utils_fn import print_progress_bar

for i in range(100):
    print_progress_bar(i, 100, "Processing {}".format(i))
    time.sleep(1)

# x = np.array([0.6, 0.3, 0.1])
# pb = PowersetBuilder(x)
# counter=0
# for prob, s in pb:
#     counter += 1
#     print('{}: {}'.format(prob, s))
#     if counter == 300:
#         break

# x = np.log(x)
# pb = PowersetBuilder(x, log_prob=True)
# for prob, s in pb:
#     print('{}: {}'.format(prob, s))


class Node(object):
    def __init__(self, n, l):
        self.n = n
        self.l = sorted(l)
        self.s = set(l)
        assert len(self.l) == len(self.s)

    def __contains__(self, i):
        return i in self.s

    def __iter__(self):
        return iter(self.l)

    def kids(self):
        if 0 not in self:
            yield Node(self.n, [0] + self.l)
        for i, v in enumerate(self.l):
            if v + 1 not in self and v + 1 < self.n:
                l = self.l[:i] + [v + 1] + self.l[i + 1:]
                yield Node(self.n, l)

    def __repr__(self):
        return repr(self.l)

    def __hash__(self):
        return hash(tuple(self.l))

    def __eq__(self, node):
        return self.l == node.l


def NodeProb(node, lp):
    return sum(lp[i] for i in node)


def SortPowerSet(log_probs, k=None):
    lp = sorted(log_probs, reverse=True)
    prospects = [Node(len(lp), [0])]
    yielded = set()
    while (k is None or len(yielded) < k) and 0 < len(prospects):
        node = prospects.pop()
        yielded.add(node)
        new_prospects = [k for k in node.kids() if k not in yielded]
        unsorted_prospects = set(prospects + new_prospects)
        prospects = sorted(unsorted_prospects, key=lambda node: NodeProb(node, lp))
        prospects = prospects if k is None else prospects[-k:]  # save space (and time while sorting)
        yield node, NodeProb(node, lp)

lp = [-2,-2,-1,-5,-6, -8, -9, -10, -11]
start = timeit.default_timer()
for node in SortPowerSet(lp, k=None): i=0
elapsed = timeit.default_timer() - start
print(elapsed)

print(lp)
pb = PowersetBuilder(np.array(lp), log_prob=True)
start = timeit.default_timer()
for prob, s in pb:
    i=0
    # print('{}: {}'.format(prob, s))
elapsed = timeit.default_timer() - start
print(elapsed)
