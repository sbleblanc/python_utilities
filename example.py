import numpy as np
from stats import PowersetBuilder

x = np.array([0.04, 0.16, 0.5, 0.3])
pb = PowersetBuilder(x)
for prob, s in pb:
    print('{}: {}'.format(prob, s))

x = np.log(x)
pb = PowersetBuilder(x, log_prob=True)
for prob, s in pb:
    print('{}: {}'.format(prob, s))
