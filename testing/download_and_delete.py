# Basic example showing how to get a dataset
import handshape_datasets as hd


DATASET_NAME = "nus1"

nus1 = hd.load(DATASET_NAME)
# hd.clear("nus1")

# print(ciarp.summary())

# ciarp.show_dataset()

# ciarp.show_dataset(subsets=["test_Kinect_WithGabor"],samples=128)

# ciarp.show_dataset(subsets=["test_Kinect_WithGabor"],samples=[1,2,3,0,15,1,200])
