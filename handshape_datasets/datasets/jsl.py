from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from handshape_datasets.dataset_loader import DatasetLoader
from skimage import io
from logging import warning
from .common import *
import os
from pyunpack import Archive
from handshape_datasets.dataset_loader import DatasetLoader
from . import utils

class JslInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n LSA16
        Argentinian Sign Language Handshapes dataset 
        More details can be found at http://facundoq.github.io/unlp/lsa16/
        \nVersion default : color\nOther version : colorbg
        """
        url_info = "http://facundoq.github.io/unlp/lsa16/"
        download_size = 655994
        disk_size = 1225566
        subject = 800
        super().__init__("lsa16",(32,32,3),{"y":"classes", "subject":"subject"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return Jsl()


class Jsl(DatasetLoader):
    def __init__(self):
        super().__init__("jsl")
        self.url = 'http://home.agh.edu.pl/~bkw/research/data/mva/jsl.zip'
        self._FILENAME = self.name + '.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        download_file(self.urls(), filepath=ZIP_PATH,
                      filename=self._FILENAME)
        # set the download flag
        self.set_downloaded(folderpath)

    def load(self, folderpath, **kwargs):
        images_folderpath = self.images_folderpath(folderpath)
        if os.path.exists(images_folderpath ):
            subsets = {
                "data": []
            }
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            # all images in thexe folder:
            warning(f"Loading images from {images_folderpath }")
            for image in os.listdir(images_folderpath ):
                image_path=os.path.join(images_folderpath,image)
                subsets["data"].append(io.imread(image_path, as_gray=True))
                images_loaded_counter += 1

            warning(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")
            dataset = Dataset(self.name, subsets)
            return dataset

    def preprocess(self, folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # extract the zip into the images_folderpath
        extract_zip(ZIP_PATH, images_folderpath)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = os.path.join(fpath, self.folder_name)
        npz_exist = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(npz_exist) == 0):
            return False
        else:
            rmtree(folder)
            return True