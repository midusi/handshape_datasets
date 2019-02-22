from pyunpack import Archive

import os
from . import _utils


def download_and_extract(folderpath, images_folderpath, download):
    """
    Download the dataset in the folderpath and extract it to images_folderpath.
    Both routes may not exist and in that case they are created.
        :folderpath (str): The path where the zip wi'll be downloaded 
        :images_folderpath (str): The path where the zip wi'll be extracted
    """
    actual_wd = os.getcwd()

    _utils.mkdir_unless_exists(folderpath)
    _utils.mkdir_unless_exists(images_folderpath)

    print("Downloading Polish Sign Language dataset to folder %s ..." % folderpath)

    # temporal store for the urls readed from file
    urls = {
        'a': [], 'b': [], 'c': [], 'e': [], 'i': [], 'l': [],
        'm': [], 'n': [], 'o': [], 'p': [], 'r': [], 's': [],
        't': [], 'u': [], 'w': [], 'y': []}

    path = os.path.join(_utils.get_project_root(), '__data__/psl')

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
                _utils.download_file(url[0], filename)
                zip_path = os.path.join(imagefolder_path, url[1])
                Archive(filename=os.path.join(zips_path, filename)
                        ).extractall(zip_path, True)
                print("Extracting {} to {}".format(
                    filename, zip_path))
                print("DONE ᕦ(ò_óˇ)ᕤ")
                print("--------------------------------")

        except FileExistsError:
            print(
                """Already exists a folder with the name %s.
                Aborting the download to avoid the overwriting of files""" % folder_name)

        os.chdir(actual_wd)
