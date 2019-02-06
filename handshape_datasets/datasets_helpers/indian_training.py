from pyunpack import Archive

import os
import __utils__


def download_and_extract(folderpath, images_folderpath, download):
    """
    Download the dataset in the folderpath and extract it to images_folderpath.
    Both routes may not exist and in that case they are created.
        :folderpath (str): The path where the zip wi'll be downloaded
        :images_folderpath (str): The path where the zip wi'll be extracted
    """
    actual_wd = os.getcwd()

    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)

    print("Downloading Indian Sign Language dataset to folder %s ..." % folderpath)

    # temporal store for the urls readed from file
    urls = {
        "depth": [],
        "rgb": []
    }

    path = os.path.join(__utils__.get_project_root(), '__data__/indian')

    for folder in urls:
        with open('%s/links.txt' % (os.path.join(path, folder)), 'r') as links:
            for line in links:
                info = line.split(',')
                urls[folder].append((info[0],
                                     # remove empty spaces and the implicit \nB
                                     info[1].replace(" ", "")[:-1]
                                     ))

    for folder_name in urls:
        os.chdir(folderpath)  # me paro en la ruta recibida por parametro
        try:
            zips_path = os.path.join(folderpath, folder_name)
            os.mkdir(zips_path)
            # create the same folder on the images path
            imagefolder_path = os.path.join(images_folderpath, folder_name)
            os.mkdir(imagefolder_path)

            os.chdir(folder_name)
            for url in urls[folder_name]:
                filename = "%s.tar.gz" % (url[0])
                __utils__.download_from_drive(url[1], filename)

                tarfile_path = os.path.join(folderpath, folder_name)
                extracted_path = os.path.join(images_folderpath, folder_name)

                __utils__.extract_tar(os.path.join(
                    tarfile_path, filename), extracted_path)
                print("--------------------------------")

        except FileExistsError:
            print(
                """Already exists a folder with the name %s.
                Aborting the download""" % folder_name)

    os.chdir(actual_wd)


download_and_extract(
    os.path.join(os.getenv('HOME'), 'Descargas'),
    os.path.join(os.getenv('HOME'), 'Descargas', 'Datasets'),
    True
)
