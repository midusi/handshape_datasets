import py7zr

from handshape_datasets.dataset_loader import DatasetLoader
from . import utils
import patoolib
from pyunpack import Archive
from logging import warning
from .common import *

import os
import math
import numpy as np
from PIL import Image


import os
from pypcd import pypcd

labels=["a", "b", "c", "e", "i", "l", "m", "n", "o","p","r","s","t","u","w","y"]

class PslInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n PSL
        Polish Sign Language Handshapes dataset 
        More details can be found at http://vision.kia.prz.edu.pl/statictof.php
        """
        url_info = "http://vision.kia.prz.edu.pl/statictof.php"
        download_size = 4
        disk_size = 3
        subject = 8
        super().__init__("psl",(32,32),{"y":"classes"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return Psl()

class Psl(DatasetLoader):
    def __init__(self):
        super().__init__("psl")
        self.url = {
            'person_a': 'https://drive.google.com/uc?export=download&id=1VjRZHI0EcY0e0vSG9AuvbqysTYdcIKek',
            'person_b': 'https://drive.google.com/uc?export=download&id=1rSp0_MauNjru-sVr8JBCueJK4ifeZRHr',
            'person_c': 'https://drive.google.com/uc?export=download&id=1jCujSvltcKZFmrCaTgqTY8--sOLMSuAa'
        }
        self.imagesurls = self.urls()

    def urls(self):
        urls = {person: {} for person in self.url.keys()}
        # fill the urls dictionary
        for person, url in self.url.items():
            links = utils.download_file_content_as_text(url)
            links = links.split('\n')[:-1]  # the last is an empty line
            links = [url.split(',')
                     for url in links]  # [['a','url'],['b','url']]
            for url in links:
                # urls[person_a]['a'] = 'link_to_file'
                urls[person][url[0]] = url[1]
        return urls  # a dict

    def download_dataset(self, folderpath, images_folderpath=None):
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            utils.mkdir_unless_exists(folderpath)
            os.chdir(folderpath)  # change to the received route
            folders = self.imagesurls.keys()  # ['person_a','person_b','person_c']
            for folder_name in folders:
                try:
                    ZIPS_PATH = os.path.join(folderpath, folder_name+'_zips')
                    os.mkdir(ZIPS_PATH)
                    os.chdir(ZIPS_PATH)
                    # iter over the dict with the url
                    for imageClass in self.imagesurls[folder_name]:
                        filename = "%s/%s.7z" % (ZIPS_PATH, imageClass)
                        utils.download_file(
                            self.imagesurls[folder_name][imageClass], filename)

                except FileExistsError:
                    print(
                        """Already exists a folder with the name %s.
                        Aborting the download to avoid the overwriting of files""" % folder_name)
        self.set_downloaded(folderpath)
#
    def read_pcd(self, pcd_path, output_path,i):

        cloud = pypcd.PointCloud.from_path(pcd_path)
        x_column=pypcd.decode_x_from_pcl(cloud.pc_data['x'])
        print(x_column)

        img_height = 480
        img_width = 640
        is_data = False


        min_d = 0
        max_d = 0
        img_depth = np.zeros((img_height, img_width), dtype='f8')
        for (i,line) in enumerate(lines):

            if(i==11):
                dato=line.split(' 'or'\n')
                for (k, dat) in enumerate(dato):
                    if (k==1):
                        x= dat

                    else:
                        if (k==2):
                            y=dat

                        else:
                            if(k==3):
                                z=dat
                            else:
                                int=dat

                d = max(0., float(line[2]))
                i = int(line[4])
                col = i % img_width
                row = math.floor(i / img_width)
                img_depth[row, col] = d
                min_d = min(d, min_d)
                max_d = max(d, max_d)

        max_min_diff = max_d - min_d

        def normalize(x):
            return 255 * (x - min_d) / max_min_diff

        normalize = np.vectorize(normalize, otypes=[np.float])
        img_depth = normalize(img_depth)
        img_depth_file = Image.fromarray(img_depth)
        img_depth_file.convert('RGB').save(os.path.join(output_path,i+ '_depth_image.png'))

    def load(self, folderpath, **kwargs):
        folders = list(
            filter(lambda x: 'psl' not in x, listdir(folderpath)))
        for folder in folders:
            folder_path= os.path.join(folderpath,folder)
            subsets_folder=list(filter(lambda x: '.db' not in x, listdir(folder_path)))
            for subset in subsets_folder:
                subset_path= os.path.join(folder_path,subset)
                subset_folder_folder= list(filter(lambda x: '.db' not in x, listdir(subset_path)))
                for sub in subset_folder_folder:
                    path=os.path.join(subset_path,sub)
                    images=list(filter(lambda x: ".db" not in x, listdir(path)))
                    for (i,image) in enumerate(images):
                        image_path= os.path.join(path, image)
                        self.read_pcd(image_path,path, i)

        return True

    def preprocess(self, folderpath, images_folderpath=None):
        preprocess_flag = "{}_preprocessed".format(self.name)

        folders= list(
            filter(lambda x: 'psl' not in x, listdir(folderpath)))
        if self.get_status_flag(folderpath, preprocess_flag) is False:
            for folder in folders:
                folder_path=os.path.join(folderpath,folder)
                zips = list(
                    filter(lambda x: x[-3:] == '.7z',
                           listdir(folder_path)))
                for zip in zips:
                    zip_path= os.path.join(folder_path, zip)
                    zip_folder= os.path.join(folder_path, zip[0])
                    utils.mkdir_unless_exists(zip_folder)
                    with py7zr.SevenZipFile(zip_path, mode='r') as z:
                        z.extractall(zip_folder)
                    os.remove(zip_path)
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