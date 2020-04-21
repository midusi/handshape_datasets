from handshape_datasets.dataset_loader import DatasetLoader
from . import utils
from pyunpack import Archive
from logging import warning
from .common import *

import os


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

    def load(self, extracted_images_folderpath, **kwargs):
        return True

    def preprocess(self, folderpath, images_folderpath=None):
        preprocess_flag = "{}_preprocessed".format(self.name)
        if self.get_status_flag(folderpath, preprocess_flag) is False:
            utils.mkdir_unless_exists(images_folderpath)
            images_folderpath = os.path.join(
                folderpath, "%s_images" % self.name) if images_folderpath is None else images_folderpath
            os.chdir(images_folderpath)
            for image_class in self.url.keys():
                images_class_foldername = os.path.join(
                    images_folderpath, image_class)
                os.mkdir(images_class_foldername)
                os.chdir(images_class_foldername)
                to_extract_current_dir = os.getcwd()
                try:
                    CURRENT_SUBSET_ZIPS_PATH = folderpath+f"/{image_class}_zips"
                    os.chdir(CURRENT_SUBSET_ZIPS_PATH)
                    FILES = os.listdir()
                    for filename in FILES:
                        Archive(filename).extractall(to_extract_current_dir) # extract into person_a in images folder
                except FileNotFoundError:
                    warning(
                        "Folder with zips not found. Make sure you haven't modified the original structure of the files.")

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = self.images_folderpath(fpath)
        npz_exist = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(npz_exist) == 0):
            return False
        else:
            rmtree(folder)
            return True