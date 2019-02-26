from ._utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from .dataset_loader import DatasetLoader
from skimage import io
from logging import warning

import os
import zipfile


class Jsl(DatasetLoader):
    def __init__(self):
        super().__init__("jsl")
        self.url = 'http://home.agh.edu.pl/~bkw/research/data/mva/jsl.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_PATH = os.path.join(folderpath, 'jsl.zip')

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(self.urls(), ZIP_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, extracted_images_folderpath):
        dataset_folder = os.path.join(extracted_images_folderpath, 'ciarp')
        if os.path.exists(dataset_folder):
            subsets = {
                "data": []
            }
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            os.chdir(dataset_folder)
            # all images in the folder:
            for image in os.listdir(dataset_folder):
                warning(f"Loading images from {dataset_folder}")
                subsets["data"].append(io.imread(image, as_gray=True))
            warning(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")
            dataset = Dataset(self._name, subsets)
            return dataset

    def preprocess(self, folderpath, images_folderpath=None):
        images_folderpath = os.path.join(
            folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, 'jsl.zip')
        # extract the zip into the images_folderpath
        extract_zip(ZIP_PATH, images_folderpath)
        self.set_preprocessed_flag(folderpath)
