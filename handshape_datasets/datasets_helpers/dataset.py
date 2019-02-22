from logging import warning
from math import ceil
from ._utils import show_images

import random


class Dataset(object):
    def __init__(self, name, data):
        self.name = name
        self.subsets = data

    def show_info(self):
        warning("The dataset has {} subsets.".format(len(self.subsets.keys())))
        images_to_show = []
        names = []
        for name in self.subsets.keys():
            images_to_show.append(
                self.subsets[name][random.randint(0, len(self.subsets[name]))])
            names.append(name)
        columns_quantity = ceil(len(names)/4)  # 4 images per column. Rounds up

        show_images(images_to_show, columns_quantity, names)

    def subsets_quantity(self):
        return len(self.subsets.keys())

    def subsets_names(self):
        for subset in self.subsets.keys():
            print('-' + subset)
