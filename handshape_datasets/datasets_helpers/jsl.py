from ._utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from .dataset_loader import DatasetLoader
from skimage import io
from logging import warning

import os


class Jsl(DatasetLoader):
    def __init__(self):
        super().__init__("jsl")
        self.url = 'http://home.agh.edu.pl/~bkw/research/data/mva/jsl.zip'
        self._FILENAME = self._name + '.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_NAME = 'jsl.zip'
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(self.urls(), filepath=ZIP_PATH,
                          filename=self._FILENAME)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, extracted_images_folderpath):
        if os.path.exists(extracted_images_folderpath):
            subsets = {
                "data": []
            }
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            os.chdir(extracted_images_folderpath)
            # all images in thexe folder:
            warning(f"Loading images from {extracted_images_folderpath}")
            for image in os.listdir(extracted_images_folderpath):
                subsets["data"].append(io.imread(image, as_gray=True))
                images_loaded_counter += 1
            warning(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")
            dataset = Dataset(self._name, subsets)
            return dataset

    def preprocess(self, folderpath, images_folderpath=None):
        if self.get_preprocessed_flag(folderpath) is False:

            images_folderpath = os.path.join(
                folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath

            mkdir_unless_exists(images_folderpath)
            ZIP_PATH = os.path.join(folderpath, self._FILENAME)
            # extract the zip into the images_folderpath
            extract_zip(ZIP_PATH, images_folderpath)
            self.set_preprocessed_flag(folderpath)
        # if is already preprocessed it doenst do anything
