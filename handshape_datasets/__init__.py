# no better way to do it since each is a submodule, not a function
from .datasets_helpers import aslA,aslB,ciarp,irish,jsl,nus1,nus2,psl#,pugeault,rwth,lsa16

import os


options = {
    'aslA': aslA.download_and_extract,
    'aslB': aslB.download_and_extract,
    'ciarp': ciarp.download_and_extract,
    # 'indian_kinect': indian.download_and_extract,
    'isl': irish.download_and_extract,
    'jsl': jsl.download_and_extract,
    # 'lsa16': lsa16.download_and_extract,
    'nus_1': nus1.download_and_extract,
    'nus_2': nus2.download_and_extract,
    'psl': psl.download_and_extract,
    # 'pugeault': pugeault.download_and_extract,
    # 'rwth-phoenix': rwth.download_and_extract
}
names=options.keys()

HOME_PATH_HANDSHAPE = os.path.join(os.getenv('HOME'),
                                   '.handshape_datasets_helpers')

for option in options:
    os.mkdir(os.path.join(HOME_PATH_HANDSHAPE, 'zips', option))


def get(selected_dataset,
        folderpath=os.path.join(HOME_PATH_HANDSHAPE, 'zips'),
        images_folderpath=os.path.join(HOME_PATH_HANDSHAPE, 'images'),
        download=True):
    if download is False:
        # check if the file DOWNLOADED EXIST
        pass
    try:
        options[selected_dataset](folderpath, images_folderpath, download)
    except KeyError:
        print("The option {} isn't valid. The valid options are")
        for key, position in enumerate(options.keys()):
            print('{}. {}'.format(position, key))