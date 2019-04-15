from ._utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from .dataset_loader import DatasetLoader
from logging import warning
import numpy as np
import os

#from scipy import ndimage
from skimage import io
from skimage import color
from skimage import transform
import zipfile





# def download_and_extract(version, folderpath, images_folderpath):
#     if not os.path.exists(folderpath):
#         print("Creating folder %s..." % folderpath)
#         os.mkdir(folderpath)
#         os.mkdir(images_folderpath)
#
#     filename = version + ".zip"
#     zip_filepath = os.path.join(folderpath, filename)
#     if not os.path.exists(zip_filepath):
#         print("Downloading lsa16 version=%s to folder %s ..." %
#               (version, zip_filepath))
#         base_url = "http://facundoq.github.io/unlp/lsa16/data/"
#         origin = base_url + filename
#         get_file(zip_filepath, origin=origin)
#     if not os.listdir(images_folderpath):
#         print("Extracting images...")
#         with zipfile.ZipFile(zip_filepath, "r") as zip_ref:
#             zip_ref.extractall(images_folderpath)
#
#
# def load_data(folderpath,):
#     if not os.path.exists(folderpath):
#         print("Creating folder %s..." % folderpath)
#         os.makedirs(folderpath, exist_ok=True)
#     # get folder where the dataset is / will be downloaded
#     folderpath = os.path.join(folderpath, version)
#     images_folderpath = os.path.join(folderpath, "images")
#     # download dataset (if necessary)
#     download_and_extract(version, folderpath, images_folderpath)
#     print("Loading images from %s" % images_folderpath)
#
#     # load images
#     x, y, subjects = load_images(images_folderpath)
#
#     return x,y,subjects


class LSA16(DatasetLoader):
    def __init__(self,version="lsa32x32_nr_rgb_black_background"):
        #TODO generate URL from options
        super().__init__("lsa16")
        self.filename = f"{version}.zip"
        self.url = f'http://facundoq.github.io/unlp/lsa16/data/{self.filename}'
        self.shape= (32,32) # TODO get from version
        self.classes = 16




    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        zip_filepath= os.path.join(folderpath, self.filename)

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(url=self.urls(), filepath=zip_filepath,
                          filename=self.filename)
            # set the exit flag
            self.set_downloaded(folderpath)

    def preprocess(self, folderpath, images_folderpath=None):
        zip_filepath = os.path.join(folderpath, self.filename)
        if self.get_preprocessed_flag(folderpath) is False:
            # if it doenst receives the images_folderpath arg creates into folderpath
            images_folderpath = os.path.join(
                folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
            mkdir_unless_exists(images_folderpath)

            # extract the zip into the images path
            extract_zip(zip_filepath, images_folderpath)
            self.set_preprocessed_flag(folderpath)
        # if its already extracted doesnt do anything



    def load(self,path_images):
        # get image file names
        files = sorted(os.listdir(path_images))
        files = list(filter(lambda f: os.path.splitext(f)[1].endswith("jpg")
                            or os.path.splitext(f)[1].endswith("png")
                            or os.path.splitext(f)[1].endswith("jpeg"), files))
        n = len(files)
        # pre-generate matrices
        x = np.zeros((n, self.shape[0], self.shape[1], 3), dtype='uint8')
        y = np.zeros(n, dtype='uint8')
        subjects = np.zeros(n)

        # Load images with labels
        for (i, filename) in enumerate(files):
            # load image
            image = io.imread(os.path.join(path_images, filename))
            x[i, :, :, :] = image
            # Get class and subject id for image
            y[i] = int(filename.split("_")[0]) - 1
            subjects[i] = int(filename.split("_")[1]) - 1
        metadata={"y":y,"subjects":subjects}
        return x, metadata

