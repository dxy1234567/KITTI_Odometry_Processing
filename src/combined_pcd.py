import open3d as o3d
import numpy as np
import os
import sys
sys.path.append(".")

from utils.functions import get_point_cloud, read_odom, odom_to_R_t, read_pcd_list, read_image_list, read_calib, R_t_to_T
from utils.util import print_progress

directory_pcd = "/home/cjs/data/KITTI/data_odometry_velodyne/dataset/sequences/00/velodyne"
directory_image = "/home/cjs/data/KITTI/data_odometry_gray/dataset/sequences/00/image_0"
path_odom = "/home/cjs/data/KITTI/data_odometry_poses/dataset/poses/00.txt"
path_calib = "/home/cjs/data/KITTI/data_odometry_calib/dataset/sequences/00/calib.txt"

path_output = "/home/cjs/data/output/com_pcd_"

odom_lists = read_odom(path_odom)
pcd_lists = read_pcd_list(directory_pcd)
image_lists = read_image_list(directory_image)

_, R, t = read_calib(path_calib)
T_CL = R_t_to_T(R, t)

N = min(len(pcd_lists), len(image_lists))

print("----------------Combining begins----------------")
for i in range(5, N - 5):
    combined_pcd = o3d.geometry.PointCloud()
    filename = os.path.basename(pcd_lists[i])
    filename = filename.replace(".bin", ".pcd")
    T, _, _ = odom_to_R_t(odom_lists, i)    ### 
    T_CW = np.linalg.inv(T)                 ####

    for j in range(i - 5, i + 5):
        
        pcd = get_point_cloud(pcd_lists[j])

        T_WC, _, _ = odom_to_R_t(odom_lists, j)

        T_WL = T_WC @ T_CL 

        pcd.transform(T_WL)

        combined_pcd += pcd

    combined_pcd.transform(T_CW)

    path = os.path.join(path_output, filename)
    o3d.io.write_point_cloud(path, combined_pcd)

    print_progress(i, N)
    







