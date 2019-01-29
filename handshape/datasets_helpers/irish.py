import numpy as np
import os

import zipfile
import requests
import shutil

def download_file(url,filepath):
    with requests.get(url, stream=True) as r:
        with open(filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

from os.path import expanduser

from skimage import io
from skimage import color
from skimage import transform

import tarfile

filenames=["Person%d.zip" % i for i in range(1,7)]

url = "https://github.com/marlondcu/ISL/blob/master/Frames/"

image_size=64,64
import string
labels=list(string.ascii_lowercase)
import skimage

def crop_to_hand(image,pad=10):
    h,w=image.shape
    # r, c = np.where(image > 0)
    # min_r, max_r = r.min(), r.max()
    # min_c, max_c = c.min(), c.max()

    binary_image = skimage.morphology.opening(image > 50)

    label = skimage.measure.label(binary_image)

    biggest_region = None

    for region in skimage.measure.regionprops(label):
        if biggest_region is None:
            biggest_region = region
        else:
            if region.area > biggest_region.area:
                biggest_region = region

    min_r, min_c, max_r, max_c = biggest_region.bbox

    min_c = max(0, min_c - pad)
    min_r = max(0, min_r - pad)
    max_c = min(w, max_c + pad)
    max_r = min(h, max_r + pad)
    image=image[min_r:max_r+1,min_c:max_c+1]
    return image


def pad_to_aspect_ratio(image,target_image_size,color=np.array([0])):
    h,w=image.shape
    ht,wt=target_image_size
    image_aspect_ratio=h/w
    t_image_aspect_ratio=ht/wt

    # print(h,w,ht,wt,image_aspect_ratio,t_image_aspect_ratio)
    color = color.astype(image.dtype)
    if image_aspect_ratio>t_image_aspect_ratio:
        deltaW = h / t_image_aspect_ratio  - w
        extra=int(round(deltaW//2))
        new_image=(h,w+extra*2)
        padded_image = np.ones(new_image, dtype=image.dtype)
        padded_image *= color
        padded_image[:,extra:extra+w]=image
    elif t_image_aspect_ratio>image_aspect_ratio:
        deltaH = w * t_image_aspect_ratio - h
        extra = int(round(deltaH // 2))
        new_size=(h + extra * 2, w)
        padded_image = np.ones(new_size, dtype=image.dtype)
        padded_image*=color
        padded_image[extra:extra + h, :] = image
    else:
        padded_image=image

    return padded_image

def preprocess_image(image,pad,image_size):
    image = crop_to_hand(image,pad=pad)
    image = pad_to_aspect_ratio(image, image_size)
    original_type=image.dtype
    image = transform.resize(image, (image_size[0], image_size[1]), preserve_range=True)
    image=image.astype(original_type)
    return image

def load_images(images_folderpath):
    
    files=os.listdir(images_folderpath)
    n=len(files)
    print("Loading ",n," images..")
    assert(n==58114,"Wrong number of images, please delete files and repeat the download and extraction process.")
    x= np.zeros((n,image_size[0],image_size[1],1),dtype='uint8')
    y= np.zeros(n)
    subject=np.zeros(n)


    # cargar cada folder con sus labels
    for (i, filename) in enumerate(files):
        klass=filename[8]
        class_index=ord(klass)-ord("A")
        image_filepath=os.path.join(images_folderpath, filename)
        image=io.imread(image_filepath)
        image=preprocess_image(image,10,image_size)
        y[i]=class_index
        x[i,:,:,0]=image
        subject[i] = int(filename[6])
        if i % (n//10)==0:
            print(i/n*100,"%")
    return x, y, subject

from multiprocessing import Pool

def list_diff(a,b):
    s = set(b)
    return [x for x in a if x not in s]


def download_and_extract(folderpath,images_folderpath):
    if not os.path.exists(folderpath):
        print("Creating folder %s..." % folderpath)
        os.mkdir(folderpath)
        print("Creating folder %s..." % images_folderpath)
        os.mkdir(images_folderpath)

    print("Downloading Irish Sign Language dataset to folder %s ..." % folderpath)
    for filename in filenames:
        zip_filepath = os.path.join(folderpath, filename)

        if not os.path.exists(zip_filepath):
            origin = url +filename+"?raw=true"
            print("Downloading: %s ..." % origin)
            download_file(origin,zip_filepath)

            with zipfile.ZipFile(zip_filepath, "r") as zip_ref:
                print("Extracting images to %s..." % images_folderpath)
                zip_ref.extractall(images_folderpath)

#
def split_data(x,y,subject,test_subjects):
    if test_subjects=="subject_dependent":
        x_test=x[::2,:,:,:]
        x_train = x[1::2, :, :, :]
        y_test=y[::2]
        y_train= y[1::2]
        subject_test=subject[::2]
        subject_train = subject[1::2]
    else:
        test_subjects=np.array(test_subjects)
        test_indices=np.isin(subject,test_subjects)
        train_indices=np.logical_not(test_indices)
        x_train=x[train_indices,:,:,:]
        x_test=x[test_indices,:,:,:]
        y_train=y[train_indices]
        y_test=y[test_indices]
        subject_train=subject[train_indices]
        subject_test=subject[test_indices]

    return x_train, x_test, y_train, y_test, subject_train,subject_test

# test_subjects can be either:
# the string "subject_dependent": for a subject dependent split where
# images are sequentially numbered, and then those with an even index are assigned to
# the test set and the rest to the train set.
# A list of numbers from 1 to 6: for a subject independent experiment where
# the list contains the subjects whose images form the test set.
def load_data(test_subjects=[6],folderpath=os.path.join(expanduser("~"),".keras",
                                                                                     "datasets","irish")):

    images_folderpath = os.path.join(folderpath, "images")
    np_filename="irish.npz"
    np_filepath = os.path.join(folderpath, np_filename)
    if not os.path.exists(np_filepath):
        print("Could not find ",np_filename,". Downloading/extracting/reencoding dataset...")
        # download dataset (if necessary)
        #download_and_extract(folderpath,images_folderpath)
        print("Loading images from %s..." % images_folderpath)
        x,y,subject = load_images(images_folderpath)
        print("Done.")
        print("Saving binary version of dataset to %s" % np_filepath)
        np.savez(np_filepath, x=x, y=y,subject=subject)
        print("Done.")
    else:
        print("Found binary version in %s, loading..." % np_filepath)
        data=np.load(np_filepath)
        x,y,subject = data["x"],data["y"],data["subject"]

    x_train, x_test, y_train, y_test,subject_train,subject_test=split_data(x,y,subject,test_subjects)
    img_channels, img_rows, img_cols =3, 32, 32
    return x_train, x_test, y_train, y_test, img_channels, img_rows, img_cols

