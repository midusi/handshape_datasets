# Basic example showing how to get a dataset
import handshape_datasets as hd


DATASET_NAME = "ciarp"

ciarp = hd.get(DATASET_NAME)
ciarp.show_info()
