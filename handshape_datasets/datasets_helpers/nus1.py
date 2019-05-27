from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from .dataset_loader import DatasetLoader
from logging import warning
from skimage import io

import os


class Nus1(DatasetLoader):
    def __init__(self):
        self.__doc__ += super.__doc__
        super().__init__("nus_1")
        self.url = 'https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/NUS-Hand-Posture-Dataset-I.zip'
        self._FILENAME = self.name + '.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(url=self.urls(), filepath=ZIP_PATH, filename= self._FILENAME)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        subsets_folder = os.path.join(images_folderpath,
                                      'NUS Hand Posture Dataset')
        if os.path.exists(subsets_folder):
            os.chdir(subsets_folder)
            folders = {}
            folders_names = list(
                # just the folders
                filter(lambda x: ".txt" not in x, os.listdir(os.getcwd())))
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

            nus1 = Dataset('nus1', folders)
            return nus1 if folders is not None else None

    def preprocess(self, folderpath):

        images_folderpath = self.images_folderpath(folderpath)
        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # extract the zip into the images path
        extract_zip(ZIP_PATH, images_folderpath)
        self.set_preprocessed_flag(folderpath)
