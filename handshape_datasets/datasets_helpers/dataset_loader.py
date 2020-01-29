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
        pass

    @abstractmethod
    def download_dataset(self, path):
        pass

    def get(self, filepath, images_folderpath, **kwargs):
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
        return self.get_status_flag(path, "{}_downloaded".format(self._name))

    def get_preprocessed_flag(self, path):
        return self.get_status_flag(path, "preprocessed")

    def get_status_flag(self, path, status):
        status_path = os.path.join(path, status)
        return os.path.exists(status_path)

    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod
    def preprocess(self, path, images_folderpath):
        pass

    def set_downloaded(self, path):
        self._set_status_flag(path, "{}_downloaded".format(self._name))

    def set_preprocessed_flag(self, path):
        self._set_status_flag(path, "{}_preprocessed".format(self._name))

    def _set_status_flag(self, path, status, value=True):
        status_path = os.path.join(path, status)
        if not os.path.exists(status_path):
            open(status_path, 'a').close()
        else:
            raise ValueError(f"Status {status} already set on {path}")
