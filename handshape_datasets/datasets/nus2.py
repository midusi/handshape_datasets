from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from handshape_datasets.dataset_loader import DatasetLoader

from skimage import io
from .common import *


import os
import numpy as np

labels=['a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j']

class Nus2Info(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n Nus II
        The postures are shot in and around National University of Singapore (NUS), against complex natural backgrounds, with various hand shapes and sizes
        More details can be found at https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/
        \nVersion default : normal\nOther version : hn
        """
        url_info = "https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet//"
        download_size = 77233719
        disk_size = 111294775
        subject= 2750
        super().__init__("Nus2",(160,120,3),{"y":"classes"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return Nus2()

class Nus2(DatasetLoader):
    def __init__(self):
        super().__init__("Nus2")
        self.url = 'https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/NUS-Hand-Posture-Dataset-II.zip'
        self._FILENAME = self.name + '.zip'
        self._CLASSES_IDS = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
            'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
        }

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        mkdir_unless_exists(folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(url=self.urls(), filepath=ZIP_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, folderpath,**kwargs):
        images_folderpath = self.images_folderpath(folderpath)
        subsets_folder = os.path.join(images_folderpath,'NUS Hand Posture dataset-II')

        IMAGE_HEIGHT = 120
        IMAGE_WIDTH = 160
        IMAGE_COLORS = 3

        IMAGE_HEIGHT_hn = 240
        IMAGE_WIDTH_hn = 320
        IMAGE_COLORS_hn = 3

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
                logging.debug(f"Loading images from {subset}")

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
                if(subset=='Hand Postures'):
                    x= np.zeros(shape=(NUMBER_OF_IMAGES,
                                                       IMAGE_HEIGHT,
                                                       IMAGE_WIDTH,
                                                       IMAGE_COLORS),
                                                dtype="uint8")

                    y= np.zeros(shape=NUMBER_OF_IMAGES, dtype='uint8')
                else:
                    xn = np.zeros(shape=(NUMBER_OF_IMAGES,
                                        IMAGE_HEIGHT_hn,
                                        IMAGE_WIDTH_hn,
                                        IMAGE_COLORS_hn),
                                 dtype="uint8")

                    yn = np.zeros(shape=NUMBER_OF_IMAGES, dtype='uint8')
                for position, image_name in enumerate(images):
                    # loads the image
                    image_path= os.path.join(subsets_folder,subset)
                    image_path2=os.path.join(image_path, image_name)
                    if(subset=='Hand Postures'):
                        x[position,:,:,:] = io.imread(image_path2)
                        # loads the image klass in the array
                        y[position] = self.get_klass_id_for_filename(
                            image_name)
                    else:
                        xn[position, :, :, :] = io.imread(image_path2)
                        # loads the image klass in the array
                        yn[position] = self.get_klass_id_for_filename(
                            image_name)
            logging.debug(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")
            if 'version' in kwargs:
                options = ['hn', 'normal']
                try:
                    class UnAcceptedValueError(Exception):
                        def __init__(self, data):
                            self.data = data

                        def __str__(self):
                            return repr(self.data)

                    if ((kwargs['version']) != options[0]) and ((kwargs['version']) != options[1]):
                        raise UnAcceptedValueError(
                            f"Version {kwargs['version']} is not valid. Valid options: {options[1]} , {options[0]}")
                    else:
                        if (kwargs['version'] == options[0]):
                            logging.info(f"Loading version: {kwargs['version']}")
                            metadata = {"y": yn}
                            return xn, metadata
                        else:
                            if (kwargs['version'] == options[1]):
                                logging.info(f"Loading version: {kwargs['version']}")
                                metadata = {"y": y}
                                return x, metadata

                except UnAcceptedValueError as e:
                    logging.error(f"Received error:{e.data}")
                    exit()
            else:
                logging.info(f"Loading default version: normal")
                metadata = {"y": y}
                return x, metadata



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
        os.remove(ZIP_PATH)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = self.images_folderpath(fpath)
        npz_exist = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(npz_exist) == 0):
            return False
        else:
            if (os.path.exists(folder)):
                rmtree(folder)
            else:
                return False
            return True