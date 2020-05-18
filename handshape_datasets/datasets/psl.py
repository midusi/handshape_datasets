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

labels=["a", "b", "c", "e", "i", "l", "m", "n", "o","p","r","s","t","u","w","y"]

label_dict =	{
  "a": 0,
  "b": 1,
  "c": 2,
  "e": 3,
  "i": 4,
  "l": 5,
  "m": 6,
  "n": 7,
  "o": 8,
  "p": 9,
  "r": 10,
  "s": 11,
  "t": 12,
  "u": 13,
  "w": 14,
  "y": 15,
}

class PslInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n PSL
        Polish Sign Language Handshapes dataset 
        More details can be found at http://vision.kia.prz.edu.pl/statictof.php
        """
        url_info = "http://vision.kia.prz.edu.pl/statictof.php"
        download_size = 299077505
        disk_size = download_size+980552843
        subject = 960
        super().__init__("psl",(176,144),{"y":"classes"},description, labels, download_size, disk_size, subject, url_info)
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
    def read_pcd(self, pcd_path, output_path,j):

        with open(pcd_path, "r") as pcd_file:
            lines = pcd_file.readlines()
        w=lines[6].split(' ')
        h = lines[7].split(' ')
        img_height =int(h[1])
        img_width = int(w[1])
        max_z = -999
        min_z = 999
        z=np.array(())

        img_depth = np.zeros((img_height, img_width), dtype='f8')

        for (i, line) in enumerate(lines):

            if (i > 10):
                dato = line.split(' ' or '\n')
                dat_float = float(dato[2])
                z = np.append(z, dat_float)
                z_act=dat_float
                if (dat_float > max_z):
                    max_z = dat_float
                if (dat_float < min_z):
                    min_z = dat_float
                index=i-11
                col = index % img_width
                row = math.floor(index / img_width)
                img_depth[row, col] = z_act
        max_min_diff_z = max_z - min_z
        def normalize(x):
            return 255 * (x - min_z) / max_min_diff_z
        normalize = np.vectorize(normalize, otypes=[np.float])
        img_depth = normalize(img_depth)
        img_depth_file = Image.fromarray(img_depth)
        img_depth_file.convert('RGB').save(os.path.join(output_path, str(j)+'_depth_img.png'))

    def convert_to_rgb(self, folderpath):
        folders = list(
            filter(lambda x: 'psl' not in x, listdir(folderpath)))
        for folder in folders:
            folder_path = os.path.join(folderpath, folder)
            subsets_folder = list(filter(lambda x: '.db' not in x, listdir(folder_path)))
            for subset in subsets_folder:
                subset_path = os.path.join(folder_path, subset)
                subset_folder_folder = list(filter(lambda x: '.db' not in x, listdir(subset_path)))
                for sub in subset_folder_folder:
                    path = os.path.join(subset_path, sub)
                    images = list(filter(lambda x: ".pcd" in x, listdir(path)))
                    for (i, image) in enumerate(images):
                        image_path = os.path.join(path, image)
                        output_path = os.path.join(path, "rgb-images")
                        utils.mkdir_unless_exists(output_path)
                        self.read_pcd(image_path, output_path, i)

    def load(self, folderpath, **kwargs):
        rgb_images="{}_rgb_images".format(self.name)
        count_image=0
        IMAGE_WIDTH=176
        IMAGE_HIGH=144
        y = np.array((),dtype='uint8')
        if self.get_status_flag(folderpath, rgb_images) is False:
            self.convert_to_rgb(folderpath)
            self._set_status_flag(folderpath, "{}_rgb_images".format(self.name))
        folders = list(
            filter(lambda x: 'psl' not in x, listdir(folderpath)))
        for folder in folders:
            folder_path = os.path.join(folderpath, folder)
            subsets_folder = list(filter(lambda x: '.db' not in x, listdir(folder_path)))
            for subset in subsets_folder:
                subset_path = os.path.join(folder_path, subset)
                subset_folder_folder = list(filter(lambda x: '.db' not in x, listdir(subset_path)))
                for sub in subset_folder_folder:
                    path = os.path.join(subset_path, sub)
                    rgb_path = list(filter(lambda x: ".pcd" not in x, listdir(path)))
                    for rgb_image_path in rgb_path:
                        path_1 = os.path.join(path, rgb_image_path)
                        image_paths = list(filter(lambda x: ".png" in x, listdir(path_1)))
                        count_image=count_image+len(image_paths)
        x = np.zeros((count_image, IMAGE_HIGH, IMAGE_WIDTH, 3), dtype='uint8')
        index = 0
        for folder in folders:
            folder_path_img = os.path.join(folderpath, folder)
            subsets_folder_img = list(filter(lambda x: '.db' not in x, listdir(folder_path_img)))
            label = -1
            for subset in subsets_folder_img:
                subset_path_img = os.path.join(folder_path_img, subset)
                subset_folder_folder_img = list(filter(lambda x: '.db' not in x, listdir(subset_path_img)))

                for sub in subset_folder_folder_img:
                    path_img = os.path.join(subset_path_img, sub)
                    rgb_path_img = list(filter(lambda x: ".pcd" not in x, listdir(path_img)))
                    label= label_dict[sub]
                    for rgb_image_path in rgb_path_img:
                        path_1_img = os.path.join(path_img, rgb_image_path)
                        image_paths_img = list(filter(lambda x: ".png" in x, listdir(path_1_img)))
                        for image in image_paths_img:
                            path_image= os.path.join(path_1_img,image)
                            x[index, :, :, :] = io.imread(path_image)
                            y = np.append(y, label)
                            index += 1
        metadata={"y":y}
        return x, metadata

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