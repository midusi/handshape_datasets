from __utils__ import download_file, check_folder_existence

import zipfile
import os

def download_and_extract(folderpath, images_folderpath):

    check_folder_existence(folderpath) # if the folder doenst exist is created
    check_folder_existence(images_folderpath)

    zip_path = os.path.join(folderpath, 'jsl.zip')
    download_file(url='http://home.agh.edu.pl/~bkw/code/ciarp2017/ciarp.zip',
                  filepath=zip_path)

    extracted_path = os.path.join(images_folderpath, 'ciarp')
    with zipfile.ZipFile(file=zip_path,
                         mode="r") as zip_ref:
        print("Extracting jsl.zip to {}".format(extracted_path))
        zip_ref.extractall(path=extracted_path)
        print("DONE ᕦ(ò_óˇ)ᕤ")

