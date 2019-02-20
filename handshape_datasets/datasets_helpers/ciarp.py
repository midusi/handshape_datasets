from ._utils import mkdir_unless_exists, extract_zip
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

    def urls(self):
        return self.url

    def download_and_extract(self, folderpath, images_folderpath=None):
        # if it doenst receives the images_folderpath arg creates into folderpath
        images_folderpath = os.path.join(
            folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, 'ciarp.zip')

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            self.download_file(self.urls(), ZIP_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)
        # extract the zip into the images path
        extract_zip(ZIP_PATH, images_folderpath)

    def load(self, extracted_images_folderpath):
        dataset_folder = extracted_images_folderpath+'/ciarp'
        if os.path.exists(dataset_folder):
            folders = {}
            folders_names = list(
                filter(lambda x: ".txt" not in x, os.listdir(dataset_folder)))
            # start the load
            images_loaded_counter = 0
            for folder in folders_names:
                warning(f"Loading images from {folder}")
                folders[folder] = []
                os.chdir(dataset_folder+'/{}'.format(folder))
                images = os.listdir(os.getcwd())
                images_loaded_counter += len(images)
                for image in images:
                    folders[folder].append(io.imread(image, as_gray=True))
                os.chdir("..")
            warning(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")
            warning(
                "You can access to the diferents categories using: var_name[folder_name][image_index]\nThe options available are:")
            for position, folder in enumerate(folders_names):
                warning('{}. {}'.format(position, folder))

        return folders if folders is not None else None

    def preprocess(self, path):
        pass
