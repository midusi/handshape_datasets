from pyunpack import Archive

import os
from . import utils


def download_and_extract(folderpath, images_folderpath, download):
    """
    Download the dataset in the folderpath and extract it to images_folderpath.
    Both routes may not exist and in that case they are created.
        :folderpath (str): The path where the zip wi'll be downloaded
        :images_folderpath (str): The path where the zip wi'll be extracted
    """
    actual_wd = os.getcwd()

    utils.mkdir_unless_exists(folderpath)
    utils.mkdir_unless_exists(images_folderpath)
    success_filename = "indian_download_complete"
    if download is True:
        print("Downloading Indian Sign Language dataset to folder %s ..." % folderpath)

        # temporal store for the urls readed from file
        urls = {
            "depth": [],
            "rgb": []
        }

        path = os.path.join(utils.get_project_root(), '__data__/indian')

        for folder in urls:
            with open('%s/links.txt' % (os.path.join(path, folder)), 'r') as links:
                for line in links:
                    info = line.split(',')
                    urls[folder].append((info[0],
                                         # remove empty spaces and the implicit \nB
                                         info[1].replace(" ", "")[:-1]
                                         ))
        # after links added
        for folder_name in urls:
            os.chdir(folderpath)  # me paro en la ruta recibida por parametro
            try:
                zips_path = os.path.join(folderpath, folder_name)
                os.mkdir(zips_path)
                for url in urls[folder_name]:
                    filename = "%s.tar.gz" % (url[0])
                    utils.download_from_drive(url[1], filename)

                os.chdir("..")
            except FileExistsError:
                print(
                    """Already exists a folder with the name %s.
                    Aborting the download""" % folder_name)
        utils.create_download_complete_file(
            os.path.join(folderpath, success_filename), 'jsl')
    else:
        if utils.download_detector_found(folderpath, success_filename) is False:
            exit(
                "The success file doesn't exists. Try again with the arg download in false")

    # create the same folder on the images path
    # just extraction if the file already exists or no
    for folder_name in urls:
        imagefolder_path = os.path.join(images_folderpath, folder_name)
        os.mkdir(imagefolder_path)

        tarfile_path = os.path.join(folderpath, folder_name)
        extracted_path = os.path.join(images_folderpath, folder_name)
        for url in urls[folder_name]:
            filename = "%s.tar.gz" % (url[0])
            utils.extract_tar(os.path.join(
                tarfile_path, filename), extracted_path)
            print("--------------------------------")

    os.chdir(actual_wd)
