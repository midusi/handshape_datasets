import numpy as np
import os
from os.path import expanduser

import tarfile


def download_and_extract(folderpath):
    if not os.path.exists(folderpath):
        print("Creating folder %s..." % folderpath)
        os.mkdir(folderpath)

    filename = "fingerspelling5.tar.bz2"
    zip_filepath = os.path.join(folderpath, filename)

    if not os.path.exists(zip_filepath):
        print("Downloading Pugeault's Fingerspelling dataset to folder %s ..." % zip_filepath)
        origin = "http://www.cvssp.org/FingerSpellingKinect2011/fingerspelling5.tar.bz2"
        get_file(zip_filepath, origin=origin)

    if len(os.listdir(folderpath))==1:
        print("Extracting images to %s..." % folderpath)
        with tarfile.open(zip_filepath, "r:bz2") as tar_ref:
            tar_ref.extractall(folderpath)


def load_data(image_size=(32,32),skip=1,test_subjects=["E"],folderpath=os.path.join(expanduser("~"),".keras",
                                                                                     "datasets","pugeault")):
    # get folder where the dataset is / will be downloaded
    # folderpath = os.path.join(tempfile.gettempdir(), "pugeault")
    test_subjects_string="".join(test_subjects)
    np_filename="pugeault_skip%d_testsubjects%s_color.npz" %(skip,test_subjects_string)
    np_filepath=os.path.join(folderpath,np_filename)
    if not os.path.exists(np_filepath):
        print("Downloading/extracting/recoding dataset...")
        # download dataset (if necessary)
        download_and_extract(folderpath)
        folderpath = os.path.join(folderpath, "dataset5")
        print("Loading images from %s..." % folderpath)
        x_train, x_test, y_train, y_test = load_images(folderpath, image_size, skip, test_subjects)
        print("Done.")
        print("Saving binary version of dataset to %s" % np_filepath)
        np.savez(np_filepath, x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test)
        print("Done.")
    else:
        print("Found binary version in %s, loading..." % np_filepath)
        data=np.load(np_filepath)
        x_train, x_test, y_train, y_test=(data["x_train"],data["x_test"],data["y_train"],data["y_test"])
    img_channels, img_rows, img_cols =3, 32, 32
    return x_train, x_test, y_train, y_test, img_channels, img_rows, img_cols

