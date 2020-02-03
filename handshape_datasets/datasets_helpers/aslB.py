from .dataset_loader import DatasetLoader
from ._utils import mkdir_unless_exists, extract_tar, download_bigger_file

import tarfile
import os


class AslB(DatasetLoader):
    def __init__(self):
        super().__init__("aslB")
        self.url = 'http://www.cvssp.org/FingerSpellingKinect2011/dataset9-depth.tar.gz'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath, images_folderpath=None):
        TARFILE_PATH = os.path.join(folderpath, 'aslB.tar.gz')

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_bigger_file(self.urls(), TARFILE_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, path):
        # FIXME Download and check the file structure
        return True

    def preprocess(self, folderpath, images_folderpath=None):
        preprocess_flag = "{}_preprocessed".format(self._name)
        if self.get_status_flag(folderpath, preprocess_flag) is False:
            # if it doenst receives the images_folderpath arg creates into folderpath
            images_folderpath = os.path.join(
                folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
            mkdir_unless_exists(images_folderpath)
            TARFILE_PATH = os.path.join(folderpath, 'aslA.tar.gz')
            # extract the zip into the images path
            extract_tar(TARFILE_PATH, images_folderpath)
            self.set_preprocessed_flag(folderpath)
        # if its already extracted doesnt do anything
