import handshape_datasets as hd
import logging
import numpy as np
import matplotlib.pyplot as plt

import cv2
import os
from PIL import Image

#hd.list_datasets()

x,metadata=hd.load("PugeaultASL_A")

"""
for i in range(len(x)):
    if(metadata['y'][i]==1):
      plt.imshow(x[i,:,:])
      plt.figure()
      plt.show()
"""
for k in metadata:
   print(k,metadata[k].shape, metadata[k].min(), metadata[k].max())

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.DEBUG)
#logging.debug(f"This message should go to the log file")
#logging.info("So should this")
#logging.warning("And this, too")
"""
def read_pcd():
    output_path="C:\\Users\\corti\\.handshape_datasets\\indianB\\zafar142007B\\user1depthreshoot\\user1"
    path="C:\\Users\\corti\\.handshape_datasets\\indianB\\zafar142007B\\user1depthreshoot\\user1"
    #img_depth = np.zeros((32,32), dtype='f8')
    image = np.zeros((480,640, 1), dtype='uint16')
    file = open(os.path.join(path, "USER-1-1-1.txt"))
    infile = file.readlines()
    for (l, line) in enumerate(infile):
        dato = line.split(' ' or '\n')
        for (k, dat) in enumerate(dato):
            image[l, k, 0] = dat
    #image = cv2.imread(os.path.join(path, "USER-1-1-1.txt"), flags=cv2.IMREAD_UNCHANGED)
    min_z=image.min()
    max_min_diff_z=image.max()-image.min()
    def normalize(x):
        return 255 * (x - min_z) / max_min_diff_z

    normalize = np.vectorize(normalize, otypes=[np.float])
    img_depth = normalize(image)
    plt.imshow(img_depth[ :, :,0])
    plt.figure()
    plt.show()
    #img_depth_file = Image.fromarray((img_depth * 255).astype(np.uint8))
   #img_depth_file.convert('RGB').save(os.path.join(output_path,'depth_img.png'))
    return 0
"""
"""
read_pcd()
plt.imshow(x[0,:,:])
plt.figure()
plt.show()
"""