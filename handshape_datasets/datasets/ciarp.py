from .utils import extract_zip, download_file
from handshape_datasets.dataset_loader import DatasetLoader
from skimage import io
import csv
import os
import numpy as np
from enum import Enum

class CiarpVersion(Enum):
    WithoutGabor = "WithoutGabor"
    WithGabor = "WithGabor"

class Ciarp(DatasetLoader):
    def __init__(self,version=CiarpVersion.WithoutGabor):
        super().__init__("ciarp")
        self.url = 'http://home.agh.edu.pl/~bkw/code/ciarp2017/ciarp.zip'
        self.filename = self.name + '.zip'
        self.version=version

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        filepath = os.path.join(folderpath, self.filename)
        download_file(url=self.urls(), filepath=filepath)
        # set the exit flag
        self.set_downloaded(folderpath)

    def read_csv(self,txt_path):
        with open(txt_path) as f:
            print(txt_path)
            reader = csv.reader(f,delimiter=' ')
            filename,y=zip(*reader)
            y=np.array(list(map(int,y )))
        return filename,y

    def load_folder(self,folder,txt_path):

        filenames,y=self.read_csv(txt_path)
        x=np.zeros( (len(y),38,38,1),dtype="uint8")
        for i,filename in enumerate(filenames):
            filepath=os.path.join(folder.path,filename)
            image=io.imread(filepath)
            image=image[:,:,np.newaxis]
            x[i,:]=image
        return x,y

    def load(self,folderpath):
        dataset_folder = os.path.join(folderpath , 'ciarp')

        version_string=self.version.value
        folders = [f for f in os.scandir(dataset_folder) if f.is_dir() and f.path.endswith(version_string) ]

        # start the load
        images_loaded_counter = 0
        # each image is stored in the key corresponding to its subset
        result={}
        for folder in folders:
            print(folder.name)
            txt_name=f"{folder.name}.txt"
            txt_path=os.path.join(dataset_folder,txt_name)
            x,y=self.load_folder(folder,txt_path)
            result[folder.name]=(x,y)
        return result



    def preprocess(self, folderpath):

        zip_path = os.path.join(folderpath, self.filename)
        # extract the zip into the images path
        extract_zip(zip_path, folderpath)
        self.set_preprocessed_flag(folderpath)