from numpy import zeros as create_np_array_with_zeros
from logging import warning
from os import path
from os import listdir, mkdir
from skimage import io
from string import ascii_uppercase

from .dataset import Dataset
from handshape_datasets.dataset_loader import DatasetLoader
from .utils import mkdir_unless_exists, download_file, extract_zip


class Irish(DatasetLoader):

    def __init__(self):
        super().__init__('irish')
        self.url = "https://github.com/marlondcu/ISL/blob/master/Frames/"
        self.klasess_ids = {
            klass: (id + 1) for (id, klass) in enumerate(list(ascii_uppercase))  # { A: 1, B: 2 }
        }

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
        urls = self.urls
        for filename in urls.keys():  # filename => Person1     f"{filename}.zip" # Person$7
            download_file(url=urls[filename],
                          filepath=zips_path,
                          filename=filename)

    def preprocess(self, folderpath, images_folderpath=None):
        # FALTA AGREGAR EL PREPROCESADO PARA CADA IMAGEN. HABRÍA QUE SOBRESCRIBIR LAS IMÁGENES??

        preprocess_flag = "{}_preprocessed".format(self.name)

        if self.get_status_flag(folderpath, preprocess_flag) is False:
            mkdir_unless_exists(images_folderpath)
            images_folderpath = path.join(
                folderpath, "%s_images" % self.name) if images_folderpath is None else images_folderpath
            folder_names = self.urls.keys()

            datasets = list(
                filter(lambda x: x[-4:] == '.zip',
                       listdir(path)))  # i just want the .zip files

            for dataset_file in datasets:
                dataset_folder_name = dataset_file[:-4]  # until the .zip(excluded)
                dataset_images_path = path.join(images_folderpath, dataset_folder_name)
                mkdir(dataset_images_path)
                extract_zip(dataset_file,
                            extracted_path=dataset_images_path)  # dataset_file has the format 'Person$.zip'

            self.set_preprocessed_flag(folderpath)

    def load(self, images_folderpath, image_size):
        subsets_folders = listdir(images_folderpath)  # the folders with the images are within image_folderpath XD
        subsets = {}
        images_loaded_counter = 0
        for person_subset in subsets_folders:
            warning(f"Loading images from {person_subset}")

            # the data variable of the dataset class
            subsets[person_subset] = {}

            images = list(
                filter(lambda x: ".db" not in x,
                       listdir(person_subset))
            )  # discard the .db files.

            NUMBER_OF_IMAGES = len(images)
            images_loaded_counter += NUMBER_OF_IMAGES

            # image size is an array or a tuple with two elements (width,height)
            IMAGE_HEIGHT = image_size[1]
            IMAGE_WIDTH = image_size[0]

            x = create_np_array_with_zeros(shape=(NUMBER_OF_IMAGES,
                                IMAGE_HEIGHT,
                                IMAGE_WIDTH),
                         dtype="uint8")  # reserves the memory for more optimal use

            y = create_np_array_with_zeros(shape=NUMBER_OF_IMAGES)  # the klass for each image

            for position, image_name in enumerate(images):
                # loads the image
                x[position] = io.imread(image_name)
                # loads the image klass in the array
                y[position] = self._get_klass_for_filename(image_name[8])  # the letter for the klass

            # assign to the subset
            subsets[person_subset]["y"] = y
            subsets[person_subset]["x"] = x
        warning(
            f"Dataset Loaded (´・ω・)っ. {images_loaded_counter} images were loaded")

        irish = Dataset('irish', subsets)
        return irish if subsets is not None else None


def _get_klass_for_filename(self, klass):
    return self.klasses_ids[klass]  # integer
