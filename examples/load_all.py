import handshape_datasets as hd

for name in hd.names:
    dataset = hd.load(name)
    print(dataset.summary())
