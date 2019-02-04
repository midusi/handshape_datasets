import tarfile
import __utils__
import os

def download_and_extract(folderpath, images_folderpath):
    
    # if the folder doenst exist is created
    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)

    tarfile_path = os.path.join(folderpath, 'aslB.tar.gz')
    __utils__.download_file(url='http://www.cvssp.org/FingerSpellingKinect2011/dataset9-depth.tar.gz',
                            filepath=tarfile_path)

    extracted_path = os.path.join(images_folderpath, 'aslB')
    __utils__.extract_tar(tarfile_path,extracted_path)

    
folderpath = os.path.join(os.getenv('HOME'),'Descargas')
images_folderpath = os.path.join(folderpath, 'Datasets')
download_and_extract(folderpath,images_folderpath)