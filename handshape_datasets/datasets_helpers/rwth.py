from ._utils import mkdir_unless_exists, extract_tar, download_file_over_ftp
from .dataset_loader import DatasetLoader
from logging import warning

import os


class Rwth(DatasetLoader):
    def __init__(self):
        super().__init__("rwth-phoenix")
        self.url = 'ftp://wasserstoff.informatik.rwth-aachen.de/pub/rwth-phoenix/2016/ph2014-dev-set-handshape-annotations.tar.gz'
        self.FILENAME = self._name+'.tar.gz'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        TARFILE_PATH = os.path.join(folderpath, self.FILENAME)

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file_over_ftp(ftp_url='wasserstoff.informatik.rwth-aachen.de',
                                   ftp_relative_file_path='pub/rwth-phoenix/2016',
                                   ftp_filename='ph2014-dev-set-handshape-annotations.tar.gz',
                                   filepath=TARFILE_PATH,
                                   filename=self.FILENAME)
            # set the success flag
            self.set_downloaded(folderpath)
        

    def load(self, path):
        return True

    def preprocess(self, folderpath, images_folderpath=None):
        if self.get_preprocessed_flag(folderpath) is False:
            # if it doenst receives the images_folderpath arg creates into folderpath
            images_folderpath = os.path.join(
                folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
            mkdir_unless_exists(images_folderpath)
            TARFILE_PATH = os.path.join(folderpath, self.FILENAME)
            # extract the tar into the images path
            extract_tar(TARFILE_PATH, images_folderpath)
            self.set_preprocessed_flag(folderpath)
        # if its already extracted doesnt do anything
