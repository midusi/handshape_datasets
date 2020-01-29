# no better way to do it since each is a submodule, not a function
# ,pugeault,rwth,lsa16
from .datasets_helpers import aslA, aslB, ciarp, irish, indian_training, jsl, nus1, nus2, psl, rwth

import os


options = {
    'aslA': aslA.AslA,
    'aslB': aslB.AslB,
    'ciarp': ciarp.Ciarp,
    # 'indian_kinect': indian_training.download_and_extract,
    # 'isl': irish.download_and_extract,
    'jsl': jsl.Jsl,
    # 'lsa16': lsa16.download_and_extract,
    'nus_1': nus1.Nus1,
    'nus_2': nus2.Nus2,
    # 'psl': psl.download_and_extract,
    # 'pugeault': pugeault.download_and_extract,
    'rwth-phoenix': rwth.Rwth
}


HOME_PATH_HANDSHAPE = os.path.join(os.getenv('HOME'),
                                   '.handshape_datasets')
try:
    os.mkdir(HOME_PATH_HANDSHAPE)  # default folder for creation
except FileExistsError:
    pass


def get(selected_dataset,
        folderpath=HOME_PATH_HANDSHAPE,
        images_folderpath=None):

    images_folderpath = os.path.join(HOME_PATH_HANDSHAPE, selected_dataset,
                                     f"{selected_dataset}_images") if images_folderpath is None else images_folderpath
    try:
        # get downloader class for dataset
        dataset_class = options[selected_dataset]
        dataset = dataset_class()  # instance the class
        return dataset.get(folderpath, images_folderpath)

    except KeyError:
        print("The option {} isn't valid. The valid options are")
        for position, key in enumerate(options.keys()):
            print('{}. {}'.format(position, key))
