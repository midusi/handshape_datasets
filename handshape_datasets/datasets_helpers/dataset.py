from logging import warning
from math import ceil
from ._utils import show_dataset


class Dataset(object):
    def __init__(self, name, data):
        self.name = name
        self.subsets = data

    def summary(self):
        subset_names=""
        for i,item in enumerate(self.subsets.items()):
            name,subset=item
            subset_names+="\t"+f"{i+1}) {name}: {len(subset)} samples"+"\n"
        n_subsets=len(self.subsets)
        result=f"Dataset {self.name}\n" \
            f"{n_subsets} subsets:\n" \
            f"{subset_names}"

        return result

    def show_dataset(self, subsets=None, samples=32):
        if subsets==None:
            subsets=self.subsets.keys()

        show_dataset(self, subsets, samples)