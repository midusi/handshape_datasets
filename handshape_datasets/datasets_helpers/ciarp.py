import os
from . import __utils__


def download_and_extract(folderpath, images_folderpath,download):
    """
    Download the dataset in the folderpath and extract it to images_folderpath.
    Both routes may not exist and in that case they are created.
        :folderpath (str): The path where the zip wi'll be downloaded 
        :images_folderpath (str): The path where the zip wi'll be extracted
    """
    # if the folder doenst exist is created
    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)

    ZIP_PATH = os.path.join(folderpath, 'jsl.zip')
    __utils__.download_file(url='http://home.agh.edu.pl/~bkw/code/ciarp2017/ciarp.zip',
                            filepath=ZIP_PATH)

    EXTRACTED_PATH = os.path.join(images_folderpath, 'ciarp')
    __utils__.extract_zip(ZIP_PATH, EXTRACTED_PATH)

