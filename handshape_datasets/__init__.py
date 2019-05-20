from shutil import rmtree as _rmtree


from logging import warning as _warning
from .datasets_helpers.config import options as _options

import os as _os

NAMES = list(_options.keys())

_HOME_PATH_HANDSHAPE = _os.path.join(_os.getenv('HOME'),
                                     '.handshape_datasets')


def load(selected_dataset,
         folderpath=_HOME_PATH_HANDSHAPE,
         images_folderpath=None,**kwargs):
    """Downloads, preprocesses and load in memory a dataset.

    Args:
        selected_dataset (str): The dataset to download
        folderpath (str, optional): Defaults to /home/.handshape-datasets.
        \tWhere the dataset files will be downloaded
        images_folderpath (str, optional): Defaults to None.
        \tThe path where the images will be extracted

    Raises:
        KeyError: If the selected dataset is not a valid option

    Returns:
        An Dataset object instance
    """
    try:
        _os.mkdir(folderpath)  # default folder for creation
    except FileExistsError:
        pass

    if images_folderpath is None:
        images_folderpath=f"{selected_dataset}_images"

    images_folderpath = _os.path.join(folderpath, selected_dataset,images_folderpath)

    try:
        # get downloader class for dataset
        dataset_class = _options[selected_dataset]
        # instance the class
        dataset = dataset_class()
        # load and return the dataset
        return dataset.get(folderpath, images_folderpath,**kwargs)

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
        _warning(f"Removing the dataset {dataset}")
        # removes the directory recursively
        _rmtree(_os.path.join(path, dataset))
        _warning("Success \(•◡•)/")
    except FileNotFoundError:
        _warning("""The dataset {} doesn't exist (ಥ﹏ಥ). The options available
                are: \n {}""".format(dataset, "\n".join(_options.keys())))


# def clear_all(path=_os.path.join(_os.getenv("HOME"), ".handshape_datasets")):

def help():
    message = f"""To load a dataset, call load('dataset'),
    where the supported datasets are:\n{", ".join(_options.keys())}\n\
Example:\n\
    import handshape_datasets\n\
    dataset=handshape_datasets.load('ciarp')\n\
    print(dataset.summary)
"""
    print(message)
