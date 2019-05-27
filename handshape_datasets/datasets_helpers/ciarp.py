from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from .dataset_loader import DatasetLoader
from logging import warning
from skimage import io

import glob
import os
import zipfile


class Ciarp(DatasetLoader):
    def __init__(self):
        super().__init__("ciarp")
        self.url = 'http://home.agh.edu.pl/~bkw/code/ciarp2017/ciarp.zip'
        self._FILENAME = self.name + '.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        download_file(url=self.urls(), filepath=ZIP_PATH,
                      filename=self._FILENAME)
        # set the exit flag
        self.set_downloaded(folderpath)

    def load(self,folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        dataset_folder = os.path.join(images_folderpath , 'ciarp')
        if os.path.exists(dataset_folder):
            folders = {}
            folders_names = list(
                # just the folders
                filter(lambda x: ".txt" not in x, os.listdir(dataset_folder)))
            # start the load
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            for folder in folders_names:
                warning(f"Loading images from {folder}")
                folders[folder] = []
                # cd subset folder
                new_dir = os.path.join(dataset_folder, '{}'.format(folder))
                images = os.listdir(new_dir)
                images_loaded_counter += len(images)
                for image in images:
                    folders[folder].append(io.imread(image, as_gray=True))
                os.chdir("..")
            warning(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")

        ciarp = Dataset('ciarp', folders)
        return ciarp if folders is not None else None


    def preprocess(self, folderpath):

        # if it doenst receives the images_folderpath arg creates into folderpath
        images_folderpath = self.images_folderpath(folderpath)
        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # extract the zip into the images path
        extract_zip(ZIP_PATH, images_folderpath)
        self.set_preprocessed_flag(folderpath)