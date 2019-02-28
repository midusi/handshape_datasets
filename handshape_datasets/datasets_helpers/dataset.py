from logging import warning
from math import ceil
from ._utils import show_subsets


class Dataset(object):
    def __init__(self, name, data):
        self.name = name
        self.subsets = data

    def show_info(self):
        warning("The dataset has {} subsets.".format(len(self.subsets.keys())))
        warning(f"The subset/s is/are {'-'.join(self.subsets_names())}")
        show_subsets(self.subsets, images_number=16)

    def subsets_number(self):
        """Returns the number of subsets"""
        return len(self.subsets.keys())

    def subsets_names(self):
        """Returns a list with the subsets names"""
        return list(self.subsets.keys())
