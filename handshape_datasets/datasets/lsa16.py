from .common import *
from os import listdir
labels=["Five","Four","Horns","Curve","Fingers together","Double","Hook","Index","L","Flat Hand","Mitten","Beak","Thumb","Fist","Telephone","V"]

class LSA16Info(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n LSA16
        \n Argentinian Sign Language Handshapes dataset 
        \nMore details can be found at http://facundoq.github.io/unlp/lsa16/
        \n"""
        url_info = "http://facundoq.github.io/unlp/lsa16/"
        download_size = 655994
        disk_size = 1225566
        subject = 800
        super().__init__("lsa16",(32,32,3),{"y":"classes", "subject":"subject"},description, labels, download_size, disk_size, subject, url_info)
    def get_loader(self) ->DatasetLoader:
        return LSA16()

class LSA16(DatasetLoader):

    def __init__(self,version="lsa32x32_nr_rgb_black_background"):
        #TODO generate URL from options
        super().__init__("lsa16")
        self.filename = f"{version}.zip"
        self.url = f'http://facundoq.github.io/unlp/lsa16/data/{self.filename}'
        self.shape= (32,32) # TODO get from version
        self.classes = 16

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        zip_filepath= os.path.join(folderpath, self.filename)
        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            download_file(url=self.urls(), filepath=zip_filepath)
            # set the exit flag
            self.set_downloaded(folderpath)

    def images_folderpath(self,folderpath):
        return folderpath / f"{self.name}_images"

    def preprocess(self, folderpath):
        zip_filepath = os.path.join(folderpath, self.filename)
        if self.get_preprocessed_flag(folderpath) is False:
            # if it doenst receives the images_folderpath arg creates into folderpath
            images_folderpath = self.images_folderpath(folderpath)
            images_folderpath.mkdir(exist_ok=True)
            # extract the zip into the images path
            extract_zip(zip_filepath, images_folderpath)
            #remove the zipfile
            os.remove(zip_filepath)
            self.set_preprocessed_flag(folderpath)
        # if its already extracted doesnt do anything

    def load(self,folderpath):
        images_folderpath = self.images_folderpath(folderpath)
        # get image file names
        files = sorted(images_folderpath.iterdir())
        files = list(filter(lambda f: f.suffix in [".jpg",".png",".jpeg"], files))
        n = len(files)
        # pre-generate matrices
        x = np.zeros((n, self.shape[0], self.shape[1], 3), dtype='uint8')
        y = np.zeros(n, dtype='uint8')
        subjects = np.zeros(n)
        # Load images with labels
        for (i, filepath) in enumerate(files):
            # load image
            image = io.imread(filepath)
            x[i, :, :, :] = image
            # Get class and subject id for image
            filename=filepath.stem
            y[i] = int(filename.split("_")[0]) - 1
            subjects[i] = int(filename.split("_")[1]) - 1
        metadata={"y":y,"subjects":subjects}
        return x, metadata

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = self.images_folderpath(fpath)
        subsets_folders = list(
            filter(lambda x: '.npz' in x,
                   listdir(fpath)))
        if (len(subsets_folders) == 0):
            logging.warning(".npz not found")
        else:
            rmtree(folder)
        return True