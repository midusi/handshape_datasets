# Basic example showing how to get a dataset
import handshape_datasets as hd


DATASET_NAME = "ciarp"

ciarp = hd.get(DATASET_NAME)
print(len(ciarp["test_Kinect_WithGabor"]))
# TODO print dataset statistics, show some images
