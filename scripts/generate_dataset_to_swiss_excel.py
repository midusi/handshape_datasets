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


from handshape_datasets import dataset_to_swiss_table
from handshape_datasets.base import default_folder

if __name__ == "__main__":
    path = default_folder / 'dataset_to_swiss.xlsx'
    cache_path = default_folder / 'cache_canonic'
    if not cache_path.exists():
        logging.info(f"Create folder {cache_path}")
        os.makedirs(cache_path,exist_ok=True,parents=True)
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
                    path_to_save=cache_path /f"{dataset_id}image{h}.png"

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
                ar=dataset_to_swiss_table[dataset_id]
                worksheet.insert_image(i+1,ar[clas], path_to_save,{'x_offset':16,'y_offset': 5})
    
    workbook.close()
    if (os.path.exists(cache_path)):
        rmtree(cache_path)
    print("Done")

