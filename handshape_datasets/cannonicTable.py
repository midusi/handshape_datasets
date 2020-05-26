import logging
import os
from pathlib import Path
from shutil import rmtree
from skimage import io


from PIL import Image
from skimage import transform

import handshape_datasets as hd
import numpy as np

import xlsxwriter

thisdict =	{
  "lsa16": [5,4,51,30,1,70,73,2,56,45,18,47,12,76,75,71],
  "Irish": [14,19,30,2,42,1,32,51,53,1,11,18,58,16,61,1,10,64,76,66,70,71,72,1,75,1],
  "rwth" : [12,1,3,78,4,5,14,6,20,19,18,14,34,75,41,42,43,63,52,51,50,54,1,69,53,2,2,73,36,35,38,23,11,71,55,61,21,46,64,76,71,40,72,74,75],
  "Ciarp": [14,20,69,70,12,51,56,53,1,80],
  "indianA":[2,71,72,4,5,1,56,3,1,1,1,1,1,14,1,1,1,1,1,1,1,1,1,1,20,1,30,1,1,30,1,68,1,1,1,1,42,1,48,1,1,43,1,1,1,1,2,1,1,1,1,1,1,76,70,1,1,1,53,1,1,1,71,56,1,1,1,48,12,56,1,1,1,1,45,15,1,1,59,1,1,12,1,1,61,1,1,1,1,76,1,1,1,1,67,1,1,1,1,1,64,1,1,20,41,1,1,1,1,1,1,76,1,1,1,1,1,45,1,1,66,1,50,2,70,71,1,1,71,1,2,1,1,72,1,73,1,1,75,1],
  "indianB":[2,71,72,4,5,1,56,3,1,1,1,1,1,14,1,1,1,1,1,1,1,1,1,1,20,1,30,1,1,30,1,68,1,1,1,1,42,1,48,1,1,43,1,1,1,1,2,1,1,1,1,1,1,76,70,1,1,1,53,1,1,1,71,56,1,1,1,48,12,56,1,1,1,1,45,15,1,1,59,1,1,12,1,1,61,1,1,1,1,76,1,1,1,1,67,1,1,1,1,1,64,1,1,20,41,1,1,1,1,1,1,76,1,1,1,1,1,45,1,1,66,1,50,2,70,71,1,1,71,1,2,1,1,72,1,73,1,1,75,1],
  "jsl":[12,53,71,57,61,54,60,1,19,24,76,1,1,1,22,12,1,1,45,70,1,1,73,1,82,2,1,1,35,9,1,1,32,75,72,1,64,3,56,40,9],
  "Nus1": [20,18,1,1,2,70,1,60,48,23],
  "Nus2": [14,20,70,75,1,21,1,56,48,1],
  "psl":[14,45,65,23,53,56,24,80,43,47,70,1,32,40,72,51],
  "PugeaultASL_A":[14,19,30,41,42,43,17,1,53,54,56,58,59,61,54,21,64,76,66,70,71,72,73,75],
  "PugeaultASL_B":[14,19,30,41,42,43,17,1,53,12,54,56,58,59,61,54,21,64,76,66,70,71,72,73,75,70],
}

def get_Cannonic():

  default_folder = Path.home() / 'handshape_datasets'
  path=os.path.join(default_folder,'images.xlsx')
  cache_path=os.path.join(default_folder, 'cache_canonic')
  if not os.path.exists(cache_path):
    logging.info(f"Create folder {cache_path}")
    os.makedirs(cache_path)
  workbook = xlsxwriter.Workbook(path)
  worksheet = workbook.add_worksheet()


  worksheet.set_column('A:A', 30)


  index=-1
  asl_class=1


  for col in range(1, 89):
    if(index==10):
      asl_class += 1
    if(index==29):
      asl_class += 1
    if (index == 44):
      asl_class += 2
    if (index == 49):
      asl_class += 1
    if (index == 62):
      asl_class += 2
    if (index == 86):
      asl_class += 1
    if(index==-1):
      worksheet.write(0, col, f"{index}")
      index += 1
    else:
      worksheet.write(0, col, f"{index}({asl_class})")
      worksheet.set_column(col, 32)
      index+=1
      asl_class+=1

  for i, dataset_id in enumerate(hd.ids()):
    x, metadata = hd.load(dataset_id)
    worksheet.write(i+1,0, dataset_id)
    worksheet.set_row(i+1, 32)
    flag = np.zeros(metadata['y'].max() + 1)
    if (x.shape[3] == 1):
      x = np.repeat(x, 3, -1)
    for h in range(len(x)):
      clas = metadata['y'][h]

      if(flag[clas]==0):
        path_to_save=os.path.join(cache_path,f"{dataset_id}image{h}.png")

        if (dataset_id == "PugeaultASL_B"):
          img_depth = np.zeros((x[h].shape[0], x[h].shape[1]), dtype='f8')
          max_z = x[h].max()
          min_z = x[h].min()
          max_min_diff_z = max_z - min_z
          img_depth = x[h]

          def normalize(x):
            return 255 * (x - min_z) / max_min_diff_z

          normalize = np.vectorize(normalize, otypes=[np.float])
          img_depth = normalize(img_depth)
          img_depth_file = Image.fromarray((img_depth).astype(np.uint8),mode = 'RGB')
          img_depth_file.convert('RGB').save(path_to_save)
        else:
          img = Image.fromarray((x[h]).astype(np.uint8))
          img = img.save(path_to_save)

        image= io.imread(path_to_save)
        original_type = image.dtype
        image= transform.resize(
              image, (32, 32), preserve_range=True, mode="reflect", anti_aliasing=True)
        image = image.astype(original_type)
        img2 = Image.fromarray(image)
        img2 = img2.save(path_to_save)
        flag[clas]=1
        ar=thisdict[dataset_id]
        worksheet.insert_image(i+1,ar[clas], path_to_save,{'x_offset':16,'y_offset': 5})



  workbook.close()
  if (os.path.exists(cache_path)):
    rmtree(cache_path)
  print("Done")
  return True