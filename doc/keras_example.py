import handshape_datasets
import sklearn
import keras
from keras.models import Model

dataset_id="lsa16" #example for the lsa16 dataset
ver="color" #version is optional argument, some datasets has one version
supr=False #supr is optional, some datasets can delete temporary files if it have .npz file

epochs=15
batch_size=64


dataset = handshape_datasets.load(dataset_id, version=ver, delete=supr) #load the dataset
input_shape = dataset[0][0].shape #obtain the shape
classes = dataset[1]['y'].max() + 1 #obtain the number ofclasses

"""build the model"""
base_model = keras.applications.mobilenet.MobileNet(input_shape=(input_shape[0],input_shape[1],3), weights='imagenet',
                                                                include_top=False)
output = keras.layers.GlobalAveragePooling2D()(base_model.output)
output = keras.layers.Dense(32, activation='relu')(output)
output = keras.layers.Dense(classes, activation='softmax')(output)
model = Model(inputs=base_model.input, outputs=output)
model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

"""split the dataset (its optional)"""
test_size=0.1
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(dataset[0], dataset[1]['y'],
                                                                                    test_size=test_size,
                                                                                    stratify=dataset[1]['y'])
"""fit the model"""
history = model.fit(X_train, Y_train, batch_size=batch_size, epochs=epochs,
                                 validation_data=(X_test, Y_test))