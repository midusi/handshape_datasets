from shutil import rmtree as _rmtree

from pathlib import Path
from logging import warning as warning
from handshape_datasets.config import options

default_folder = Path.home() / '.handshape_datasets'

from .dataset_info import DatasetInfo

def list_datasets()->DatasetInfo:
    for id in options.keys():
        dataset_name =options[id].id
        print(dataset_name)

def info(id:str)->DatasetInfo:
    return options[id]

def load(id,
         folderpath:Path=default_folder, **kwargs):
    """Downloads, preprocesses and load in memory a dataset.

    Args:
        id (str): The dataset to download
        folderpath (str, optional): Defaults to /home/.handshape-datasets.
        \tWhere the dataset files will be downloaded

    Raises:
        KeyError: If the selected dataset is not a valid option

    Returns:
        An Dataset object instance
    """
    if not id in options.keys():
        raise ValueError(f"Unknown dataset id {id}. Refer to handshape_datasets.ids() for a complete list of supported datasets.")

    folderpath.mkdir(parents=True,exist_ok=True)

    # get downloader class for dataset
    dataset_loader = options[id].get_loader()
    # load and return the dataset
    return dataset_loader.get(folderpath, **kwargs)




def clear(dataset,
          folderpath=default_folder):
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
        _rmtree(folderpath / dataset)
        warning("Success \(•◡•)/")
    except FileNotFoundError:
        warning("""The dataset {} doesn't exist (ಥ﹏ಥ). The options available
                are: \n {}""".format(dataset, "\n".join(options.keys())))


# def clear_all(path=_os.path.join(_os.getenv("HOME"), ".handshape_datasets")):

def help():
    message = f"""To load a dataset, call load('dataset'),
    where the supported datasets are:\n{", ".join(options.keys())}\n\
Example:\n\
    import handshape_datasets\n\
    dataset=handshape_datasets.load('ciarp')\n\
    print(dataset.summary)
"""
    print(message)


def ids():
    return list(options.keys())