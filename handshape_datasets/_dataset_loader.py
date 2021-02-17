from abc import ABC, abstractmethod
from urllib.parse import urlparse
from pathlib import Path

import os
import logging


default_folder = Path.home() / '.handshape_datasets'

class DatasetLoader(ABC):

    def __init__(self, name):
        self.name = name

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
        """
        pass

    @abstractmethod
    def delete_temporary_files(self, path, **kwargs):
        """


        """
        pass

    def get(self, filepath:Path, **kwargs):
        """Downloads and load the dataset.

        Args:
            filepath (str): The path where the datasets files will be downloaded
        Returns:
            [type]: [description]
        """
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        path = filepath / self.name
        if not path.exists():
            logging.info(
                f"Creating folder {path} for the dataset {self.name}")
            path.mkdir()

        if not self.get_downloaded_flag(path):
            self.download_dataset(path)
            logging.info("Download Complete ƪ(˘⌣˘)ʃ")
        if not self.get_preprocessed_flag(path):
            logging.info(f"Preprocessing {self.name}...")
            self.preprocess(path)
            logging.info("Done ƪ(˘⌣˘)ʃ")
        load = self.load(path, **kwargs)
        if 'delete' in kwargs:
            if (kwargs['delete']==True):
                flag=self.delete_temporary_files(default_folder)
                if(flag):
                    logging.info("Delete Complete ƪ(˘⌣˘)ʃ")
                else:
                    logging.warning(".npz not found")
        return load

    def images_folderpath(self,folderpath:Path)->Path:
        return folderpath / f"{self.name}_images"

    def get_downloaded_flag(self, path:Path):
        """
        Check if downloaded flag exists in path

        Args:
            path(str): The route where to look for the downloaded flag
        """
        return self.get_status_flag(path, "{}_downloaded".format(self.name))

    def get_preprocessed_flag(self, path:Path):
        """
        Check if preprocessed flag exists in path
        Args:
            path(str): The route where to look for the preprocessed flag
        """
        return self.get_status_flag(path, "{}_preprocessed".format(self.name))

    def get_status_flag(self, path:Path, status:str):
        """
        Checks if the filename(status) received exists in path.
        The flags are used as checkpoints to avoid unnecessary repetition of processes.
        Args:
            path(str): The path where to look for the file
            status(str): The name of the file to find

        Returns:
            bool: The return value. True if the file exists, False otherwise
        """
        status_path = path / status
        return status_path.exists()

    @abstractmethod
    def load(self, image_files_path:Path, **kwargs):
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
    def preprocess(self, path:Path):
        """
        The process in which the dataset files are extracted and moved to a uniform folder received as argument

        Args:
            path(str): The path where the downloaded files are located (The files must be at the root of the filepath)
        """
        pass

    def set_downloaded(self, path:Path):
        """
        Creates the downloaded flag in the path received with the name of the dataset

        Args:
            path(str) : The path where the flag file will be setted
        """
        self._set_status_flag(path, "{}_downloaded".format(self.name))

    def set_preprocessed_flag(self, path:Path):
        """
        Creates the preprocessed flag in the path received with the name of the dataset

        Args:
            path(str) : The path where the flag file will be setted
        """
        self._set_status_flag(path, "{}_preprocessed".format(self.name))

    def _set_status_flag(self, path:Path, status:str):
        """
        Flags are used as a way to control that a stage ended successfully.
        This method creates a file used for that control process.

        Args:
            path(str): The path where the status file will be created
            status(str): The name of the status file
        """
        status_path = path / status
        if not status_path.exists():
            open(status_path, 'a').close()
        else:
            raise ValueError(f"Status {status} already set on {path}")
