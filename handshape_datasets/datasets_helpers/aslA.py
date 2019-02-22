from .dataset_loader import DatasetLoader
from ._utils import mkdir_unless_exists, extract_zip

import tarfile
import os


class AslA(DatasetLoader):
    def __init__(self):
        super().__init__("aslA")
        self.url = 'http://www.cvssp.org/FingerSpellingKinect2011/fingerspelling5.tar.bz2'

    def urls(self):
        return self.url

    def download_and_extract(self, folderpath, images_folderpath=None):
        # if it doenst receives the images_folderpath arg creates into folderpath
        images_folderpath = os.path.join(
            folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
        mkdir_unless_exists(images_folderpath)
        TARFILE_PATH = os.path.join(folderpath, 'aslA.tar.gz')

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            self.download_bigger_file(self.urls(), TARFILE_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)
        # extract the zip into the images path
        extract_zip(TARFILE_PATH, images_folderpath)

    def load(self, path):
        return True

    def preprocess(self, path):
        pass