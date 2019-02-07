from . import __utils__
import tarfile
import os


def download_and_extract(folderpath, images_folderpath, download):

    # if the folder doenst exist is created
    __utils__.check_folder_existence(folderpath)
    __utils__.check_folder_existence(images_folderpath)

    tarfile_path = os.path.join(folderpath, 'rwth-phoenix.tar.gz')
    __utils__.download_file_over_ftp(
        ftp_url='wasserstoff.informatik.rwth-aachen.de',
        ftp_relative_file_path='pub/rwth-phoenix/2016',
        ftp_filename='ph2014-dev-set-handshape-annotations.tar.gz',
        filepath=tarfile_path)

    extracted_path = os.path.join(images_folderpath, 'rwth-phoenix')
    __utils__.extract_tar(tarfile_path, extracted_path)


download_and_extract(
    os.path.join(os.getenv('HOME'), 'Descargas'),
    os.path.join(os.getenv('HOME'), 'Descargas', 'Datasets'),
    True
)
