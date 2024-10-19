"""
    现在已获得在世界坐标系下的拼接点云，现在要将点云转换到相机坐标系下，并投影。
    World -> XT-16 -> RealSense
"""

import open3d as o3d
import numpy as np
import os
import cv2
import sys
sys.path.append(".")

from utils.functions import (odom_to_R_t, T_to_r_t, read_calib, R_t_to_T,
                             read_odom, read_image_list, read_pcd_list)
from utils.pcd2depth import pcd_projection
from utils.util import print_progress

directory_combined_pcd = "/home/cjs/data/output/com_pcd_C_250/"   # 直接对拼接好的点云组进行操作
directory_image = "/home/cjs/data/KITTI/data_odometry_gray/dataset/sequences/00/image_0/"
path_odom = "/home/cjs/data/KITTI/data_odometry_poses/dataset/poses/00.txt"
path_calib = "/home/cjs/data/KITTI/data_odometry_calib/dataset/sequences/00/calib.txt"

odom_list = read_odom(path_odom)
combined_pcd_list = read_pcd_list(directory_combined_pcd)
image_list = read_image_list(directory_image)

K, R, t = read_calib(path_calib)

# 相机内参
camera_intrinsics = K

## 畸变参数
dist_coeffs = np.float64([0, 0, 0, 0, 0])


N = len(combined_pcd_list)

start_index = int(os.path.splitext(os.path.basename(combined_pcd_list[0]))[0])
directory_output = "/home/cjs/data/output/com_projection_C_250/"
# i表示为XT16时间戳序号（下标）
for i in range(N):
    j = i + start_index
    if j >= N - 5:
        break
    
    # T_WC, _, _ = odom_to_R_t(odom_list, j)
    # T_CW = np.linalg.inv(T_WC)

    # rvec, tvec = T_to_r_t(T_CW)
    rvec = np.array([[0], [0], [0]], dtype=np.float64)
    tvec = np.array([[0], [0], [0]], dtype=np.float64)

    path_pcd = combined_pcd_list[i]
    path_image = image_list[j]

    image_origin = cv2.imread(path_image)
    cloud_origin = o3d.io.read_point_cloud(path_pcd)

    path_output = os.path.join(directory_output, "{:06d}".format(j) + ".png")

    pts2d = pcd_projection(image_origin, cloud_origin, rvec, tvec, camera_intrinsics, dist_coeffs, path_output)
    print_progress(i, N)