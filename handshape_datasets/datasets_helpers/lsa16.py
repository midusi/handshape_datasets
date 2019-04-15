from keras.utils.data_utils import get_file
import numpy as np
import os
#from scipy import ndimage
from skimage import io
from skimage import color
from skimage import transform
import zipfile

from os.path import expanduser

LSA16_w = 32
LSA16_h = 32
LSA16_class = 16


def load_images(path_images):
    # tensor con toda la BD
    files = sorted(os.listdir(path_images))
    # base, ext = os.path.splitext()
    # if ext.endswith("jpg") or ext.endswith("jpeg") or ext.endswith("png"):
    files = list(filter(lambda f: os.path.splitext(f)[1].endswith("jpg")
                        or os.path.splitext(f)[1].endswith("png")
                        or os.path.splitext(f)[1].endswith("jpeg"), files))
    n = len(files)
    x = np.zeros((n, LSA16_w, LSA16_h, 3), dtype='uint8')
    y = np.zeros(n, dtype='uint8')
    subjects = np.zeros(n)

    # cargar imagenes con labels
    for (i, filename) in enumerate(files):

        # cargar la imagen actual
        image = io.imread(os.path.join(path_images, filename))

        #image = color.rgb2gray(image)
        image = transform.resize(
            image, (LSA16_w, LSA16_h), preserve_range=True)

        x[i, :, :, :] = image
        # obtener label de la imagen, en base al primer dígito en el nombre de archivo
        y[i] = int(filename.split("_")[0]) - 1
        subjects[i] = int(filename.split("_")[1]) - 1
    return x, y, subjects


def download_and_extract(version, folderpath, images_folderpath):
    if not os.path.exists(folderpath):
        print("Creating folder %s..." % folderpath)
        os.mkdir(folderpath)
        os.mkdir(images_folderpath)

    filename = version + ".zip"
    zip_filepath = os.path.join(folderpath, filename)
    if not os.path.exists(zip_filepath):
        print("Downloading lsa16 version=%s to folder %s ..." %
              (version, zip_filepath))
        base_url = "http://facundoq.github.io/unlp/lsa16/data/"
        origin = base_url + filename
        get_file(zip_filepath, origin=origin)
    if not os.listdir(images_folderpath):
        print("Extracting images...")
        with zipfile.ZipFile(zip_filepath, "r") as zip_ref:
            zip_ref.extractall(images_folderpath)


def load_data(folderpath,version="lsa32x32_nr_rgb_black_background",):
    if not os.path.exists(folderpath):
        print("Creating folder %s..." % folderpath)
        os.makedirs(folderpath, exist_ok=True)
    # get folder where the dataset is / will be downloaded
    folderpath = os.path.join(folderpath, version)
    images_folderpath = os.path.join(folderpath, "images")
    # download dataset (if necessary)
    download_and_extract(version, folderpath, images_folderpath)
    print("Loading images from %s" % images_folderpath)

    # load images
    x, y, subjects = load_images(images_folderpath)

    return x,y,subjects
