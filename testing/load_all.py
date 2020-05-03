import handshape_datasets as hd
from handshape_datasets.config import options

for id in hd.ids():
    #info = hd.info(id)
    done = False
    if (options[id].id == 'Nus1'):
        x, metadata = hd.load(id, version='Color', delete=True)
        done=True
    if(options[id].id == 'Ciarp'):
        x, metadata = hd.load(id, version='WithoutGabor', delete=True)
        done = True
    if (options[id].id == 'Nus2'):
        x, metadata = hd.load(id, version='normal', delete=True)
        done = True
    if (not done):
        x, metadata = hd.load(id)
    print(x.shape)
    for k in metadata:
        print(k, metadata[k].shape, metadata[k].min(), metadata[k].max())
    #for k in metadata:
        #print(k,metadata[k].shape, metadata[k].min(), metadata[k].max())
