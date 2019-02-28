# Basic example showing how to get a dataset
import handshape_datasets as hd


dataset_name = "rwth-phoenix"

rwth = hd.get(dataset_name)
rwth.show_info()
