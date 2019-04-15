from abc import ABC, abstractmethod
from urllib.parse import urlparse


import os
import logging
import gdown


class DatasetLoader(ABC):

    def __init__(self, name):
        self._name = name

    @property
    @abstractmethod
    def urls(self):
        """Returns the urls from the dataset
        """
        pass

    @abstractmethod
    def download_dataset(self, path):
        """Downloads the dataset in the specified path

        Args:
            path (str): The folder where the dataset will be downloaded
        Example:
            >>> dataset.download_dataset("$HOME/Downloads/Datasets")
        """
        pass

    def get(self, filepath, images_folderpath, **kwargs):
        """The methods take care of download the dataset,
        preprocess it and load it in memory

        Args:
            filepath (str): The path where the datasets files will be downloaded
            images_folderpath ([type]): [description]

        Returns:
            [type]: [description]
        """
        path = os.path.join(filepath, self._name)
        if not os.path.exists(path):
            logging.warning(
                f"Creating folder {path} for the dataset {self._name}")
            os.mkdir(path)
        if not self.get_downloaded_flag(path):
            self.download_dataset(path)
        if not self.get_preprocessed_flag(path):
            logging.warning(f"Preprocessing {self._name}...")
            self.preprocess(path, images_folderpath)
            logging.warning("Done")
        return self.load(images_folderpath)

    def get_downloaded_flag(self, path):
        """
        Check if downloaded flag exists in path

        Args:
            path(str): The route where to look for the downloaded flag
        """
        return self.get_status_flag(path, "{}_downloaded".format(self._name))

    def get_preprocessed_flag(self, path):
        """
        Check if preprocessed flag exists in path

        Args:
            path(str): The route where to look for the preprocessed flag
        """
        return self.get_status_flag(path, "{}_preprocessed".format(self._name))

    def get_status_flag(self, path, status):
        """
        Checks if the filename(status) received exists in path.
        The flags are used as checkpoints to avoid unnecessary repetition of processes.

        Args:
            path(str): The path where to look for the file
            status(str): The name of the file to find

        Returns:
            bool: The return value. True if the file exists, False otherwise
        """
        status_path = os.path.join(path, status)
        return os.path.exists(status_path)

    @abstractmethod
    def load(self, image_files_path):
        """
        Loads dataset images in memory and instance to a dataset class object.
        The management of the load of the images in memory varies according to the implementation.

        Args:
            image_files_path(str): The path where the images were extracted

        Returns:
            Dataset: An instance from the object dataset than receives the loaded images as data
        """
        pass


    @abstractmethod
    def preprocess(self, path, images_folderpath=None):
        """
        The process in which the dataset files are extracted and moved to a uniform folder received as argument

        Args:
            path(str): The path where the downloaded files are located (The files must be at the root of the filepath)
            images_folderpath(str,optional): The path where the images will be extracted. Default to None

        Examples: (INTERN IMPLEMENTATION)
            >> preprocess(path='./datasetName',images_folderpath='./images')
            - With this the file/s WILL BE EXTRACTED in './images'-> images/all_the_dataset_file_images
        """
        pass

    def set_downloaded(self, path):
        """
        Creates the downloaded flag in the path received with the name of the dataset

        Args:
            path(str) : The path where the flag file will be setted
        """
        self._set_status_flag(path, "{}_downloaded".format(self._name))

    def set_preprocessed_flag(self, path):
        """
        Creates the preprocessed flag in the path received with the name of the dataset

        Args:
            path(str) : The path where the flag file will be setted
        """
        self._set_status_flag(path, "{}_preprocessed".format(self._name))

    def _set_status_flag(self, path, status):
        """
        Flags are used as a way to control that a stage ended successfully.
        This method creates a file used for that control process.

        Args:
            path(str): The path where the status file will be created
            status(str): The name of the status file
        """
        status_path = os.path.join(path, status)
        if not os.path.exists(status_path):
            open(status_path, 'a').close()
        else:
            raise ValueError(f"Status {status} already set on {path}")
