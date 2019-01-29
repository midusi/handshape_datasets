import numpy as np
import os
from keras.utils.data_utils import get_file
from os.path import expanduser

from skimage import io
from skimage import color
from skimage import transform

import tarfile



def load_subject(subject_path,image_size,skip):
    
    folders= sorted(os.listdir(subject_path))
    # definir variables vacías, luego crecen
    data= np.zeros((0,image_size[0],image_size[1], 3),dtype='uint8')
    labels= np.array(())
    
    # cargar cada folder con sus labels
    for (i, folderName) in enumerate(folders):
        label_i= ord(folderName) - 97  # convierte el caracter en un índice de A=0 en adelante
        files= sorted(os.listdir(os.path.join(subject_path,folderName)))
        files = [f for f in files if f.startswith("color")]
        files=files[::skip]
        # por cada archivo dentro del folder
        folder_data=np.zeros((len(files), image_size[0], image_size[1], 3),dtype='uint8')
        for (j, filename) in enumerate(files):
            image_filepath=os.path.join(subject_path, folderName,filename)
            image=io.imread(image_filepath)
            image = transform.resize(image, (image_size[0], image_size[1]), preserve_range=True)
            # actualizar matriz de datos y de labels
            labels= np.append(labels, label_i)
            folder_data[j,:,:,:]=image
        data= np.vstack((data, folder_data))
    return data, labels               

from multiprocessing import Pool

def list_diff(a,b):
    s = set(b)
    return [x for x in a if x not in s]

def load_images(folder_path,image_size,skip,test_subjects):
    # se considera datos para training los sujetos A, B, C, D
    # y datos para testing al sujeto E

    # cargar sujetos train y test
    train_subjects=list_diff(["A","B","C","D","E"],test_subjects)
    # p = Pool(len(subjects))

    def f(subject): return load_subject(os.path.join(folder_path,subject),image_size,skip)

    train_subject_data=map(f, train_subjects)
    x_train,y_train=zip(*train_subject_data)

    x_train = np.vstack(x_train)
    y_train = np.hstack(y_train)

    test_subject_data = map(f, test_subjects)
    x_test, y_test = zip(*test_subject_data)
    x_test = np.vstack(x_test)
    y_test = np.hstack(y_test)

    return x_train, x_test, y_train, y_test


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

