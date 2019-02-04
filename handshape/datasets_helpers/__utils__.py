from pathlib import Path
from requests import get
from shutil import copyfileobj
from hurry.filesize import size

import os
import zipfile
import tarfile


def get_project_root() -> Path:
    """Returns project root folder."""

    return Path(__file__).parent.parent.parent


def __humansize__(nbytes):
    return size(nbytes)


def download_file(url, filepath):
    """
        download a zip from an url and stores it in filepath
        :param url:
        :param filepath:
    """
    with get(url, stream=True) as r:
        print("The file size is {}".format(
            __humansize__(r.headers['Content-length'])))
        print("Downloading {} dataset from {}".format(filepath, url))
        with open(filepath, 'wb') as f:
            copyfileobj(r.raw, f)
    print("Done ƪ(˘⌣˘)ʃ")


def check_folder_existence(folder):
    if not os.path.exists(folder):
        print("Creating folder %s..." % folder)
        os.mkdir(folder)


def extract_zip(zip_path, extracted_path):
    with zipfile.ZipFile(file=zip_path,
                         mode="r") as zip_ref:
        print("Extracting {} to {}".format(zip_path, extracted_path))
        zip_ref.extractall(path=extracted_path)
        print("DONE ᕦ(ò_óˇ)ᕤ")


def extract_tar(tarfile_path, extracted_path):
    print("Extracting {} to {}".format(tarfile_path, extracted_path))
    if (tarfile_path.endswith("tar.gz")):
        with tarfile.open(tarfile_path, "r:gz") as tar:
            tar.extractall(path=extracted_path)
    elif (tarfile_path.endswith("tar")):
        with tarfile.open(tarfile_path, "r:") as tar:
            tar.extractall(path=extracted_path)
    print("DONE ᕦ(ò_óˇ)ᕤ")