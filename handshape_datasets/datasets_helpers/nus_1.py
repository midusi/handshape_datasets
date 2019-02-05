import __utils__
import os


def download_and_extract(folderpath, images_folderpath,download):

    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)

    zip_path = os.path.join(folderpath, 'jsl.zip')
    __utils__.download_file(url='https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/NUS-Hand-Posture-Dataset-I.zip',
                  filepath=zip_path)

    extracted_path = os.path.join(images_folderpath, 'nus1_images')
    __utils__.extract_zip(zip_path, extracted_path)