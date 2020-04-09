# Basic example showing how to get a dataset
import handshape_datasets as hd

DATASET_NAME = "ciarp"
version=dict({'1':'WithGabor'})
#ciarp_info = hd.info(DATASET_NAME)
ciarp = hd.load(DATASET_NAME, **version)
print(x.shape)
for k in metadata:
    print(k,metadata[k].shape)

