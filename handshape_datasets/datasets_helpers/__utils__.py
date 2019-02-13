from pathlib import Path
from requests import get
from shutil import copyfileobj
#from hurry.filesize import size
from ftplib import FTP

import os
import zipfile
import tarfile
import gdown


def check_folder_existence(folder):
    if not os.path.exists(folder):
        print("Creating folder %s..." % folder)
        os.mkdir(folder)


def create_download_complete_file(filepath, dataset_name):
    open(filepath, 'a').close()
    print("The download of the dataset {} was successfully completed.".format(dataset_name))


def download_detector_found(folderpath, file_name):
    try:
        open(os.path.join(folderpath, file_name), 'r').close()
        return True
    except FileNotFoundError:
        return False


def download_file(url, filepath):
    """
        download a file from an url and stores it in filepath
        :param url:
        :param filepath:
    """
    with get(url, stream=True) as r:
        # with stream in true the file doen't save in memory inmediately
        # it doesn't dowload the content just the headers and the conection keep open
        print("Downloading {} dataset from {}".format(filepath, url))
        with open(filepath, 'wb') as f:
            copyfileobj(r.raw, f)
    print("Download Complete ƪ(˘⌣˘)ʃ")


def download_from_drive(url, filepath):
    print("Downloading {} dataset from {}".format(filepath, url))
    gdown.download(url, filepath, quiet=True)
    print("Done ƪ(˘⌣˘)ʃ")


def download_file_over_ftp(ftp_url, ftp_relative_file_path, ftp_filename, filepath):
    ftp = FTP(ftp_url)
    ftp.login()
    ftp.cwd(ftp_relative_file_path)
    with open(filepath, 'wb') as f:
        print("Downloading the dataset...")
        ftp.retrbinary('RETR {}'.format(ftp_filename), f.write)
        print("Done ƪ(˘⌣˘)ʃ")


def download_bigger_file(url, filepath):
    """
        download a file from an url and stores it in filepath
        :param url:
        :param filepath:
    """
    with get(url, stream=True) as r:
        # with stream in true the file doen't save in memory inmediately
        # it doesn't dowload the content just the headers and the conection keep open
        print("Downloading {} dataset from {}".format(filepath, url))
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk.raw)
    print("Done ƪ(˘⌣˘)ʃ")


def extract_zip(zip_path, extracted_path):
    try:
        with zipfile.ZipFile(file=zip_path,
                             mode="r") as zip_ref:
            print("Extracting {} to {}".format(zip_path, extracted_path))
            zip_ref.extractall(path=extracted_path)
            print("DONE ᕦ(ò_óˇ)ᕤ")
    except FileExistsError:
        print("The folder already exists.")


def extract_tar(tarfile_path, extracted_path):
    print("Extracting {} to {}".format(tarfile_path, extracted_path))
    if (tarfile_path.endswith("tar.gz")):
        with tarfile.open(tarfile_path, "r:gz") as tar:
            tar.extractall(path=extracted_path)
    elif (tarfile_path.endswith("tar")):
        with tarfile.open(tarfile_path, "r:") as tar:
            tar.extractall(path=extracted_path)
    print("DONE ᕦ(ò_óˇ)ᕤ")


def get_project_root() -> Path:
    """Returns project root folder."""

    return Path(__file__).parent.parent.parent
