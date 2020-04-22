from ftplib import FTP
from logging import warning, error, info, debug
from math import ceil
from pathlib import Path
from requests import get
from shutil import copyfileobj
from requests import get as get_file
import math
import gdown
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import tarfile
import zipfile
import codecs
import patoolib
import platform


def download_file_content_as_text(url:str):
    with get_file(url, stream=True) as r:
        return r.text

def download_file(url: str, filepath: str) -> None:
    """
    download a file from an url and stores it in filepath
    :param url:
    :param filepath:
    """
    with get_file(url, stream=True) as r:
        # with stream in true the file doen't save in memory inmediately
        # it doesn't dowload the content just the headers and the conection keep open
        info(
            f"Downloading {url} to {filepath}")
        # if filename exists
        with open(filepath, 'wb') as f:
            copyfileobj(r.raw, f)

def download_from_drive(url:str, filepath:str):
    info("Downloading {} dataset from {}".format(filepath, url))
    gdown.download(url, filepath, quiet=True)


def download_file_over_ftp(ftp_url:str, ftp_relative_file_path:str, ftp_filename:str, filepath:str):
    ftp = FTP(ftp_url)
    ftp.login()
    ftp.cwd(ftp_relative_file_path)
    with open(filepath, 'wb') as f:
        info("Downloading the dataset...")
        ftp.retrbinary('RETR {}'.format(ftp_filename), f.write)


def download_bigger_file(url:str, filepath:str):
    """
                    download a file from an url and stores it in filepath
                    :param url:
                    :param filepath:
    """
    with get_file(url, stream=True) as r:
        # with stream in true the file doen't save in memory inmediately
        # it doesn't dowload the content just the headers and the conection keep open
        info(f"Downloading {filepath} dataset from {url}")
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=512 * 1024):
                if chunk:
                    f.write(chunk)


def extract_zip(zip_path, extracted_path):
    try:
        with zipfile.ZipFile(file=zip_path,
                             mode="r") as zip_ref:
            info(f"Extracting {zip_path} to {extracted_path}")
            zip_ref.extractall(path=extracted_path)
            debug("DONE ᕦ(ò_óˇ)ᕤ")
    except FileExistsError:
        error("The folder already exists.")

def extract_tar(tarfile_path, extracted_path):
    extracted_path_act=str(extracted_path)
    try:
        info(f"Extracting {tarfile_path} to {extracted_path}")

        if (tarfile_path.endswith("tar.gz")):
           mode ="r:gz"
        elif (tarfile_path.endswith("tar")):
            mode = "r:"
        elif tarfile_path.endswith(".tar.bz2"):
            mode = "r:bz2"
        else:
            raise ValueError(f"Unsupported file extension for file {tarfile_path}")

        if(platform.system()=="Windows"):
            debug("So: Windows")
            if (mode=="r:bz2"):
                with tarfile.open(tarfile_path, mode) as tar:
                    tar.extractall(path=extracted_path)
            else:
                patoolib.extract_archive(tarfile_path.encode().decode('utf-8'), outdir=extracted_path_act, verbosity=-2)
        else:
            debug("So: Linux")
            with tarfile.open(tarfile_path, mode) as tar:
               tar.extractall(path=extracted_path)
               debug("DONE ᕦ(ò_óˇ)ᕤ")
    except FileExistsError:
        error("The folder already exists.")


def get_project_root() -> Path:
    """Returns project root folder."""

    return Path(__file__).parent.parent.parent


def mkdir_unless_exists(folder):
    if not os.path.exists(folder):
        info(f"Creating folder {folder} ...")
        os.makedirs(folder)


def show_images(plot_title, images, cols, titles=None):
    """Display a list of images in a single figure with matplotlib.

    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.

    cols (Default = 1): Number of columns in figure (number of rows is
                        set to np.ceil(n_images/float(cols))).

    titles: List of titles corresponding to each image. Must have
            the same length as titles.
    """
    assert ((titles is None) or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None:  # doenst receive any title
        titles = ['Image (%d)' % i for i in range(1, n_images + 1)]
    fig = plt.figure()  # the container plot
    fig.suptitle(plot_title)
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images / float(cols)), n + 1)
        if image.ndim == 2:  # if isn't rgb else show the colors by default
            plt.gray()
        plt.imshow(image)
        a.axis("off")
        if n_images <= 16:
            a.set_title(title)

    if n_images <= 16:
        plt.subplots_adjust(left=0.13, bottom=0.15, right=0.9,
                            top=0.89, wspace=0, hspace=0.32)
    else:  # titles for images are hidden
        plt.subplots_adjust(left=0.03, bottom=0.11, right=0.98,
                            top=0.91, wspace=0, hspace=0.05)
    plt.show()


def show_subset(dataset, subset_name, samples=32, cols=None):
    subset = dataset.subsets[subset_name]

    if isinstance(samples, int):
        # select a random subset of samples
        sample_indices = np.random.permutation(len(subset))[:samples]
    elif isinstance(samples, list):
        sample_indices = samples
    else:
        raise ValueError(
            f"Invalid samples: {samples}. Must be int or list of ints")

    images_to_show = [subset[i] for i in sample_indices]
    names = [f"Id {i}" for i in sample_indices]
    if cols == None:
        wide_aspect_ratio = 1080 / 1920
        cols = ceil(math.sqrt(len(names) * wide_aspect_ratio))

    show_images(f"Subset {subset_name}:", images_to_show, cols, titles=names)


def show_dataset(dataset, subset_names=None, samples=32):
    if subset_names == None:
        subset_names = dataset.subsets.keys()
    for name in subset_names:
        show_subset(dataset, name, samples)
