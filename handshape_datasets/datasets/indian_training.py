from .common import *
import os
from os import listdir, path
from .utils import mkdir_unless_exists
from . import utils
from skimage import transform
from sys import stdin
import numpy as np1

#Each depth image is a matrix of size 640x480 having values in the range [0,2047]
#https://github.com/zafar142007/Gesture-Recognition-for-Indian-Sign-Language-using-Kinect/zipball/master
#url info http://zafar142007.github.io/Gesture-Recognition-for-Indian-Sign-Language-using-Kinect/

labels=["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "A", "Add", "Appreciation", "A-SingleHanded", "Assistance", "B", "Bell", "Between", "Bhangada", "Bite", "Blow", "Bottle", "Bowl", "Boxing", "B-SingleHanded", "Bud", "C", "Conservation", "Control", "C-SingleHanded", "D", "Density", "Deposit", "D-SingleHanded", "E", "Elbow", "E-SingleHanded", "F", "Few", "Fine", "Friend", "F-SingleHanded", "G", "Ghost", "Good", "Gram", "G-SingleHanded", "Gun", "H", "Handcuff", "Help", "Here", "Hold", "How", "H-SingleHanded", "I", "Intermediate", "Iron", "I-SingleHanded", "It", "K", "Keep", "K-SingleHanded", "L", "Leaf", "Learn", "Leprosy", "Little", "Lose", "L-SingleHanded", "M", "Mail", "Me", "Measure", "Mirror", "M-SingleHanded", "N", "Negative", "N-SingleHanded", "O", "Obedience", "Okay","Opposite","Opposition","O-SingleHanded", "P", "Participation", "Paw", "Perfect", "Potentiality", "Pray", "Promise", "P-SingleHanded", "Q","Q-SingleHanded","Quantity","Questions", "R", "Respect", "Rigid","R-SingleHanded", "S", "Sample", "Season", "Secondary", "Size", "Skin", "Small", "Snake", "Some", "Specific", "S-SingleHanded", "Stand", "Strong", "Study", "Sugar", "T", "There", "Thick", "Thursday","T-SingleHanded", "U", "Unit", "Up", "U-SingleHanded", "V", "Vacation", "Varanasi","V-SingleHanded", "W", "Warn", "Weight","Work", "W-SingleHanded", "X", "X-SingleHanded", "Y", "You", "Y-SingleHanded", "Z"]
ids_txt=["0B6iDOaIw70ScYndDbGVrZWdIeVE", "0B6iDOaIw70ScLUZPcEMxXzdGb1k","1o7xtLyItrRlQctrCFmM1ZPx_IHXuk29x"]
name_txt=["credits.txt", "license.txt","README.txt"]
ids_rgb=["0B6iDOaIw70ScbndjX1NrMUFhczA","0B6iDOaIw70ScYkhLRW5JWlhCY1U", "0B6iDOaIw70ScZHo2OG5VWmd6eDQ", "0B6iDOaIw70ScR1pYT29DSUIzVlU", "0B6iDOaIw70ScYzVZU25HcWl0bEk", "0B6iDOaIw70ScVzVnZV9HWE42WjQ", "0B6iDOaIw70ScMm84Tzc4Nkhvcm8","0B6iDOaIw70ScaFpWREJKSFBrQXM", "0B6iDOaIw70ScSlpsVEhxcVdRbVk", "0B6iDOaIw70ScQnpZYUNWSU9tcWM", "0B6iDOaIw70ScTkRCT0k1NlFMdkk", "0B6iDOaIw70ScS3FncUFHZ0FYZXc", "0B6iDOaIw70ScX2JZc05XZ3l6YW8", "0B6iDOaIw70ScRWk3cThFdl9wUHc","0B6iDOaIw70ScRmZnZjhGNmhRalU", "0B6iDOaIw70ScUEJRWWJQYi01RVE", "0B6iDOaIw70ScT2ZRMFFzaC05ZGM", "0B6iDOaIw70ScUEM0ZnlJSWlkbDg"]
ids_depth=["0B6iDOaIw70ScbnYtcnpJdGR5Vmc", "0B6iDOaIw70ScLWJDR2p4VGJUR0U","0B6iDOaIw70ScbmxkaEk0Mk0tYmM", "0B6iDOaIw70ScYll3YnQ3X3VsSEU", "0B6iDOaIw70ScaXpYNjJxazJPN1k","0B6iDOaIw70ScWm5nQmM0VGNXQmc","0B6iDOaIw70SceEJuaXBQa0tMZUE", "0B6iDOaIw70ScT2xZTVcydk9RbE0", "0B6iDOaIw70ScTUJyN2s3RHhzNkk", "0B6iDOaIw70ScSDkzZGR5aVBJZlU","0B6iDOaIw70ScRlgzMF9fd2N3ZDQ", "0B6iDOaIw70ScZ19Xby1PM1lXeUk","0B6iDOaIw70ScVmQwQ0RHT09fMFE","0B6iDOaIw70ScX0ltODc1OFpUbHc","0B6iDOaIw70ScNkdkV1RjZkltaDg","0B6iDOaIw70ScWFdFellEcklBQlk","0B6iDOaIw70ScTEFCNHFyd0lNNWc","0B6iDOaIw70ScWGRHMTFqa3JpaFk"]

class Indian_AInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n Indian Sign Language
        Gesture recognition for Indian sign language using Kinect
        More details can be found at http://zafar142007.github.io/Gesture-Recognition-for-Indian-Sign-Language-using-Kinect/
        """
        url_info = "http://zafar142007.github.io/Gesture-Recognition-for-Indian-Sign-Language-using-Kinect/"
        download_size = 1780897140
        disk_size = 2020009029
        subject = 5040
        super().__init__("indianA",(640,480,3),{"y":"classes", "subject":"subject"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return IndianA()

class IndianA(DatasetLoader):
    def __init__(self,image_size=(32,32)):
        super().__init__("indianA")
        assert(len(image_size)==2)
        self.url = 'https://drive.google.com/uc?export=download&id='
        self.image_size=image_size
        self.npz_filename=f"indian_color_{image_size[0]}x{image_size[1]}.npz"
        self.folder_name="zafar142007"

    def urls(self):
        return self.url

    def download_dataset(self, folderpath, images_folderpath=None):
        mkdir_unless_exists(os.path.join(folderpath,self.folder_name))
        folder_n=os.path.join(folderpath,self.folder_name)
        for i in range(len(ids_txt)):
            download_from_drive(f"{self.urls()}{ids_txt[i]}", folder_n+"\\"+name_txt[i])
            # set the exit flag
        for j in range(len(ids_rgb)):
            if(j==0):
                    download_from_drive(f"{self.urls()}{ids_rgb[j]}", os.path.join(folder_n,f"user{j + 1}rgbreshoot.tar.gz"))
            else:
                    download_from_drive(f"{self.urls()}{ids_rgb[j]}", os.path.join(folder_n,f"user{j+1}rgb.tar.gz"))
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
        if (subject_id > 9):# for control de filename labels
            text_control = 8
        else:
            text_control = 7
        for (i, folderName) in enumerate(folders):
            files = sorted(os.listdir(os.path.join(subject_folderpath, folderName)))
            folder_data = np.zeros((len(files), image_size[0], image_size[1], 3), dtype='uint8')
            for (j, filename) in enumerate(files):
                image_filepath = os.path.join(subject_folderpath, folderName, filename)
                image = io.imread(image_filepath)
                image = transform.resize(image, (image_size[0], image_size[1]), preserve_range=True,mode="reflect",anti_aliasing=True)
                # Update the matrix (data and labels)
                if (filename[text_control+1] == "-"):
                    labels_i = ord(filename[text_control]) - 48-1
                else:
                    if (filename[text_control+2] == "-"):
                        labels_i = (ord(filename[text_control]) - 48) * 10 + ord(filename[text_control+1]) - 48-1
                    else:
                        labels_i = (ord(filename[text_control]) - 48) * 100 + (ord(filename[text_control+1]) - 48) * 10 + ord(filename[text_control + 2]) - 48-1
                labels = np.append(labels, labels_i)
                folder_data[j, :, :, :] = image
            data = np.vstack((data, folder_data))
        subject=np.zeros(len(labels))+subject_id
        logging.debug(data.shape,labels.shape,subject.shape)
        return data, labels,subject

    def load_images(self,images_folderpath):
        n=18
        ytot=np.array((),dtype='uint8')
        subjecttot = np.array(())
        xtot = np.zeros((0, self.image_size[0], self.image_size[1], 3), dtype='uint8')

        for i in range(0,n):
            subject_id=i+1
            logging.info(f"({subject_id}/{n}) Loading images for subject {subject_id}")
            if (i == 0):
                path_rgb=os.path.join(images_folderpath,f"user{i + 1}rgbreshoot")
            else:
                path_rgb = os.path.join(images_folderpath,f"user{i + 1}rgb")
            x, y, subject = self.load_subject(path_rgb, subject_id, self.image_size)
            ytot=np.append(ytot, y)
            subjecttot=np.append(subjecttot, subject)
            xtot=np.vstack((xtot, x))
        return xtot,ytot,subjecttot

    def preprocess(self, folderpath):

        preprocess_flag = "{}_preprocessed".format(self.name)
        folderpath_act=Path(str(folderpath)+"\\"+self.folder_name)
        folderpath_act2 = os.path.join(folderpath, self.folder_name)

        if self.get_status_flag(folderpath_act, preprocess_flag) is False:
            datasets = list(
                filter(lambda x: x[-7:] == '.tar.gz', #comprobar el -4
                       listdir(folderpath_act2)))  # i just want the .tar files
            for dataset_file in datasets:
                dataset_folder_name = dataset_file[:-7]  # until the .tar(excluded) #comprobar el -4
                dataset_images_path = path.join(folderpath_act2, dataset_folder_name)
                mkdir_unless_exists(dataset_images_path)
                filepath = os.path.join(folderpath_act2,dataset_file)
                extract_tar(filepath,
                            extracted_path=dataset_images_path)  # dataset_file has the format 'Person$.zip'
                # remove the zips files
                os.remove((filepath))

        #load images
        images_folderpath = folderpath_act2
        x,y,subject=self.load_images(images_folderpath)
        # save to binary
        npz_filepath=os.path.join(folderpath,self.npz_filename)
        np.savez(npz_filepath, x=x,y=y,subject=subject)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self,path):
        fpath = path / self.name
        folder=os.path.join(fpath,self.folder_name)
        npz_exist = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(npz_exist)==0):
            return False
        else:
            if (os.path.exists(folder)):
                rmtree(folder)
            else:
                return False
            return True

class Indian_BInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n Indian Sign Language- depth images
        Gesture recognition for Indian sign language using Kinect B
        More details can be found at http://zafar142007.github.io/Gesture-Recognition-for-Indian-Sign-Language-using-Kinect/
        """
        url_info = "http://zafar142007.github.io/Gesture-Recognition-for-Indian-Sign-Language-using-Kinect/"
        download_size = 336079729
        disk_size = 9263074067
        subject = 5000
        super().__init__("indianB",(640,480,1),{"y":"classes", "subject":"subject"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return IndianB()

class IndianB(DatasetLoader):
    def __init__(self,image_size=(480,640)):
        super().__init__("indianB")
        assert(len(image_size)==2)
        self.url = 'https://drive.google.com/uc?export=download&id='
        self.image_size=image_size
        self.npz_filename=f"indian_depth_{image_size[0]}x{image_size[1]}.npz"
        self.folder_name="zafar142007B"

    def urls(self):
        return self.url

    def download_dataset(self, folderpath, images_folderpath=None):
        mkdir_unless_exists(os.path.join(folderpath, self.folder_name))
        folder_n = os.path.join(folderpath, self.folder_name)
        for i in range(len(ids_txt)):
            download_from_drive(f"{self.urls()}{ids_txt[i]}", folder_n + "\\" + name_txt[i])
        # set the exit flag
        for j in range(len(ids_depth)):
            if (j == 0):
                download_from_drive(f"{self.urls()}{ids_depth[j]}", os.path.join(folder_n,f"user{j + 1}depthreshoot.tar.gz"))
            else:
                download_from_drive(f"{self.urls()}{ids_depth[j]}", os.path.join(folder_n,f"user{j + 1}depth.tar.gz"))
        self.set_downloaded(folderpath)

    def load(self, folderpath, **kwargs):
        npz_filepath = os.path.join(folderpath, self.npz_filename)  # get the npz file with the data
        data = np.load(npz_filepath)
        x, y, subject = (data["x"], data["y"], data["subject"])
        metadata = {"y": y, "subjects": subject}
        return x, metadata

    def load_subject(self,subject_folderpath, subject_id,image_size):
        folders = sorted(os.listdir(subject_folderpath))
        labels = np.array((),dtype='uint8')
        if (subject_id > 9):# for control de filename labels
            text_control = 8
        else:
            text_control = 7
        for (i, folderName) in enumerate(folders):
            files = sorted(os.listdir(os.path.join(subject_folderpath, folderName)))
            folder_data = np.zeros((len(files), image_size[0], image_size[1],1), dtype='uint16')
            files_path=os.path.join(subject_folderpath, folderName)
            for (j, filename) in enumerate(files):

                file = open(os.path.join(files_path, filename))
                infile = file.readlines()
                for (l, line) in enumerate(infile):
                    dato=line.split(' 'or'\n')
                    for (k,dat) in enumerate(dato):
                        folder_data[j, l, k, 0] = dat
                if (filename[text_control+1] == "-"):
                    labels_i = ord(filename[text_control]) - 48-1
                else:
                    if (filename[text_control+2] == "-"):
                        labels_i = (ord(filename[text_control]) - 48) * 10 + ord(filename[text_control+1]) - 48-1
                    else:
                        labels_i = (ord(filename[text_control]) - 48) * 100 + (ord(filename[text_control+1]) - 48) * 10 + ord(filename[text_control + 2]) - 48-1
                labels = np.append(labels, labels_i)
        subject=np.zeros(len(labels))+ subject_id
        data=folder_data
        logging.debug(data.shape,labels.shape,subject.shape)
        return data, labels,subject

    def load_images(self,images_folderpath):
        n=18
        ytot=np.array((),dtype='uint8')
        subjecttot = np.array(())
        xtot=np.zeros((0, self.image_size[0], self.image_size[1],1), dtype='uint16')
        for i in range(0,n):
            subject_id=i+1
            logging.info(f"({subject_id}/{n}) Loading images for subject {subject_id}")
            if (i == 0):
                path_depth=os.path.join(images_folderpath,f"user{i + 1}depthreshoot")
            else:
                path_depth= os.path.join(images_folderpath, f"user{i + 1}depth")
            x, y, subject = self.load_subject(path_depth, subject_id, self.image_size)
            ytot=np.append(ytot, y)
            subjecttot=np.append(subjecttot, subject)
            xtot=np.vstack((xtot, x))
        return xtot,ytot,subjecttot

    def preprocess(self, folderpath):

        preprocess_flag = "{}_preprocessed".format(self.name)
        folderpath_act=Path(str(folderpath)+"\\"+self.folder_name)
        folderpath_act2 = os.path.join(folderpath,self.folder_name)
        if self.get_status_flag(folderpath_act, preprocess_flag) is False:
            datasets = list(
                filter(lambda x: x[-7:] == '.tar.gz', #comprobar el -4
                       listdir(folderpath_act2)))  # i just want the .tar files
            for dataset_file in datasets:
                dataset_folder_name = dataset_file[:-7]  # until the .tar(excluded) #comprobar el -4
                dataset_images_path = path.join(folderpath_act2, dataset_folder_name)
                mkdir_unless_exists(dataset_images_path)
                filepath = os.path.join(folderpath_act2,dataset_file)
                extract_tar(filepath,
                            extracted_path=dataset_images_path)  # dataset_file has the format 'Person$.zip'
                # remove the zips files
                os.remove((filepath))
        #load images
        images_folderpath = folderpath_act2
        x,y,subject=self.load_images(images_folderpath)
        # save to binary
        npz_filepath=os.path.join(folderpath,self.npz_filename)
        np.savez(npz_filepath, x=x,y=y,subject=subject)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = os.path.join(fpath, self.folder_name)
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