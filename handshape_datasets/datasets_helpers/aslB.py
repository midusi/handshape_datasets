import tarfile
from . import __utils__
import os

def download_and_extract(folderpath, images_folderpath,download):
    
    # if the folder doenst exist is created
    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)

    tarfile_path = os.path.join(folderpath, 'aslB.tar.gz')
    __utils__.download_file(url='http://www.cvssp.org/FingerSpellingKinect2011/dataset9-depth.tar.gz',
                            filepath=tarfile_path)

    extracted_path = os.path.join(images_folderpath, 'aslB')
    __utils__.extract_tar(tarfile_path,extracted_path)