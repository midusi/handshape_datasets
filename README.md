

A single library to (down)load all existing sign language handshape datasets.

![handshape](http://facundoq.github.io/unlp/datasets/lsa16/files/dataset/1_1_1.png "sample handshape") 
![handshape](http://facundoq.github.io/unlp/datasets/lsa16/files/dataset/2_1_1.png "sample handshape")

There are [various handshape datasets](http://facundoq.github.io/unlp/sign_language_datasets/) for Sign Language. However:
* Each dataset has its own format and many are hard to find. 
* Each dataset has its own mapping of handshapes to classes. While Signs depend on the specific Sign Language for a country/region, handshapes are universal. Hence, they could be shared between datasets/tasks. 

This library aims to provide two main features:
* A simplified API to download and load handshape datasets
* A mapping between datasets so that datasets can be merged for training/testing models.

We hope it will help Sign Language Recognition develop further, both for research and application development.

If you wish to add a dataset you can make a push request, file an issue, or write to handshape.datasets@at@gmail.

This library is a *work in progress*. Contributions are welcome.
## Installation

You can install `handshape_datasets` via pip with:

`pip install handshape_datasets`

# Basic usage

Simply import the module and load a dataset. The following downloads, preprocesses and load to memory the [LSA16 dataset](http://facundoq.github.io/datasets/lsa16/):

    import handshape_datasets as hd
    images,metadata = hd.load("lsa16")
    
    import matplotlib.pyplot as plt
    plt.imshow(images[0,:,:,:]) # show the first sample of the dataset

# Advanced usage
    import handshape_datasets as hd
    hd.list_datasets() # List available datasets
    hd.load("lsa16",version="color",delete=True) # use the color version, delete temporary files
    hd.delete_temporary_files("lsa16")# Delete temporary files  (if any)
    hd.clear("lsa16") # Delete all the local files for dataset LSA16
    

# Supported datasets

+---------------+---------------+--------------+---------+---------+
|    Dataset    | Download size | Size on disk | Samples | Classes |
+---------------+---------------+--------------+---------+---------+
|     lsa16     |    640.6 Kb   |    1.2 Mb    |   800   |    16   |
|      rwth     |    44.8 Mb    |   206.8 Mb   |   3359  |    45   |
|     Irish     |    173.4 Mb   |   515.0 Mb   |  58114  |    26   |
|     Ciarp     |    10.6 Mb    |   18.6 Mb    |   7127  |    10   |
| PugeaultASL_A |     2.1 Gb    |    4.3 Gb    |  65774  |    24   |
| PugeaultASL_B |    317.4 Mb   |   717.9 Mb   |  72676  |    26   |
|    indianA    |     1.7 Gb    |    1.9 Gb    |   5040  |   140   |
|    indianB    |    320.5 Mb   |    8.6 Gb    |   5000  |   140   |
|      Nus1     |     2.8 Mb    |    3.6 Mb    |   479   |    10   |
|      Nus2     |    73.7 Mb    |   106.1 Mb   |   2750  |    10   |
|      jsl      |     4.5 Mb    |    7.9 Mb    |   8055  |    41   |
|      psl      |    285.2 Mb   |    1.2 Gb    |   960   |    16   |
+---------------+---------------+--------------+---------+---------+

## Training a handshape classifier with Keras



Load the dataset:

    dataset = handshape_datasets.load(dataset_id, version=ver, delete=supr)

Get the input_shape and number of classes:

    input_shape = self.dataset[0][0].shape
    classes = self.dataset[1]['y'].max() + 1

Define a model (using a pretrained MobileNet here):

    base_model = keras.applications.mobilenet.MobileNet(input_shape=(input_shape[0],self.input_shape[1],3), 
                                                                weights='imagenet', include_top=False)
    output = keras.layers.GlobalAveragePooling2D()(base_model.output)
    output = keras.layers.Dense(32, activation='relu')(output)
    output = keras.layers.Dense(self.classes, activation='softmax')(output)
    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

Split the dataset intro train/test sets:

    X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(self.dataset[0], self.dataset[1]['y'],
                                                                                    test_size=test_size,
                                                                                    stratify=self.dataset[1]['y'])

Fit the model

    history = model.fit(X_train, Y_train, batch_size=self.batch_size, epochs=self.epochs, validation_data=(X_test, Y_test))

# Google Colab example:

https://colab.research.google.com/drive/1kY-YrbegGFVT7NqVaeA4RjXYRVlZiISR?usp=sharing
