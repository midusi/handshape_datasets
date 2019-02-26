from ftplib import FTP
from logging import warning, error
from math import ceil
from pathlib import Path
from requests import get
from shutil import copyfileobj
from requests import get as get_file

import gdown
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import tarfile
import zipfile


def download_file(url, filepath):
    """
    download a file from an url and stores it in filepath
    :param url:
    :param filepath:
    """
    with get_file(url, stream=True) as r:
        # with stream in true the file doen't save in memory inmediately
        # it doesn't dowload the content just the headers and the conection keep open
        warning(
            f"Downloading {filepath} from {url}")
        with open(filepath, 'wb') as f:
            copyfileobj(r.raw, f)
            warning("Download Complete ƪ(˘⌣˘)ʃ")


def download_from_drive(url, filepath):
    warning("Downloading {} dataset from {}".format(filepath, url))
    gdown.download(url, filepath, quiet=True)
    warning("Done ƪ(˘⌣˘)ʃ")


def download_file_over_ftp(ftp_url, ftp_relative_file_path, ftp_filename, filepath):
    ftp = FTP(ftp_url)
    ftp.login()
    ftp.cwd(ftp_relative_file_path)
    with open(filepath, 'wb') as f:
        warning("Downloading the dataset...")
        ftp.retrbinary('RETR {}'.format(ftp_filename), f.write)
        warning("Done ƪ(˘⌣˘)ʃ")


def download_bigger_file(url, filepath):
    """
                    download a file from an url and stores it in filepath
                    :param url:
                    :param filepath:
    """
    with get_file(url, stream=True) as r:
        # with stream in true the file doen't save in memory inmediately
        # it doesn't dowload the content just the headers and the conection keep open
        warning(f"Downloading {filepath} dataset from {url}")
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=512 * 1024):
                if chunk:
                    f.write(chunk)
    warning("Done ƪ(˘⌣˘)ʃ")


def extract_zip(zip_path, extracted_path):
    try:
        with zipfile.ZipFile(file=zip_path,
                             mode="r") as zip_ref:
            warning(f"Extracting {zip_path} to {extracted_path}")
            zip_ref.extractall(path=extracted_path)
            warning("DONE ᕦ(ò_óˇ)ᕤ")
    except FileExistsError:
        error("The folder already exists.")


def extract_tar(tarfile_path, extracted_path):
    try:
        warning(f"Extracting {tarfile_path} to {extracted_path}")
        if (tarfile_path.endswith("tar.gz")):
            with tarfile.open(tarfile_path, "r:gz") as tar:
                tar.extractall(path=extracted_path)
        elif (tarfile_path.endswith("tar")):
            with tarfile.open(tarfile_path, "r:") as tar:
                tar.extractall(path=extracted_path)
        warning("DONE ᕦ(ò_óˇ)ᕤ")
    except FileExistsError:
        error("The folder already exists.")


def get_project_root() -> Path:
    """Returns project root folder."""

    return Path(__file__).parent.parent.parent


def mkdir_unless_exists(folder):
    if not os.path.exists(folder):
        warning(f"Creating folder {folder}...")
        # FIXME Why crashs with nus_1 (?
        os.mkdir(folder)


def show_images(plot_title, images, cols=1, titles=None):
    """Display a list of images in a single figure with matplotlib.

    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.

    cols (Default = 1): Number of columns in figure (number of rows is
                        set to np.ceil(n_images/float(cols))).

    titles: List of titles corresponding to each image. Must have
            the same length as titles.
    """
    assert((titles is None)or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None:  # doenst receive any title
        titles = ['Image (%d)' % i for i in range(1, n_images + 1)]
    fig = plt.figure()  # the container plot
    fig.suptitle(plot_title)
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images/float(cols)), n + 1)
        if image.ndim == 2:  # if isn't rgb else show the colors by default
            plt.gray()
        plt.imshow(image)
        a.axis("off")
        if n_images <= 16:
            a.set_title(title)

    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    if n_images <= 16:
        plt.subplots_adjust(left=0.13, bottom=0.15, right=0.9,
                            top=0.89, wspace=0, hspace=0.32)
    else:  # titles for images are hidden
        plt.subplots_adjust(left=0.03, bottom=0.11, right=0.98,
                            top=0.91, wspace=0, hspace=0.05)
    plt.show()


def show_subsets(subsets, images_number):
    for name in subsets.keys():
        images_to_show = []
        names = []
        for i in range(0, images_number):
            random_image_id = random.randint(0, len(subsets[name])-1)
            images_to_show.append(
                subsets[name][random_image_id])
            names.append("Id {}".format(random_image_id))
        # 4 images per column. Rounds up
        columns_quantity = ceil(len(names)/4)
        show_images(name, images_to_show, columns_quantity, names)
