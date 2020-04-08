from numpy import zeros as create_np_array_with_zeros
from logging import warning
from os import path
from os import listdir, mkdir
from skimage import io
from string import ascii_uppercase
from .common import *
import numpy as np
from .dataset import Dataset
from handshape_datasets.dataset_loader import DatasetLoader
from .utils import mkdir_unless_exists, download_file, extract_zip
import logging
import skimage
from skimage import io
from skimage import transform
from skimage import morphology

labels=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
dataset_images = 58114

class IrishInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n Irish Sign Language - Hand shape dataset (ISL-HS)
        \n To build this dataset, short videos were filmed. In total 6 people performed the finger spelling ISL alphabets.
        \n performed the finger spelling ISL alphabets. Each shape was recorded 3 times.
        \nMore details can be found at https://github.com/marlondcu/ISL
        \n"""
        url_info = "https://github.com/marlondcu/ISL"
        download_size = 181773245
        disk_size = 540026681
        subject = 58114
        super().__init__("Irish",(640,480,1),{"y":"classes", "subject":"subject"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return Irish()

class Irish(DatasetLoader):

    def __init__(self):
        super().__init__('irish')
        self.url = "https://github.com/marlondcu/ISL/blob/master/Frames/"
        self.shape = (640, 480)
        self.klasess_ids = {
            klass: (id + 1) for (id, klass) in enumerate(list(ascii_uppercase))  # { A: 1, B: 2 }
        }

    def _get_klass_for_filename(self, klass):
        return self.klasses_ids[klass]  # integer

    def urls(self):
        """
        returns a dictionary with the filenames and their urls
        :rtype: dict
        """
        return {
            f"Person{index}": f"{self.url}/Person{index}.zip?raw=true" for index in range(1, 7)
        }

    def download_dataset(self, zips_path: str):

        mkdir_unless_exists(zips_path)

        urls = self.urls()

        file_exists = self.get_downloaded_flag(zips_path)
        if file_exists is False:
            for filename in urls.keys():  # filename => Person1     f"{filename}.zip" # Person$7
                filepath = str(zips_path) + f"\{filename}.zip"
                download_file(url=urls[filename],
                              filepath=filepath)
            self.set_downloaded(zips_path)



    def preprocess(self, folderpath):
        # FALTA AGREGAR EL PREPROCESADO PARA CADA IMAGEN. HABRÍA QUE SOBRESCRIBIR LAS IMÁGENES??

        preprocess_flag = "{}_preprocessed".format(self.name)

        if self.get_status_flag(folderpath, preprocess_flag) is False:
            datasets = list(
                filter(lambda x: x[-4:] == '.zip',
                       listdir(folderpath)))  # i just want the .zip files
            for dataset_file in datasets:
                dataset_folder_name = dataset_file[:-4]  # until the .zip(excluded)
                dataset_images_path = path.join(folderpath, dataset_folder_name)
                mkdir_unless_exists(dataset_images_path)
                filepath = str(folderpath) + f"\{dataset_file}"
                extract_zip(filepath,
                            extracted_path=dataset_images_path)  # dataset_file has the format 'Person$.zip'

            self.set_preprocessed_flag(folderpath)

    def crop_to_hand(self, image, pad=10):
        h, w = image.shape
        # r, c = np.where(image > 0)
        # min_r, max_r = r.min(), r.max()
        # min_c, max_c = c.min(), c.max()

        binary_image = morphology.opening(image > 50)

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
        image = image[min_r:max_r + 1, min_c:max_c + 1]
        return image

    def preprocess_image(self, image, pad, image_size):
        image = self.crop_to_hand(image, pad=pad)
        image = self.pad_to_aspect_ratio(image, image_size)
        original_type = image.dtype
        image = transform.resize(
            image, (image_size[0], image_size[1]), preserve_range=True, mode="reflect", anti_aliasing=True)
        image = image.astype(original_type)
        return image

    def pad_to_aspect_ratio(self, image, target_image_size, color=np.array([0])):
        h, w = image.shape
        ht, wt = target_image_size
        image_aspect_ratio = h / w
        t_image_aspect_ratio = ht / wt
        #padded_image=1
        # print(h,w,ht,wt,image_aspect_ratio,t_image_aspect_ratio)
        color = color.astype(image.dtype)
        if image_aspect_ratio > t_image_aspect_ratio:
            deltaW = h / t_image_aspect_ratio - w
            extra = int(round(deltaW // 2))
            new_image = (h, w + extra * 2)
            padded_image = np.ones(new_image, dtype=image.dtype)
            padded_image *= color
            padded_image[:, extra:extra + w] = image
        elif t_image_aspect_ratio > image_aspect_ratio:
            deltaH = w * t_image_aspect_ratio - h
            extra = int(round(deltaH // 2))
            new_size = (h + extra * 2, w)
            padded_image = np.ones(new_size, dtype=image.dtype)
            padded_image *= color
            padded_image[extra:extra + h, :] = image
        else:
            padded_image = image

        return padded_image

    def load(self, images_folderpath):
        image_size = (64, 64)

        subsets_folders = list(
            filter(lambda x: '.zip' not in x,
                   listdir(images_folderpath)))  # Files contains all the folders (Person1, Person2, Person3, Person4, Person5, Person6)
        files = list(filter(lambda x: 'irish' not in x,
                    list(subsets_folders)))

        #files = os.listdir(images_folderpath)
        #n=len(files)
        #logging.warning("Loading ", n, " images..")

        h=0
        for (i, filename) in enumerate(files):  #this counts the amount of images
            images = list(
                filter(lambda x: ".db" not in x,
                       listdir(str(images_folderpath) + f"\{filename}"))
            )
            h = len(images) + h

        if h != dataset_images:
            logging.warning(
                f"Wrong number of images, please delete files and repeat the download and extraction process (expected {dataset_images}, got {h}).")

        xtot= np.zeros((h, image_size[0], image_size[1], 1), dtype='uint8')
        ytot=np.zeros(h)
        subjecttot = np.zeros(h)
        j_act=0 #index
        # load the image
        for (i, filename) in enumerate(files): #for folder (Person)
            images = list(
                filter(lambda x: ".db" not in x,
                       listdir(str(images_folderpath) + f"\{filename}"))
            )
            #print(images)
            m = len(images)
            #print(m)
            #x = np.zeros((m, image_size[0], image_size[1], 1), dtype='uint8')
            #y = np.zeros(m)
            #subject = np.zeros(m)
            print("Processing "+filename+"...")
            for(j,im) in enumerate(images): #for images in the specific folder
                klass = im[8]
                class_index = ord(klass) - ord("A")
                image_filepath = str(images_folderpath) + f"\{filename}"+f"\{im}"
                image = io.imread(image_filepath)
                pad=10
                image = self.preprocess_image(image, pad, image_size)
                ytot[j_act] = class_index
                xtot[j_act, :, :, 0] = image
                subjecttot[j_act] = int(filename[6])
                j_act = j_act + 1
                if j % (m // 10) == 0:
                   percent = j / m * 100
                   logging.warning(f'Progress {percent:.2f}%.. ')
        metadata = {"y": ytot, "subjects":subjecttot}
        return xtot, metadata


    def load_image(self, images_folderpath):
        subsets_folders = list(
                filter(lambda x:'.zip' not in x,
                       listdir(images_folderpath)))  # subsets_folders_act contains all the folders (Person1, Person2, Person3, Person4, Person5, Person6)
        subsets_folders_act=list(filter(lambda x:'irish' not in x,
                       list(subsets_folders)))
        #print(subsets_folders_act)
        subsets = {}
        images_loaded_counter = 0
        for person_subset in subsets_folders_act:
            warning(f"Loading images from {person_subset}")

            # the data variable of the dataset class
            subsets[person_subset] = {}

            images = list(
                filter(lambda x: ".db" not in x,
                       listdir(str(images_folderpath)+f"\{person_subset}"))
            )  # discard the .db files.
            NUMBER_OF_IMAGES = len(images)
            #print(NUMBER_OF_IMAGES)
            images_loaded_counter += NUMBER_OF_IMAGES

            # image size is an array or a tuple with two elements (width,height)
            IMAGE_HEIGHT = self.shape[1]
            IMAGE_WIDTH = self.shape[0]

            x = np.zeros(shape=(NUMBER_OF_IMAGES,
                               IMAGE_HEIGHT,
                              IMAGE_WIDTH),
                         dtype="uint8")  # reserves the memory for more optimal use



            y = create_np_array_with_zeros(shape=NUMBER_OF_IMAGES)  # the klass for each image

            #x=[]
            for position, image_name in enumerate(images):
                # loads the image

            #    im = io.imread(str(images_folderpath)+f"\{person_subset}"+f"\{image_name}")
            #    im = im[np.newaxis, :, :]
            #   if len(im.shape) == 2:
            #       pass
            #    x.append(im)

                x[position] = io.imread(str(images_folderpath)+f"\{person_subset}"+f"\{image_name}")

                # loads the image klass in the array
                y[position] = self.klasess_ids[image_name[8]]  # the letter for the klass

            #x = np.vstack(x)
            # assign to the subset
            subsets[person_subset]["y"] = y
            subsets[person_subset]["x"] = x
        warning(
            f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")

        irish = Dataset('irish', subsets)
        return irish if subsets is not None else None
