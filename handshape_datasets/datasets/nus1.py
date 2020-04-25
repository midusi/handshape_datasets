from .utils import mkdir_unless_exists, extract_zip, download_file
from .dataset import Dataset
from handshape_datasets.dataset_loader import DatasetLoader
from skimage import io
from .common import *

import os

labels=["B","Miton","Mano Plana","Pinza Pico","Indice","Duo","Puño","Pulgar-Mayor","Pico","Angulo"]

class Nus1Info(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n Nus 1
        \n The NUS hand posture dataset I consists 10 classes of postures, 24 sample images per class
        \nMore details can be found at https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/
        \n Select Version bw or color.
        \n"""
        url_info = "https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet//"
        download_size = 2929790
        disk_size = 3810809
        subject_color = 239
        subject_bw=240
        subject= subject_color+subject_bw
        super().__init__("Nus1",(160,120,3),{"y":"classes"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return Nus1()

class Nus1(DatasetLoader):
    def __init__(self, image_size=(120,160)):
        #self.__doc__ += super.__doc__
        super().__init__("nus_1")
        self.url = 'https://www.ece.nus.edu.sg/stfpage/elepv/NUS-HandSet/NUS-Hand-Posture-Dataset-I.zip'
        self._FILENAME = self.name + '.zip'
        self.image_size=image_size

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(url=self.urls(), filepath=ZIP_PATH)
            # set the exit flag
            self.set_downloaded(folderpath)

    def load(self, folderpath,**kwargs):
        images_folderpath = self.images_folderpath(folderpath)
        subsets_folder = os.path.join(images_folderpath,
                                      'NUS Hand Posture Dataset')
        y_color = np.array(())
        y_bw = np.array(())
        if os.path.exists(subsets_folder):
            os.chdir(subsets_folder)
            folders = {}
            folders_names = list(
                # just the folders
                filter(lambda x: ".txt" not in x, os.listdir(os.getcwd())))
            # start the load
            images_loaded_counter = 0
            # each image is stored in the key corresponding to its subset
            for (j,folder) in enumerate(folders_names):
                logging.debug(f"Loading images from {folder}")
                folders[folder] = []
                # cd subset folder
                os.chdir(subsets_folder+'/{}'.format(folder))
                images = list(
                    filter(
                        lambda x: ".db" not in x, os.listdir(os.getcwd())))
                images_loaded_counter += len(images)
                if(folder=='Color'):
                    x_color = np.zeros((len(images), self.image_size[0], self.image_size[1], 3), dtype='uint8')
                    #fix a bw image in the color folder
                    for (i, image) in enumerate(images):
                        im=io.imread(image)
                        if (im.shape==(120,160)):
                            fix=os.path.join(subsets_folder,folder)
                            fix2=os.path.join(fix,image)
                            os.remove(fix2) #remove g7(14)
                            images = list(
                                filter(
                                    lambda x: ".db" not in x, os.listdir(os.getcwd())))
                else:
                    x_bw = np.zeros((len(images), self.image_size[0], self.image_size[1]), dtype='uint8')
                for (i,image) in enumerate(images):
                    if(image[2]=='0'):
                        label=9
                    else:
                        label= ord(image[1]) - 49
                    if(folder=='Color'):
                        im = io.imread(image)
                        x_color[i, :, :, :] = im
                        y_color = np.append(y_color, label)
                    else:
                        im = io.imread(image, as_gray=(folder == 'Color'))
                        x_bw[i,:,:]=im
                        y_bw=np.append(y_bw,label)
                os.chdir("..")
            logging.debug(
                f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")
            if 'version' in kwargs:
                if (kwargs['version'] != 'Color'):
                    metadata = {"y": y_bw}
                    return x_bw, metadata
                else:
                    metadata = {"y": y_color}
                    return x_color, metadata
            else:
                metadata = {"y": y_color}
                return x_color, metadata

    def preprocess(self, folderpath):

        images_folderpath = self.images_folderpath(folderpath)
        mkdir_unless_exists(images_folderpath)
        ZIP_PATH = os.path.join(folderpath, self._FILENAME)
        # extract the zip into the images path
        extract_zip(ZIP_PATH, images_folderpath)
        os.remove(ZIP_PATH)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = self.images_folderpath(fpath)
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