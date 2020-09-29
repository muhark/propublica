import sklearn.preprocessing as skpp
import numpy as np
import torch
import imageio
import os

a = imageio.imread("../db/images/23842565865340752.jpg")
a = np.array(a)
a = torch.tensor(a)
a.shape

image_dir = "../../db/images"
image_files = [image_dir+"/"+f for f in os.listdir(image_dir)]

dimensions = []
for f in image_files:
    id = f.split("/")[3].split(".")[0]
    try:
        a = imageio.imread(f)
    except ValueError:
        dimensions.append((id, (0, 0, 0)))
    dimensions.append((id, a.shape))

dims = [t[1] for t in dimensions]

[int(len(t)!=3) for t in dims].index(1)


dims[2052]
dimensions[2052][1]
a = imageio.imread(image_files[2052])
a.shape
torch.tensor(a).shape


for t in enumerate(dimensions):
    if len(t[1])!=3:
        print(t[0])
