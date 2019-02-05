import tarfile
import __utils__
import os


def download_and_extract(folderpath, images_folderpath, download):

    # if the file is dowloaded
    #   extract the file in the path into images_folderpath
    if download is not True:
        tarfile_path = folderpath  # must be the filepath
    else:
        # if the folder doenst exist is created
        __utils__.check_folder_existence(folderpath)
        __utils__.check_folder_existence(images_folderpath)

        tarfile_path = os.path.join(folderpath, 'aslA.tar.gz')
        __utils__.download_file(url='http://www.cvssp.org/FingerSpellingKinect2011/fingerspelling5.tar.bz2',
                                filepath=tarfile_path)

    extracted_path = os.path.join(images_folderpath, 'aslA')
    __utils__.extract_tar(tarfile_path, extracted_path)
