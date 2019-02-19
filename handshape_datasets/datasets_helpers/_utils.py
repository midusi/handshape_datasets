from ftplib import FTP
from pathlib import Path
from requests import get
from shutil import copyfileobj
#from hurry.filesize import size

import gdown
import logging
import os
import tarfile
import zipfile


def check_folder_existence(folder):
    if not os.path.exists(folder):
        logging.info(f"Creating folder {folder}...")
        os.mkdir(folder)


def extract_zip(zip_path, extracted_path):
    try:
        with zipfile.ZipFile(file=zip_path,
                             mode="r") as zip_ref:
            logging.info(f"Extracting {zip_path} to {extracted_path}")
            zip_ref.extractall(path=extracted_path)
            logging.info("DONE ᕦ(ò_óˇ)ᕤ")
    except FileExistsError:
        logging.error("The folder already exists.")


def extract_tar(tarfile_path, extracted_path):
    try:
        logging.warning(f"Extracting {tarfile_path} to {extracted_path}")
        if (tarfile_path.endswith("tar.gz")):
            with tarfile.open(tarfile_path, "r:gz") as tar:
                tar.extractall(path=extracted_path)
        elif (tarfile_path.endswith("tar")):
            with tarfile.open(tarfile_path, "r:") as tar:
                tar.extractall(path=extracted_path)
        logging.info("DONE ᕦ(ò_óˇ)ᕤ")
    except FileExistsError:
        logging.error("The folder already exists.")


def get_project_root() -> Path:
    """Returns project root folder."""

    return Path(__file__).parent.parent.parent
