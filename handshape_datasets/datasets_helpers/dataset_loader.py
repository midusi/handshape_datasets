from abc import ABC, abstractmethod
from urllib.parse import urlparse
from shutil import copyfileobj
from requests import get as get_file
from ftplib import FTP

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
    def download_and_extract(self, path, images_folderpath):
        pass

    def download_file(self, url, filepath):
        """
        download a file from an url and stores it in filepath
        :param url:
        :param filepath:
        """
        with get_file(url, stream=True) as r:
            # with stream in true the file doen't save in memory inmediately
            # it doesn't dowload the content just the headers and the conection keep open
            logging.warning(
                f"Downloading {filepath} from {url}")
            with open(filepath, 'wb') as f:
                copyfileobj(r.raw, f)
        logging.warning("Download Complete ƪ(˘⌣˘)ʃ")

    def download_from_drive(self, url, filepath):
        logging.warning("Downloading {} dataset from {}".format(filepath, url))
        gdown.download(url, filepath, quiet=True)
        logging.warning("Done ƪ(˘⌣˘)ʃ")

    def download_file_over_ftp(self, ftp_url, ftp_relative_file_path, ftp_filename, filepath):
        ftp = FTP(ftp_url)
        ftp.login()
        ftp.cwd(ftp_relative_file_path)
        with open(filepath, 'wb') as f:
            logging.warning("Downloading the dataset...")
            ftp.retrbinary('RETR {}'.format(ftp_filename), f.write)
            logging.warning("Done ƪ(˘⌣˘)ʃ")

    def download_bigger_file(self, url, filepath):
        """
            download a file from an url and stores it in filepath
            :param url:
            :param filepath:
        """
        with get_file(url, stream=True) as r:
            # with stream in true the file doen't save in memory inmediately
            # it doesn't dowload the content just the headers and the conection keep open
            logging.warning(f"Downloading {filepath} dataset from {url}")
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=512 * 1024):
                    if chunk:
                        f.write(chunk)
        logging.warning("Done ƪ(˘⌣˘)ʃ")

    def get(self, filepath, images_folderpath, **kwargs):
        path = os.path.join(filepath, self._name)
        if not os.path.exists(path):
            logging.warning(
                f"Creating folder {path} for the dataset {self._name}")
            os.mkdir(path)
        if not self.get_downloaded_flag(path):
            self.download_and_extract(path, images_folderpath)
        if not self.get_preprocessed_flag(path):
            logging.warning(f"Preprocessing {self._name}...")
            self.preprocess(path)
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
    def preprocess(self, path):
        pass

    def set_downloaded(self, path):
        self._set_status_flag(path, "{}_downloaded".format(self._name))

    def set_preprocessed_flag(self, path):
        self._set_status_flag(path, "preprocessed")

    def _set_status_flag(self, path, status, value=True):
        status_path = os.path.join(path, status)
        if not os.path.exists(status_path):
            open(status_path, 'a').close()
        else:
            raise ValueError(f"Status {status} already set on {path}")
