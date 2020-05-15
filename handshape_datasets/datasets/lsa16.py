from .common import *
from os import listdir
from skimage import transform
labels=["Five","Four","Horns","Curve","Fingers together","Double","Hook","Index","L","Flat Hand","Mitten","Beak","Thumb","Fist","Telephone","V"]

class LSA16Info(ClassificationDatasetInfo):
    def __init__(self):
        description="""
        \n LSA16
        Argentinian Sign Language Handshapes dataset 
        More details can be found at http://facundoq.github.io/unlp/lsa16/
        \nVersion default : color\nOther version : colorbg
        """
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
        self.filename =[f"{version}", f"lsa_nr_rgb"]
        self.url = [f'http://facundoq.github.io/unlp/lsa16/data/{self.filename[0]}.zip', f"http://facundoq.github.io/unlp/lsa16/data/{self.filename[1]}.zip"]
        self.shape= (32,32) # TODO get from version
        self.classes = 16

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):

        # check if the dataset is downloaded
        file_exists = self.get_downloaded_flag(folderpath)
        if file_exists is False:
            for (i,url) in enumerate(self.url):
                zip_filepath = os.path.join(folderpath, f"{self.filename[i]}.zip")
                download_file(url=url, filepath=zip_filepath)
                # set the exit flag
            self.set_downloaded(folderpath)

    def images_folderpath(self,folderpath):
        return folderpath / f"{self.name}_images"

    def preprocess(self, folderpath):

        if self.get_preprocessed_flag(folderpath) is False:
            # if it doenst receives the images_folderpath arg creates into folderpath
            for (i,filename) in enumerate(self.filename):
                zip_filepath = os.path.join(folderpath, f"{filename}.zip")
                images_folderpath = self.images_folderpath(folderpath)
                images_folderpath.mkdir(exist_ok=True)
                # extract the zip into the images path
                extract_zip(zip_filepath, os.path.join(images_folderpath,filename))
                #remove the zipfile
                os.remove(zip_filepath)
            self.set_preprocessed_flag(folderpath)
        # if its already extracted doesnt do anything

    def load(self,folderpath,**kwargs):

        images_folderpath=self.images_folderpath((folderpath))

        if 'version' in kwargs:
            options = ['color', 'colorbg']
            try:
                class UnAcceptedValueError(Exception):
                    def __init__(self, data):
                        self.data = data

                    def __str__(self):
                        return repr(self.data)

                if ((kwargs['version']) != options[0]) and ((kwargs['version']) != options[1]):
                    raise UnAcceptedValueError(
                        f"Version {kwargs['version']} is not valid. Valid options: {options[1]} , {options[0]}")
                else:
                    if (kwargs['version'] == options[0]):
                        logging.info(f"Loading version: {kwargs['version']}")
                        images_folderpath_act = os.path.join(images_folderpath, self.filename[0])
                        ver = "color"
                    else:
                        if (kwargs['version'] == options[1]):
                            logging.info(f"Loading version: {kwargs['version']}")
                            images_folderpath_act_1 = os.path.join(images_folderpath, self.filename[1])
                            images_folderpath_act = os.path.join(images_folderpath_act_1, "cut_with_background")
                            ver = "colorbg"

            except UnAcceptedValueError as e:
                logging.error(f"Received error:{e.data}")
                exit()
        else:
            logging.info(f"Loading default version: color")
            images_folderpath_act = os.path.join(images_folderpath, self.filename[0])
            ver = "color"
        # get image file names
        files = sorted(Path(images_folderpath_act).iterdir())
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
            if(ver=="colorbg"):
                image=transform.resize(image, (32, 32), preserve_range=True, mode="reflect",
                                 anti_aliasing=True)
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
            return False
        else:
            if (os.path.exists(folder)):
                rmtree(folder)
            else:
                return False
            return True