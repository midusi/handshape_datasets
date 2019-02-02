from __utils__ import download_file, check_folder_existence

import zipfile
import os

def download_and_extract(folderpath, images_folderpath):
    actual_wd = os.getcwd()

    check_folder_existence(folderpath)
    check_folder_existence(images_folderpath)

    zip_path = os.path.join(folderpath, 'jsl.zip')
    download_file(url='http://home.agh.edu.pl/~bkw/research/data/mva/jsl.zip',
                  filepath=zip_path)

    extracted_path = os.path.join(images_folderpath, 'jsl_images')
    with zipfile.ZipFile(file=zip_path,
                         mode="r") as zip_ref:
        print("Extracting jsl.zip to {}".format(extracted_path))
        zip_ref.extractall(path=extracted_path)
        print("DONE ᕦ(ò_óˇ)ᕤ")

    os.chdir(actual_wd)

folderpath = os.path.join(os.getenv('HOME'), 'Descargas', 'jsl')
images_folderpath = os.path.join(os.getenv('HOME'), 'Descargas', 'datasets')
download_and_extract(folderpath, images_folderpath)