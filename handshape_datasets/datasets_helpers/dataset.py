from logging import warning
from math import ceil
from .utils import show_dataset


class Dataset(object):
    def __init__(self, name, data):
        self.name = name
        self.subsets = data

    def summary(self):
        subset_names = ""

        for i, item in enumerate(self.subsets.items()):
            name, subset = item
            subset_names += '\t{} {}:{} samples\n'.format(
                i+1, name, len(subset))

        n_subsets = len(self.subsets)

        result = "Dataset {}\n{} subsets:\n{}".format(self.name,
                                                      n_subsets,
                                                      subset_names)

        return result

    def show_dataset(self, subsets=None, samples=32):
        if subsets is None:
            subsets = self.subsets.keys()

        show_dataset(self, subsets, samples)
