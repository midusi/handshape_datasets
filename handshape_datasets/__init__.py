from .datasets_helpers.config import options as _options
from shutil import rmtree
from os.path import join as create_path
from logging import warning

import os as _os

names = list(_options.keys())

_HOME_PATH_HANDSHAPE = _os.path.join(_os.getenv('HOME'),
                                     '.handshape_datasets')
try:
    _os.mkdir(_HOME_PATH_HANDSHAPE)  # default folder for creation
except FileExistsError:
    pass


def load(selected_dataset,
         folderpath=_HOME_PATH_HANDSHAPE,
         images_folderpath=None):

    images_folderpath = create_path(_HOME_PATH_HANDSHAPE, selected_dataset,
                                    f"{selected_dataset}_images") if images_folderpath is None else images_folderpath
    try:
        # get downloader class for dataset
        dataset_class = _options[selected_dataset]
        # instance the class
        dataset = dataset_class()
        # load and return the dataset
        return dataset.get(folderpath, images_folderpath)

    except KeyError:
        print("The option {} isn't valid. The valid options are")
        for position, key in enumerate(_options.keys()):
            print('{}. {}'.format(position, key))


def clear(dataset,
          path=_os.path.join(_os.getenv("HOME"), ".handshape_datasets")):
    """Removes a dataset folder from the specified path
    Args:
        dataset (str): the dataset to delete
        path (str, optional): Defaults to $HOME/handshape_datasets
    Raises:
        FileNotFoundError: The dataset entered doesnt exist or at least in path
    """
    # BUG Why doesnt work with nus1?
    try:
        warning(f"Removing the dataset {dataset}")
        # removes the directory recursively
        rmtree(_os.path.join(path, dataset))
        warning("Success \(•◡•)/")
    except FileNotFoundError:
        warning("""The dataset {} doesn't exist (ಥ﹏ಥ). The options available
                are: \n {}""".format(dataset, "\n".join(_options.keys())))


def help():
    message = f"""To load a dataset, call load('dataset'), where the supported datasets are:\n{", ".join(_options.keys())}\n\
Example:\n\
    import handshape_datasets\n\
    dataset=handshape_datasets.load('ciarp')\n\
    print(dataset.summary)
"""
    print(message)
