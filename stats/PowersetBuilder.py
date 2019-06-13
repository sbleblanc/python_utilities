import heapq as h
import numpy as np


class PowersetBuilder(object):
    """ Iterator building the powerset from a probability vector. Will obtain the next most likely set in linear time."""

    def __init__(self, x, root_size=1, log_prob=False):
        """
        :param x: Probability vector
        :param root_size: Length of the root set
        :param log_prob: Whether "x" is the log-probabilities
        """
        self.log_prob = log_prob
        self.x = -x
        self.n = len(x)
        self.sorted_elements = self.x.argsort()
        self.current_pool = []
        self.pool_set_cache = set()
        self.most_probable_elements = set()
        self.sorted_elements_indices = {se: i for i, se in enumerate(self.sorted_elements)}

        for i in range(len(self.sorted_elements)):
            most_probable_set = frozenset(self.sorted_elements[:i+1])
            self.most_probable_elements.add(most_probable_set)
            if i + 1 == root_size:
                root_set = most_probable_set

        h.heappush(self.current_pool, (-self.__get_element_prob(root_set), root_set))
        self.pool_set_cache.add(root_set)

    def __len__(self):
        return 2 ** self.n - 1

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.current_pool) == 0:
            raise StopIteration
        next_element_p, next_element_s = h.heappop(self.current_pool)

        for sub_element in next_element_s:
            if self.sorted_elements_indices[sub_element] == self.n - 1:
                continue
            se_set = set([sub_element])
            new_element = set(next_element_s.difference(se_set))
            new_element.add(self.sorted_elements[self.sorted_elements_indices[sub_element] + 1])
            if new_element not in self.pool_set_cache and len(new_element) == len(next_element_s):
                self.__add_new_element(new_element)

        if next_element_s not in self.most_probable_elements:
            for se in self.sorted_elements:
                if se in next_element_s:
                    continue
                else:
                    new_element = set(next_element_s)
                    new_element.add(se)
                    if new_element not in self.pool_set_cache:
                        self.__add_new_element(new_element)
                    break

        self.pool_set_cache.remove(next_element_s)
        return -next_element_p, next_element_s

    def __get_element_prob(self, element):
        if self.log_prob:
            return np.array([-(self.x[se]) for se in element]).sum()
        else:
            return np.array([-(self.x[se]) for se in element]).prod()

    def __add_new_element(self, new_element):
        """ Will add the new element set to the pool(and cache) with the appropriate probability
        :param new_element:The new set of elements to add to the pool
        """
        # if self.log_prob:
        #     prob = np.array([-(self.x[se]) for se in new_element]).sum()
        # else:
        #     prob = np.array([-(self.x[se]) for se in new_element]).prod()
        prob = self.__get_element_prob(new_element)
        new_element = frozenset(new_element)
        h.heappush(self.current_pool, (-prob, new_element))
        self.pool_set_cache.add(new_element)
