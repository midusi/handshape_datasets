

A single library to (down)load all existing sign language handshape datasets.

![handshape](http://facundoq.github.io/unlp/lsa16/files/dataset/1_1_1.png "sample handshape") 
![handshape](http://facundoq.github.io/unlp/lsa16/files/dataset/2_1_1.png "sample handshape")

There are [various handshape datasets](http://facundoq.github.io/unlp/sign_language_datasets/) for Sign Language. However:
* Each dataset has its own format and many are hard to find. 
* Each dataset has its own mapping of handshapes to classes. While Signs depend on the specific Sign Language for a country/region, handshapes are universal. Hence, they could be shared between datasets/tasks. 

This library aims to provide two main features:
* A simplified API to download and load handshape datasets
* A mapping between datasets so that datasets can be merged for training/testing models.

We hope it will help Sign Language Recognition develop further, both for research and application development.

If you wish to add a dataset you can make a push request, file an issue, or write to handshape.datasets@at@gmail.

This library is a *work in progress*. Contributions are welcome.

## 						Working with images

- **<u>Identifiying Hand Classes</u>**

| Letter | Class ID |
| :----: | :------: |
|   a    |    0     |
|   b    |    1     |
|   c    |    2     |
|   d    |    3     |
|   e    |    4     |
|   f    |    5     |
|   g    |    6     |
|   h    |    7     |
|   i    |    8     |
|   j    |    9     |

### 						How to use?

    Import handshape_datasets

    handshape_datasets.load("dataset_id")
Download, extract and preprocess the dataset. The function will return "x" 
that contain an array with the images and metadata, this one contain an array with classes and if it have, an array with 
subjects or differents other values. For example, in lsa16 "x" will return a shape of (800,32,32,3). Also you could give
a version value if its available to the selected dataset and you could give a boolean value to delete temporary files if 
its possible
 
Example:
 
    handshape_datasets.load("lsa16",version="color",delete=True) --> download, extract and preprocess the lsa16 dataset in
    version "color" and delete the temporary files if its have a .npz file.

    handshape_datasets.clear("dataset_id") --> Delete all the local files for the dataset, if its exist.

    handshape_datasets.list_datasets() --> Returns a table with the information for the availables datasets

    handshape_datasets.delete_temporary_files("dataset_id") --> Delete the local files if its exist a .npz file

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

[Full example](https://colab.research.google.com/drive/1kY-YrbegGFVT7NqVaeA4RjXYRVlZiISR?usp=sharing)