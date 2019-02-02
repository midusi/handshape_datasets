from pathlib import Path
from requests import get
from shutil import copyfileobj

import os


def get_project_root() -> Path:
    """Returns project root folder."""

    return Path(__file__).parent.parent.parent


def download_file(url, filepath):
    """
        download a zip from an url and stores it in filepath
        :param url: 
        :param filepath: 
    """
    with get(url, stream=True) as r:
        print("Downloading {} dataset from {}".format(filepath, url))
        with open(filepath, 'wb') as f:
            copyfileobj(r.raw, f)
    print("Done ƪ(˘⌣˘)ʃ")

def check_folder_existence(folder):
    if not os.path.exists(folder):
        print("Creating folder %s..." % folder)
        os.mkdir(folder)