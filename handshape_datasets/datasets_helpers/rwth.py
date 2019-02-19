from ._utils import check_folder_existence, extract_zip
from .dataset_loader import DatasetLoader

import tarfile
import os


class Rwth(DatasetLoader):
    def __init__(self):
        super().__init__("rwth-phoenix")
        self.url = 'ftp://wasserstoff.informatik.rwth-aachen.de/pub/rwth-phoenix/2016/ph2014-dev-set-handshape-annotations.tar.gz'

    def urls(self):
        return self.url

    def download_and_extract(self, folderpath, images_folderpath=None):
        # if it doenst receives the images_folderpath arg creates into folderpath
        images_folderpath = os.path.join(
            folderpath, "%s_images" % self._name) if images_folderpath is None else images_folderpath
        check_folder_existence(images_folderpath)
        TARFILE_PATH = os.path.join(folderpath, 'rwth-phoenix.tar.gz')

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            self.download_file_over_ftp(ftp_url='wasserstoff.informatik.rwth-aachen.de',
                                        ftp_relative_file_path='pub/rwth-phoenix/2016',
                                        ftp_filename='ph2014-dev-set-handshape-annotations.tar.gz',
                                        filepath=TARFILE_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)
        # extract the zip into the images path
        extract_zip(TARFILE_PATH, images_folderpath)

    def load(self, path):
        return True

    def preprocess(self, path):
        pass
