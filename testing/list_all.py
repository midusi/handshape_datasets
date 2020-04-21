import handshape_datasets as hd
import logging


#hd.list_datasets()
x,metadata=hd.load("lsa16",version="colorbg", delete=True)
print(x.shape)
print(x.min())
print(x.max())
for k in metadata:
    print(k, metadata[k].shape, metadata[k].min(), metadata[k].max())

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.DEBUG)


