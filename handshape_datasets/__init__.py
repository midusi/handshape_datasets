import datasets_helpers as datasets
import os

options = {
    'aslA': datasets.aslA.download_and_extract,
    'aslB': datasets.aslB.download_and_extract,
    'ciarp': datasets.ciarp.download_and_extract,
    # 'indian_kinect': datasets.indian.download_and_extract,
    'isl': datasets.jsl.download_and_extract,
    'jsl': datasets.aslA.download_and_extract,
    'lsa16': datasets.aslA.download_and_extract,
    'nus_1': datasets.aslA.download_and_extract,
    'nus_2': datasets.aslA.download_and_extract,
    'psl': datasets.aslA.download_and_extract,
    'pugeault': datasets.aslA.download_and_extract,
    'rwth-phoenix': datasets.aslA.download_and_extract,
}

HOME_PATH_HANDSHAPE = os.path.join(os.getenv('HOME'),
                                   '.handshape_datasets')

for option in options.keys():
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
