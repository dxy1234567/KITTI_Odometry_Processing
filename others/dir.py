import os

dir_dc = "/data/KITTI_to_DC/"

for i in range(11):
    os.makedirs(os.path.join(dir_dc, "{:02d}".format(i)))