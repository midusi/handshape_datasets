import handshape_datasets as hd

for id in hd.ids():
    print(f"Loading {id}...")
    info = hd.info(id)
    x,metadata = hd.load(id)
    print(x.shape)
    for k in metadata:
        print(k,metadata[k].shape)
