# no better way to do it since each is a submodule, not a function
# ,pugeault,rwth,lsa16


from .datasets_helpers import (aslA as _aslA,
                               aslB as _aslB,
                               ciarp as _ciarp,
                            #    irish as _irish,
                            #    indian_training as _indian_training,
                               jsl as _jsl,
                               nus1 as _nus1,
                               nus2 as _nus2,
                               psl as _psl,
                               rwth as _rwth)

import os as _os


_options = {
    #'aslA': aslA.AslA,
    #'aslB': aslB.AslB,
    'ciarp': _ciarp.Ciarp,
    # 'indian_kinect': indian_training.download_and_extract,
    # 'isl': irish.download_and_extract,
    'jsl': _jsl.Jsl,
    # 'lsa16': lsa16.download_and_extract,
    'nus1': _nus1.Nus1,
    'nus2': _nus2.Nus2,
    'psl': _psl.Psl,
    # 'pugeault': pugeault.download_and_extract,
    'rwth-phoenix': _rwth.Rwth
}

names=list(_options.keys())

HOME_PATH_HANDSHAPE = _os.path.join(_os.getenv('HOME'),
                                   '.handshape_datasets')
try:
    _os.mkdir(HOME_PATH_HANDSHAPE)  # default folder for creation
except FileExistsError:
    pass


def load(selected_dataset,
        folderpath=HOME_PATH_HANDSHAPE,
        images_folderpath=None):

    images_folderpath = _os.path.join(HOME_PATH_HANDSHAPE, selected_dataset,
                                     f"{selected_dataset}_images") if images_folderpath is None else images_folderpath
    try:
        # get downloader class for dataset
        dataset_class = _options[selected_dataset]
        # instance the class
        dataset = dataset_class()
        # load and return the dataset
        return dataset.get(folderpath, images_folderpath)

    except KeyError:
        print("The option {} isn't valid. The valid options are")
        for position, key in enumerate(_options.keys()):
            print('{}. {}'.format(position, key))


def help():
    message=f"""To load a dataset, call get('dataset'), where the supported datasets are:\n{", ".join(_options.keys())}\n\
        Examples:\n\
        import handshape_datasets\n\
        dataset=handshape_datasets.load('ciarp')\
        print(dataset.summary)
        """
    print(message)
