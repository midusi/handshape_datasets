# handshape_datasets
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





