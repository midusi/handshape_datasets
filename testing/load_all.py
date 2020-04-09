import handshape_datasets as hd
from handshape_datasets.config import options

for id in hd.ids():
    print(f"Loading {id}...")
    info = hd.info(id)
    if(options[id].id == 'Ciarp'):
        version = dict({'1': 'WithGabor'})
        x, metadata = hd.load(id, **version)
    else:
        x,metadata = hd.load(id)
    print(x.shape)
    for k in metadata:
        print(k,metadata[k].shape)
