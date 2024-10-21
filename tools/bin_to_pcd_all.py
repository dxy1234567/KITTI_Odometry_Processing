import numpy as np
import open3d as o3d
import sys
import os
sys.path.append(".")

from utils.functions import read_pcd_list, get_point_cloud
from utils.util import print_progress


directory_pcd = "/home/cjs/data/KITTI/data_odometry_velodyne/dataset/sequences/00/velodyne"
directory_output = "/home/cjs/data/output/pcd/"

pcd_list = read_pcd_list(directory_pcd)
start_index = int(os.path.splitext(os.path.basename(pcd_list[0]))[0])
N = len(pcd_list)
for i in range(N):
    j = i + start_index
    ###
    path_bin = pcd_list[i]
    pcd = get_point_cloud(path_bin)
    path_output = os.path.join(directory_output, "{:06d}".format(j) + ".pcd")
    o3d.io.write_point_cloud(path_output, pcd)

    print_progress(i, N)
    