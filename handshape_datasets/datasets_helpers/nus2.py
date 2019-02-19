from ._utils import check_folder_existence, extract_zip
from .dataset_loader import DatasetLoader

import os
import zipfile


class Nus2(DatasetLoader):
    def __init__(self):
        super().__init__("nus1")
        self.url = 'https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/NUS-Hand-Posture-Dataset-II.zip'

    def urls(self):
        return self.url

    def download_and_extract(self, folderpath, images_folderpath=None):
        # if it doenst receives the images_folderpath arg creates into folderpath
        images_folderpath = os.path.join(
            folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
        check_folder_existence(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, 'nus2.zip')

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            self.download_file(self.urls(), ZIP_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)
        # extract the zip into the images path
        extract_zip(ZIP_PATH, images_folderpath)

    def load(self, path):
        return True

    def preprocess(self, path):
        pass
