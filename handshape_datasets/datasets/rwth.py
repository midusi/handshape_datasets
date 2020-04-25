from .common import *
import platform

labels = ['1', '2', '3', '3_hook', '4', '5', 'a', 'ae', 'b', 'b_nothumb', 'b_thumb', 'by', 'c', 'cbaby', 'd', 'e', 'f', 'f_open', 'fly', 'fly_nothumb', 'g', 'h', 'h_hook', 'h_thumb', 'i', 'index', 'index_flex', 'index_hook', 'ital', 'ital_nothumb', 'ital_open', 'ital_thumb', 'jesus', 'k', 'l_hook', 'o', 'obaby', 'pincet', 'r', 's', 'v', 'v_flex', 'w', 'write', 'y']

class RWTHInfo(ClassificationDatasetInfo):
    def __init__(self):
        description="""
            \n RWTH
        German Sign Language Handshapes dataset 
        More details can be found at https://www-i6.informatik.rwth-aachen.de/~koller/1miohands-data/
        """
        url_info = "https://www-i6.informatik.rwth-aachen.de/~koller/1miohands-data/"
        download_size = 46982846
        disk_size = 216876384
        subject = 3359
        super().__init__("rwth",(132,92,3),{"y":"Class labels"},description,labels, download_size, disk_size, subject, url_info)
    def get_loader(self):
        return RWTH()

class RWTH(DatasetLoader):
    def __init__(self):
        super().__init__("rwth")
        self.url = 'ftp://wasserstoff.informatik.rwth-aachen.de/pub/rwth-phoenix/2016/ph2014-dev-set-handshape-annotations.tar.gz'
        self.FILENAME = self.name + '.tar.gz'
        self.npz_filename = "rwth.npz"

    def urls(self):
        return self.url

    def download_dataset(self, folderpath):
        TARFILE_PATH = os.path.join(folderpath, self.FILENAME)
        download_file_over_ftp(ftp_url='wasserstoff.informatik.rwth-aachen.de',
                               ftp_relative_file_path='pub/rwth-phoenix/2016',
                               ftp_filename='ph2014-dev-set-handshape-annotations.tar.gz',
                               filepath=TARFILE_PATH)
        # set the success flag
        self.set_downloaded(folderpath)
        
    def load(self, folderpath, **kwargs):
        npz_filepath = os.path.join(folderpath, self.npz_filename)
        data = np.load(npz_filepath)
        x, y = (data["x"], data["y"])
        metadata = {"y": y}
        return x, metadata

    def images_folderpath(self,folderpath:Path)-> Path:
        return folderpath / f"{self.name}_images"

    def load_images(self,folderpath):
        extracted_folderpath=os.path.join(folderpath,"ph2014-dev-set-handshape-annotations")
        metadata_path = os.path.join(extracted_folderpath, "3359-ph2014-MS-handshape-annotations.txt")
        search="*"
        replace1="_"
        logging.info("Loading ph dataset from %s" % metadata_path)
        with open(metadata_path) as f:
            lines = f.readlines()
        lines = [x.strip().split(" ") for x in lines]
        for l in lines:
            assert (len(l) == 2)
        images_paths = [x[0] for x in lines]
        images_class_names = [x[1] for x in lines]
        if(platform.system()=="Windows"):
            logging.debug("SO: Windows")
            i=0
            for im in images_paths:
                images_paths[i]=im.replace(search, replace1)
                i=i+1
        classes = sorted(list(set(images_class_names)))
        y = np.array([classes.index(name) for name in images_class_names])
        paths = [os.path.join(extracted_folderpath, path) for path in images_paths]
        x = []
        for filepath in paths:
            im = io.imread(filepath)
            im = im[np.newaxis, :, :]
            if len(im.shape) == 2:
                pass
            x.append(im)
        x=np.vstack(x)
        return x,y

    def preprocess(self, folderpath):
        TARFILE_PATH = os.path.join(folderpath, self.FILENAME)
        # extract the tar into the images path
        extract_tar(TARFILE_PATH, folderpath)
        x,y=self.load_images(folderpath)
        npz_filepath=os.path.join(folderpath,self.npz_filename)
        np.savez(npz_filepath, x=x,y=y)
        os.remove(TARFILE_PATH)
        self.set_preprocessed_flag(folderpath)

    def delete_temporary_files(self, path):
        fpath = path / self.name
        folder = os.path.join(fpath, "ph2014-dev-set-handshape-annotations")
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