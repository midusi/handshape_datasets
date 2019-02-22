# Basic example showing how to get a dataset
import handshape_datasets as hd


DATASET_NAME = "ciarp"

ciarp = hd.get(DATASET_NAME)
<<<<<<< HEAD
ciarp.show_info()
=======
print(len(ciarp["test_Kinect_WithGabor"]))
# TODO print dataset statistics, show some images
question = input(
    "Do you want see some images and info about the dataset?. Y o N\n")
if question.lower() == 'y':
    for position, folder in enumerate(ciarp.keys()):
        print("The folder {} has {} images".format(folder, len(ciarp[folder])))
        plt.imshow(ciarp[folder][1], cmap='gray')
        plt.show()
>>>>>>> bc6ab9fd51f6594bd10de31188632282e8b2dd43
