from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset_loader import DatasetLoader
import numpy as np
import os

from skimage import io




class LSA16(DatasetLoader):
    def __init__(self,version="lsa32x32_nr_rgb_black_background"):
        #TODO generate URL from options
        super().__init__("lsa16")
        self.filename = f"{version}.zip"
        self.url = f'http://facundoq.github.io/unlp/lsa16/data/{self.filename}'
        self.shape= (32,32) # TODO get from version
        self.classes = 16

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):

        #zip_filepath= os.path.join(folderpath, self.filename)

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(url=self.urls(), filepath=folderpath,
                          filename=self.filename)

            # set the exit flag
            self.set_downloaded(folderpath)

    def images_folderpath(self,folderpath):
        return os.path.join(folderpath, "%s_images" % self.name)

    def preprocess(self, folderpath):

        zip_filepath = os.path.join(folderpath, self.filename)
        if self.get_preprocessed_flag(folderpath) is False:
            # if it doenst receives the images_folderpath arg creates into folderpath
            images_folderpath = self.images_folderpath(folderpath)
            mkdir_unless_exists(images_folderpath)

            # extract the zip into the images path
            extract_zip(zip_filepath, images_folderpath)
            self.set_preprocessed_flag(folderpath)
        # if its already extracted doesnt do anything

    def load(self,folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        # get image file names
        files = sorted(os.listdir(images_folderpath ))
        files = list(filter(lambda f: os.path.splitext(f)[1].endswith("jpg")
                            or os.path.splitext(f)[1].endswith("png")
                            or os.path.splitext(f)[1].endswith("jpeg"), files))
        n = len(files)
        # pre-generate matrices
        x = np.zeros((n, self.shape[0], self.shape[1], 3), dtype='uint8')
        y = np.zeros(n, dtype='uint8')
        subjects = np.zeros(n)

        # Load images with labels
        for (i, filename) in enumerate(files):
            # load image
            image = io.imread(os.path.join(images_folderpath, filename))
            x[i, :, :, :] = image
            # Get class and subject id for image
            y[i] = int(filename.split("_")[0]) - 1
            subjects[i] = int(filename.split("_")[1]) - 1
        metadata={"y":y,"subjects":subjects}
        return x, metadata