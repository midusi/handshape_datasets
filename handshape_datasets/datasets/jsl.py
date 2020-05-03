from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from handshape_datasets.dataset_loader import DatasetLoader
from skimage import io
import logging
from .common import *
import os
from pyunpack import Archive
from handshape_datasets.dataset_loader import DatasetLoader
from . import utils

labels=['a',' i', 'u', 'e', 'o','ka', 'ki','ku','ke','ko',
'sa','shi','su','se','so','ta','chi','tsu','te','to',
'na','ni','nu','ne','ha','hi','hu','he','ho','ma',
'mi','mu','me','ya','yu','yo','ra','ru','re','ro','wa']

class JslInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n JSL
        Japanese Sign Language Handshapes dataset 
        More details can be found at https://ieeexplore.ieee.org/document/7986796?denied=
        """
        url_info = "https://ieeexplore.ieee.org/document/7986796?denied="
        download_size = 4691517
        disk_size = 3547685 + download_size
        subject = 8055
        super().__init__("jsl",(32,32),{"y":"classes"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return Jsl()


class Jsl(DatasetLoader):
    def __init__(self):
        super().__init__("jsl")
        self.url = 'http://home.agh.edu.pl/~bkw/research/data/mva/jsl.zip'
        self._FILENAME = self.name + '.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        download_file(self.urls(), filepath=ZIP_PATH)
        # set the download flag
        self.set_downloaded(folderpath)

    def load(self, folderpath, **kwargs):
        images_folderpath = self.images_folderpath(folderpath)

        if os.path.exists(images_folderpath ):
            files = sorted(Path(images_folderpath).iterdir())
            files = list(filter(lambda f: f.suffix in [".jpg", ".png", ".jpeg"], files))
            n = len(files)
            x = np.zeros((n, 32, 32,1), dtype='uint8')
            y = np.array((),dtype='uint8')
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            # all images in thexe folder:
            logging.info(f"Loading images from {images_folderpath }")
            for (i,image) in enumerate(os.listdir(images_folderpath )):
                image_path=os.path.join(images_folderpath,image)
                image1=io.imread(image_path)
                image1 = image1[:, :, np.newaxis]
                x[i, :] = image1
                images_loaded_counter += 1
                label= ((ord(image[9])-48)*10+ord(image[10])-48)-1
                y=np.append(y,label)
            metadata= {"y":y}
            return x, metadata

    def preprocess(self, folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # extract the zip into the images_folderpath
        extract_zip(ZIP_PATH, images_folderpath)
        os.remove(ZIP_PATH)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = self.images_folderpath(fpath)
        subsets_folders = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(subsets_folders) == 0):
            return False
        else:
            if (os.path.exists(folder)):
                rmtree(folder)
            else:
                return False
            return True