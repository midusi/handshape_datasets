from __utils__ import get_project_root
from pyunpack import Archive

import numpy as np
import os
import zipfile
import requests
import shutil


def download_file(url, filepath):
    with requests.get(url, stream=True) as r:
        print("Downloading {} dataset from {}".format(filepath, url))
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print("Done ƪ(˘⌣˘)ʃ")


def download_and_extract(folderpath, images_folderpath):
    actual_wd = os.getcwd()

    if not os.path.exists(folderpath):
        print("Creating folder %s..." % folderpath)
        os.mkdir(folderpath)

    if not os.path.exists(images_folderpath):
        print("Creating folder %s ..." %
              images_folderpath)
        os.mkdir(images_folderpath)
    print("Downloading Polish Sign Language dataset to folder %s ..." % folderpath)

    # temporal store for the urls readed from file
    urls = {
        'a': [], 'b': [], 'c': [], 'e': [], 'i': [], 'l': [],
        'm': [], 'n': [], 'o': [], 'p': [], 'r': [], 's': [],
        't': [], 'u': [], 'w': [], 'y': []}

    path = os.path.join(get_project_root(), '__data__/psl')

    for person_name in 'ABC':
        folder_name = 'person%s' % person_name
        with open('%s/links.txt' % (os.path.join(path, folder_name)), 'r') as links:
            for line in links:
                info = line.split(',')
                urls[info[0]].append((info[0], info[1][:-1]))

    for folder_name in urls.keys():
        os.chdir(folderpath)  # me paro en la ruta recibida por parametro
        try:
            zips_path = os.path.join(folderpath, folder_name)
            os.mkdir(zips_path)
            # create the same folder on the images path
            imagefolder_path = os.path.join(images_folderpath, folder_name)
            os.mkdir(imagefolder_path)

            os.chdir(folder_name)
            urls_list = [url[1] for url in urls[folder_name]]

            for url in zip(urls_list, ['personA', 'personB', 'personC']):
                filename = "%s.7z" % (url[1])
                download_file(url[0], filename)
                # Archive(os.path.join(zips_path, filename)
                #         ).extractall(imagefolder_path)
                # print("Extracting {} to {}".format(
                #     filename, imagefolder_path))
                # print("DONE ᕦ(ò_óˇ)ᕤ")
                # print("--------------------------------")

        except FileExistsError:
            print(
                """Already exists a folder with the name %s.
                Aborting the download to avoid the overwriting of files""" % folder_name)

        os.chdir(actual_wd)

    # proceed to extract all the zips


folderpath = '/home/brian/Descargas'
images_folderpath = '/home/brian/Descargas/Imágenes'
download_and_extract(folderpath, images_folderpath)
