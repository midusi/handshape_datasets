from shutil import rmtree as _rmtree
import os
from pathlib import Path
from logging import warning as warning
from handshape_datasets.config import options
from prettytable import PrettyTable
from .dataset_info import DatasetInfo

default_folder = Path.home() / '.handshape_datasets'

def list_datasets():
    print("\n")
    print("Datasets disponibles:")
    table = PrettyTable ( ["Dataset", "Tamaño de descarga", "Tamaño en disco", "Ejemplos", "Cantidad de clases"])
    for id in options.keys():
        download_size_format, do_size_format, disk_size_format, di_size_format=size_format(options[id].download_size, options[id].disk_size)
        dataset_name =options[id].id
        dlz = str(round(download_size_format,1)) + ' ' + do_size_format
        dz = str(round(disk_size_format,1)) + ' ' + di_size_format
        sub = options[id].subject
        cla, y = options[id].return_labels()
        table.add_row([dataset_name, dlz, dz, sub, cla])
    print (table)

def size_format(download_size, disk_size):
    do_size_format="b"
    di_size_format = "b"
    download_size_format=download_size
    disk_size_format=disk_size
    if (download_size > 1000):
        download_size_format = download_size / 1024
        do_size_format = "Kb"
        if (download_size > 1000000):
            download_size_format = download_size_format / 1024
            do_size_format = "Mb"
            if (download_size > 1000000000):
                download_size_format = download_size_format / 1024
                do_size_format = "Gb"
    if (disk_size > 1000):
        disk_size_format = disk_size / 1024
        di_size_format = "Kb"
        if (disk_size > 1000000):
            disk_size_format = disk_size_format / 1024
            di_size_format = "Mb"
            if (disk_size > 1000000000):
                disk_size_format = disk_size_format / 1024
                di_size_format = "Gb"
    return (download_size_format, do_size_format, disk_size_format, di_size_format)

def info(id:str)->DatasetInfo:
    return options[id]

def load(id, folderpath:Path=default_folder, **kwargs):
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

def delete_temporary_folders(id, folderpath:Path=default_folder):
    dataset_loader = options[id].get_loader()
    return dataset_loader.delete_temporary_files(folderpath)