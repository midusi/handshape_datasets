import numpy as np
import os
import zipfile
import requests
import shutil


def download_file(url, filepath):
    with requests.get(url, stream=True) as r:
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def download_and_extract(folderpath, images_folderpath):
    if not os.path.exists(folderpath):
        print("Creating folder %s..." % folderpath)
        print("Creating folder %s..." % images_folderpath)
        os.mkdir(images_folderpath)

    print("Downloading Polish Sign Language dataset to folder %s ..." % folderpath)
    actual_dir = os.getcwd()
    os.chdir('__data__/psl/')

    # temporal store for the urls readed from file
    urls = {
        'a': [], 'b': [], 'c': [], 'e': [], 'i': [], 'l': [],
        'm': [], 'n': [], 'o': [], 'p': [], 'r': [], 's': [],
        't': [], 'u': [], 'w': [], 'y': [] }

    for folder in os.listdir():
        os.chdir(folder)
        with open('./links.txt', 'r') as links:
            for line in links:
                info = line.split(',')
                urls[info[0]].append((folder, info[1][:-1]))
        os.chdir('..')

    os.chdir(actual_dir)
    for folder_name in urls.keys():
        path = os.path.join(folderpath, folder_name)
        print(path)
        if not os._exists(path):
            os.mkdir(path)
        os.chdir(path)


folderpath = '/home/brian/Descargas'
images_folderpath = '~/Descargas/Imágenes'
download_and_extract(folderpath, images_folderpath)
