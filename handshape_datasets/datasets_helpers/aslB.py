from .dataset_loader import DatasetLoader
from ._utils import mkdir_unless_exists, extract_zip, download_bigger_file

import tarfile
import os


class AslB(DatasetLoader):
    def __init__(self):
        super().__init__("aslb")
        self.url = 'http://www.cvssp.org/FingerSpellingKinect2011/dataset9-depth.tar.gz'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        # if it doenst receives the images_folderpath arg creates into folderpath
        TARFILE_PATH = os.path.join(folderpath, 'aslB.tar.gz')

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_bigger_file(self.urls(), TARFILE_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)
        # extract the zip into the images path

    def load(self, folderpath):
        return None

    def preprocess(self, folderpath, images_folderpath=None):
        images_folderpath = os.path.join(
            folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
        
        mkdir_unless_exists(images_folderpath)
        TARFILE_PATH = os.path.join(folderpath, 'aslB.tar.gz')
        
        extract_zip(TARFILE_PATH, images_folderpath)
        self.set_preprocessed_flag(folderpath)
