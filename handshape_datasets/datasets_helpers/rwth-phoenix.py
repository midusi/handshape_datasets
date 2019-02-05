import __utils__
import tarfile
import os


def download_and_extract(folderpath, images_folderpath,download):

    # if the folder doenst exist is created
    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)

    tarfile_path = os.path.join(folderpath, 'rwth-phoenix.tar.gz')
    __utils__.download_file(url='ftp://wasserstoff.informatik.rwth-aachen.de/pub/rwth-phoenix/2016/ph2014-dev-set-handshape-annotations.tar.gz',
                            filepath=tarfile_path)

    extracted_path = os.path.join(images_folderpath, 'rwth-phoenix')
    __utils__.extract_tar(tarfile_path, extracted_path)
