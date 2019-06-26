import numpy as np
from python_utilities.stats import PowersetBuilder
from python_utilities.parsers.fce import extract_original_text_to_file, extract_original_text

# extract_original_text('/home/user1/Documents/Research/Corpus/FCE/fce-released-dataset/dataset/0102_2000_6/doc883.xml')
extract_original_text_to_file('fce_original.txt', '/home/user1/Documents/Research/Corpus/FCE/fce-released-dataset/dataset')


# x = np.array([0.04, 0.16, 0.5, 0.3])
# pb = PowersetBuilder(x, root_size=3)
# for prob, s in pb:
#     print('{}: {}'.format(prob, s))
#
# x = np.log(x)
# pb = PowersetBuilder(x, root_size=3, log_prob=True)
# for prob, s in pb:
#     print('{}: {}'.format(prob, s))
