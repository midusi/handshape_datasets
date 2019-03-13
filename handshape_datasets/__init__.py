import os as _os
from .datasets_helpers.config import options as _options

names=list(_options.keys())

_HOME_PATH_HANDSHAPE = _os.path.join(_os.getenv('HOME'),
                                   '.handshape_datasets')
try:
    _os.mkdir(_HOME_PATH_HANDSHAPE)  # default folder for creation
except FileExistsError:
    pass


def load(selected_dataset,
         folderpath=_HOME_PATH_HANDSHAPE,
         images_folderpath=None):

    images_folderpath = _os.path.join(_HOME_PATH_HANDSHAPE, selected_dataset,
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
