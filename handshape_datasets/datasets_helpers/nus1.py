from ._utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from .dataset_loader import DatasetLoader
from logging import warning
from skimage import io

import glob
import os
import zipfile


class Nus1(DatasetLoader):
    def __init__(self):
        super().__init__("nus1")
        self.url = 'https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/NUS-Hand-Posture-Dataset-I.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_PATH = os.path.join(folderpath, 'nus1.zip')

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(url=self.urls(), filepath=ZIP_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, extracted_images_folderpath):
        # FIXME How is the dataset structure?
        # dataset_folder = os.path.join(extracted_images_folderpath, 'nus1')
        # if os.path.exists(dataset_folder):
        #     folders = {}
        #     folders_names = list(
        #         # just the folders
        #         filter(lambda x: ".txt" not in x, os.listdir(dataset_folder)))
        #     # start the load
        #     images_loaded_counter = 0
        #     # each image is stored in the key corresponding to its subset
        #     for folder in folders_names:
        #         warning(f"Loading images from {folder}")
        #         folders[folder] = []
        #         # cd subset folder
        #         os.chdir(dataset_folder+'/{}'.format(folder))
        #         images = os.listdir(os.getcwd())
        #         images_loaded_counter += len(images)
        #         for image in images:
        #             folders[folder].append(io.imread(image, as_gray=True))
        #         os.chdir("..")
        #     warning(
        #         f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")

        # nus1 = Dataset('nus1', folders)
        # return nus1 if folders is not None else None
        return True

    def preprocess(self, folderpath, images_folderpath=None):
        preprocess_flag = "{}_preprocessed".format(self._name)
        if self.get_status_flag(folderpath, preprocess_flag) is False:
            # if it doenst receives the images_folderpath arg creates into folderpath
            images_folderpath = os.path.join(
                folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
            mkdir_unless_exists(images_folderpath)
            ZIP_PATH = os.path.join(folderpath, 'nus1.zip')
            # extract the zip into the images path
            extract_zip(ZIP_PATH, images_folderpath)
            self.set_preprocessed_flag(folderpath)
        # if its already extracted doesnt do anything
