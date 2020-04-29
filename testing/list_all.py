import handshape_datasets as hd
import logging


#hd.list_datasets()
x,metadata=hd.load("Irish")
print(x.shape)
for k in metadata:
    print(k,metadata[k].shape, metadata[k].min(), metadata[k].max())

#hd.clear("Nus1")
logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.DEBUG)
#logging.debug(f"This message should go to the log file")
#logging.info("So should this")
#logging.warning("And this, too")

