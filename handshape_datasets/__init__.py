# no better way to do it since each is a submodule, not a function
# ,pugeault,rwth,lsa16
from .datasets_helpers import aslA, aslB, ciarp, irish, jsl, nus1, nus2, psl

import os


options = {
    'aslA': aslA.download_and_extract,
    'aslB': aslB.download_and_extract,
    'ciarp': ciarp.download_and_extract,
    # 'indian_kinect': indian.download_and_extract,
    # 'isl': irish.download_and_extract,
    'jsl': jsl.download_and_extract,
    # 'lsa16': lsa16.download_and_extract,
    'nus_1': nus1.download_and_extract,
    'nus_2': nus2.download_and_extract,
    'psl': psl.download_and_extract,
    # 'pugeault': pugeault.download_and_extract,
    # 'rwth-phoenix': rwth.download_and_extract
}
names = options.keys()

HOME_PATH_HANDSHAPE = os.path.join(os.getenv('HOME'),
                                   '.handshape_datasets')
try:
    os.mkdir(HOME_PATH_HANDSHAPE)  # default folder for creation
except FileExistsError:
    pass


def get(selected_dataset,
        folderpath=os.path.join(HOME_PATH_HANDSHAPE, 'files'),
        images_folderpath=os.path.join(HOME_PATH_HANDSHAPE, 'images'),
        download=True):
    if download is False:
        pass
    try:
        options[selected_dataset](folderpath, images_folderpath, download)
    except KeyError:
        print("The option {} isn't valid. The valid options are")
        for key, position in enumerate(options.keys()):
            print('{}. {}'.format(position, key))
