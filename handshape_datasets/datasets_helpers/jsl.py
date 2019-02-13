from . import __utils__

import os
import zipfile


def download_and_extract(folderpath, images_folderpath, download):
    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)
    zip_path = os.path.join(folderpath, 'jsl.zip')
    success_filename = "jsl_download_complete"

    if download is True:
        "Downloading Dataset. A download_complete file will be created in the folderpath when download is done"
        try:
            __utils__.download_file(url='http://home.agh.edu.pl/~bkw/research/data/mva/jsl.zip',
                                    filepath=zip_path)
        except FileExistsError:
            exit("The file already exists.")
        __utils__.create_download_complete_file(
            os.path.join(folderpath, success_filename), 'jsl')
    else:
        if __utils__.download_detector_found(folderpath, success_filename) is False:
            print(
                "The success file doesn't exists. Try again with the arg download in false")

    extracted_path = os.path.join(images_folderpath, 'jsl_images')
    __utils__.extract_zip(zip_path, extracted_path)
