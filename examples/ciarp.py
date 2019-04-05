# Basic example showing how to get a dataset
import handshape_datasets as hd


DATASET_NAME = "ciarp"

ciarp = hd.load(DATASET_NAME)
print(ciarp)
