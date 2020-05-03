from handshape_datasets.dataset_loader import DatasetLoader
from .utils import mkdir_unless_exists, extract_tar, download_bigger_file
import logging
from .common import *
import os
import numpy as np

import cv2

from skimage import io
from skimage import transform

labels_A=["A","B","C","D","E","F","G","H","I","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y"]
labels_B=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y", "Z"]

class PugeaultASL_AInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n ASL A
        The first dataset comprises 24 static signs (excluding letters j and z because they involve motion).
        This was captured in 5 different sessions, with similar lighting and background
        More details can be found at http://empslocal.ex.ac.uk/people/staff/np331/index.php?section=FingerSpellingDataset
        """
        url_info = "http://empslocal.ex.ac.uk/people/staff/np331/index.php?section=FingerSpellingDataset"
        download_size = 2246539027
        disk_size = 4585740339
        subject = 65774
        super().__init__("PugeaultASL_A",(32,32,3),{"y":"classes", "subject":"subject"},description, labels_A, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return PugeaultASL_A()

class PugeaultASL_A(DatasetLoader):
    def __init__(self,image_size=(32,32)):
        super().__init__("PugeaultASL_A")
        assert(len(image_size)==2)
        self.url = 'http://www.cvssp.org/FingerSpellingKinect2011/fingerspelling5.tar.bz2'
        self.subjects=["A","B","C","D","E"]
        self.image_size=image_size
        self.npz_filename=f"pugeault_color_{image_size[0]}x{image_size[1]}.npz"
        self.tarfile_name = 'fingerspelling5.tar.bz2'

    def urls(self):
        return self.url

    def download_dataset(self, folderpath, images_folderpath=None):
            download_bigger_file(self.urls(), os.path.join(folderpath,self.tarfile_name))
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, folderpath, **kwargs):
        npz_filepath = os.path.join(folderpath, self.npz_filename) #get the npz file with the data
        data = np.load(npz_filepath)
        x,y,subject = (data["x"], data["y"],data["subject"])
        metadata={"y":y,"subjects":subject}
        return x,metadata


    def load_subject(self,subject_folderpath, subject_id,image_size):

        folders = sorted(os.listdir(subject_folderpath))
        data = np.zeros((0, image_size[0], image_size[1], 3), dtype='uint8')
        labels = np.array((),dtype='uint8')
        for (i, folderName) in enumerate(folders):
            label_i = ord(folderName) - 97  #Transform the character into a index (A=0)
            if(label_i > 9): #the class "j" doesnt exist
                label_i=label_i-1
            files = sorted(os.listdir(os.path.join(subject_folderpath, folderName)))
            files = [f for f in files if f.startswith("color")]
            # for each file in the folder
            folder_data = np.zeros((len(files), image_size[0], image_size[1], 3), dtype='uint8')
            for (j, filename) in enumerate(files):
                image_filepath = os.path.join(subject_folderpath, folderName, filename)
                image = io.imread(image_filepath)
                image = transform.resize(image, (image_size[0], image_size[1]), preserve_range=True,mode="reflect",anti_aliasing=True)
                # Update the matrix (data and labels)
                labels = np.append(labels, label_i)
                folder_data[j, :, :, :] = image
            data = np.vstack((data, folder_data))
        subject=np.zeros(len(labels))+subject_id
        logging.debug(data.shape,labels.shape,subject.shape)
        return data, labels,subject

    def load_images(self,images_folderpath):
        n=len(self.subjects)

        def f(i_subject):
            subject_id,subject=i_subject
            logging.info(f"({subject_id}/{n}) Loading images for subject {subject}")
            return self.load_subject(os.path.join(images_folderpath, subject), subject_id, self.image_size)
        # get x,y,subject arrays for each subject

        ytot=np.array((),dtype='uint8')
        subjecttot = np.array(())
        xtot=np.zeros((0, self.image_size[0], self.image_size[1], 3), dtype='uint8')
        for i in range(0,n):
            subject_id=i
            subject= self.subjects[i]
            logging.info(f"({subject_id+1}/{n}) Loading images for subject {subject}")
            x,y,subject= self.load_subject(os.path.join(images_folderpath, subject), subject_id, self.image_size)
            ytot=np.append(ytot, y)
            subjecttot=np.append(subjecttot, subject)
            xtot=np.vstack((xtot, x))
        return xtot,ytot,subjecttot

    def preprocess(self, folderpath):
        # extract the zip
        tarfile_path = os.path.join(folderpath, self.tarfile_name)
        extract_tar(tarfile_path, folderpath)
        #load images
        images_folderpath = os.path.join(folderpath, "dataset5")
        x,y,subject=self.load_images(images_folderpath)
        # save to binary
        npz_filepath=os.path.join(folderpath,self.npz_filename)
        np.savez(npz_filepath, x=x,y=y,subject=subject)
        #remove the .tar file
        os.remove(tarfile_path)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder=os.path.join(fpath, "dataset5")
        npz_exist = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(npz_exist) == 0):
            return False
        else:
            if (os.path.exists(folder)):
                rmtree(folder)
            else:
                return False
            return True

class PugeaultASL_BInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \nASL B
        The second dataset (depth only) is captured from 9 different persons in two very different environments and lighting. 
        More details can be found at http://empslocal.ex.ac.uk/people/staff/np331/index.php?section=FingerSpellingDataset
        """
        url_info = "http://empslocal.ex.ac.uk/people/staff/np331/index.php?section=FingerSpellingDataset"
        download_size = 332789476
        disk_size = 752803969
        subject = 72676
        super().__init__("PugeaultASL_B",(32,32,1),{"y":"classes", "subject":"subject"},description, labels_B, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return PugeaultASL_B()

class PugeaultASL_B(DatasetLoader):
    def __init__(self,image_size=(32,32)):
        super().__init__("PugeaultASL_B")
        self.url = 'http://www.cvssp.org/FingerSpellingKinect2011/dataset9-depth.tar.gz'
        self.npz_filename = f"pugeault_depth_{image_size[0]}x{image_size[1]}.npz"
        self.image_size=image_size
        self.tarfile_name="aslB.tar.gz"
        self.subjects=["A","B","C","D","E","F","G","H","I"]

    def urls(self):
        return self.url

    def download_dataset(self, folderpath, images_folderpath=None):
        TARFILE_PATH = os.path.join(folderpath, 'aslB.tar.gz')
        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_bigger_file(self.urls(), TARFILE_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, folderpath, **kwargs):
        npz_filepath = os.path.join(folderpath, self.npz_filename)
        data = np.load(npz_filepath)
        x,y,subject = (data["x"], data["y"],data["subject"])
        metadata={"y":y,"subjects":subject}
        return x,metadata


    def load_subject(self,subject_folderpath, subject_id,image_size):

        folders = sorted(os.listdir(subject_folderpath))
        data = np.zeros((0, image_size[0], image_size[1],1), dtype='uint16')
        labels = np.array((),dtype='uint8')

        for (i, folderName) in enumerate(folders):
            label_i = ord(folderName) - 97
            files = sorted(os.listdir(os.path.join(subject_folderpath, folderName)))
            files = [f for f in files if f.startswith("depth")]
            folder_data = np.zeros((len(files), image_size[0], image_size[1],1), dtype='uint16') #uint16 cause of depth image
            for (j, filename) in enumerate(files):
                image_filepath = os.path.join(subject_folderpath, folderName, filename)
                image = cv2.imread(image_filepath, flags=cv2.IMREAD_UNCHANGED)
                image = transform.resize(image, (image_size[0], image_size[1]), preserve_range=True,mode="reflect",anti_aliasing=True)
                image=image[:,:,np.newaxis]
                labels = np.append(labels, int(label_i))
                folder_data[j, :]= image
            data = np.vstack((data, folder_data))
        subject=np.zeros(len(labels))+subject_id
        logging.debug(data.shape,labels.shape,subject.shape)
        return data, labels,subject

    def load_images(self,images_folderpath):
        n=len(self.subjects)

        def f(i_subject):
            subject_id,subject=i_subject
            logging.info(f"({subject_id}/{n}) Loading images for subject {subject}")
            return self.load_subject(os.path.join(images_folderpath, subject), subject_id, self.image_size)

        ytot=np.array((),dtype='uint8')
        subjecttot = np.array(())
        xtot=np.zeros((0, self.image_size[0], self.image_size[1],1), dtype='uint16')
        for i in range(0,n):
            subject_id=i
            subject= self.subjects[i]
            logging.info(f"({subject_id+1}/{n}) Loading images for subject {subject}")
            x,y,subject= self.load_subject(os.path.join(images_folderpath, subject), subject_id, self.image_size)
            ytot=np.append(ytot, y)
            subjecttot=np.append(subjecttot, subject)
            xtot=np.vstack((xtot, x))
        return xtot,ytot,subjecttot

    def preprocess(self, folderpath):
        # extract the zip
        tarfile_path = os.path.join(folderpath, self.tarfile_name)
        extract_tar(tarfile_path, folderpath)
        #load images
        images_folderpath = os.path.join(folderpath, "ds9")
        x,y,subject=self.load_images(images_folderpath)
        # save to binary
        npz_filepath=os.path.join(folderpath,self.npz_filename)
        np.savez(npz_filepath, x=x,y=y,subject=subject)
        #remove the .tar file
        os.remove(tarfile_path)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = os.path.join(fpath, "ds9")
        npz_exist = list(
            filter(lambda x: '.npz' in x,
                    listdir(fpath)))
        if (len(npz_exist) == 0):
            return False
        else:
            if (os.path.exists(folder)):
                rmtree(folder)
            else:
                return False
            return True