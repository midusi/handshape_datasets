from ._utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from .dataset_loader import DatasetLoader
from logging import warning
from skimage import io

import os


class Nus2(DatasetLoader):
    def __init__(self):
        super().__init__("nus_2")
        self.url = 'https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/NUS-Hand-Posture-Dataset-II.zip'
        self._FILENAME = self._name + '.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        mkdir_unless_exists(folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(self.urls(), ZIP_PATH, filename=self._FILENAME)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, extracted_images_folderpath):
        subsets_folder = os.path.join(extracted_images_folderpath,
                                      'NUS Hand Posture dataset-II')
        if os.path.exists(subsets_folder):
            os.chdir(subsets_folder)
            folders = {}
            folders_names = list(
                # just the folders
                filter(lambda x: ".txt" not in x and "Backgrounds" not in x,
                       os.listdir(os.getcwd())))
            # start the load
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            for folder in folders_names:
                warning(f"Loading images from {folder}")
                folders[folder] = []
                # cd subset folder
                os.chdir(subsets_folder+'/{}'.format(folder))
                images = list(
                    filter(
                        lambda x: ".db" not in x, os.listdir(os.getcwd())))
                images_loaded_counter += len(images)
                for image in images:
                    folders[folder].append(
                        # if the images are in color, doenst show in gray
                        io.imread(image, as_gray=(folder == 'Color')))
                os.chdir("..")
            warning(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")

            nus_2 = Dataset('nus_2', folders)
            return nus_2 if folders is not None else None

    def preprocess(self, folderpath, images_folderpath=None):
        if self.get_preprocessed_flag(folderpath) is False:
            images_folderpath = os.path.join(
                folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
            mkdir_unless_exists(images_folderpath)
            ZIP_PATH = os.path.join(folderpath, self._FILENAME)
            # extract the zip into the images_folderpath
            extract_zip(ZIP_PATH, images_folderpath)
            self.set_preprocessed_flag(folderpath)
