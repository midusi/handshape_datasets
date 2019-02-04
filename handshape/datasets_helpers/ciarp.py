import __utils__
import os


def download_and_extract(folderpath, images_folderpath):

    # if the folder doenst exist is created
    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)

    zip_path = os.path.join(folderpath, 'jsl.zip')
    __utils__.download_file(url='http://home.agh.edu.pl/~bkw/code/ciarp2017/ciarp.zip',
                            filepath=zip_path)

    extracted_path = os.path.join(images_folderpath, 'ciarp')
    __utils__.extract_zip(zip_path,extracted_path)
