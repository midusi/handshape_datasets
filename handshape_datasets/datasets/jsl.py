from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from handshape_datasets.dataset_loader import DatasetLoader
from skimage import io
from logging import warning
from .common import *
import os


class Jsl(DatasetLoader):
    def __init__(self):
        super().__init__("jsl")
        self.url = 'http://home.agh.edu.pl/~bkw/research/data/mva/jsl.zip'
        self._FILENAME = self.name + '.zip'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        download_file(self.urls(), filepath=ZIP_PATH,
                      filename=self._FILENAME)
        # set the download flag
        self.set_downloaded(folderpath)

    def load(self, folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        if os.path.exists(images_folderpath ):
            subsets = {
                "data": []
            }
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            # all images in thexe folder:
            warning(f"Loading images from {images_folderpath }")
            for image in os.listdir(images_folderpath ):
                image_path=os.path.join(images_folderpath,image)
                subsets["data"].append(io.imread(image_path, as_gray=True))
                images_loaded_counter += 1

            warning(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")
            dataset = Dataset(self.name, subsets)
            return dataset

    def preprocess(self, folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # extract the zip into the images_folderpath
        extract_zip(ZIP_PATH, images_folderpath)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = os.path.join(fpath, self.folder_name)
        subsets_folders = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(subsets_folders) == 0):
            return print("npz not found")
        else:
            # rmtree(folder)
            print("Folders delete")

        return True