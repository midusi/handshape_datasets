# Basic example showing how to get a dataset
import handshape_datasets as hd


DATASET_NAME = "lsa16"

ciarp_info = hd.info(DATASET_NAME)
ciarp = hd.load(DATASET_NAME)


#print(ciarp_info.summary())

#ciarp[0].show_dataset() #nunca devuelve un dataset, sino que en el caso de lsa16 devuelve un np.array y un dict (x y metadata)

# ciarp.show_dataset(subsets=["test_Kinect_WithGabor"],samples=128)

# ciarp.show_dataset(subsets=["test_Kinect_WithGabor"],samples=[1,2,3,0,15,1,200])
