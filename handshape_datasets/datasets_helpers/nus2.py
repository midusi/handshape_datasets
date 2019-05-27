from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from .dataset_loader import DatasetLoader
from logging import warning
from skimage import io

import os
import numpy as np


class Nus2(DatasetLoader):
    def __init__(self):
        super().__init__("nus_2")
        self.url = 'https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/NUS-Hand-Posture-Dataset-II.zip'
        self._FILENAME = self.name + '.zip'
        self._CLASSES_IDS = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5,
            'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10,
        }

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

    def load(self, folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        subsets_folder = os.path.join(images_folderpath,'NUS Hand Posture dataset-II')
        if os.path.exists(subsets_folder):
            subsets = {}
            subsets_names = list(
                # just the subsets folders
                filter(lambda x: "Hand" in x,
                       os.listdir(subsets_folder)))
            # start the load
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            for subset in subsets_names:
                warning(f"Loading images from {subset}")

                # the data variable of the dataset class
                subsets[subset] = {}
                # where the subset images are stored
                subset_images_path = os.path.join(subsets_folder, subset)
                # Drops the Thumbs.db file
                images = list(
                    filter(
                        lambda x: ".db" not in x,
                        os.listdir(subset_images_path)
                    )
                )

                NUMBER_OF_IMAGES = len(images)
                images_loaded_counter += NUMBER_OF_IMAGES

                IMAGE_HEIGHT = 120
                IMAGE_WIDTH = 160
                IMAGE_COLORS = 3

                subsets[subset]["x"] = np.zeros(shape=(NUMBER_OF_IMAGES,
                                                       IMAGE_HEIGHT,
                                                       IMAGE_WIDTH,
                                                       IMAGE_COLORS),
                                                dtype="uint8")

                subsets[subset]["y"] = np.zeros(shape=NUMBER_OF_IMAGES)
                x = subsets[subset]["x"]
                y = subsets[subset]["y"]
                for position, image_name in enumerate(images):
                    # loads the image
                    x[position] = io.imread(image_name)
                    # loads the image klass in the array
                    y[position] = self.get_klass_id_for_filename(
                        image_name)

            warning(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")

            nus_2 = Dataset('nus_2', subsets)
            return nus_2 if subsets is not None else None

    def get_klass_id_for_filename(self, filename):
        """Returns the class corresponding to the image

        Args:
            filename (str): The name of the file to be parsed

        Returns:
            int: The class id of the hand. In this dataset the class
            \tis the first char from filename
        """
        return self._CLASSES_IDS[filename[0]]

    def preprocess(self, folderpath, images_folderpath=None):
        images_folderpath = self.images_folderpath(folderpath)

        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # extract the zip into the images_folderpath
        extract_zip(ZIP_PATH, images_folderpath)
        self.set_preprocessed_flag(folderpath)
