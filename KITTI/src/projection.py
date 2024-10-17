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

from utils.functions import read_image_list, read_odom, read_pcd_list, find_closest_timestamp, odom_to_T_r, T_to_r_t, list_to_timestamps, timestamps_20
from utils.get_one_combined_pcd import get_one_pcd
from utils.pcd2depth import pcd_projection

directory_combined_pcd = "/home/cjs/rosbag/2024-09-27/gml_2024-09-27-17-10-28/output"   # 直接对拼接好的点云组进行操作
directory_pcd = "/home/cjs/rosbag/2024-09-27/gml_2024-09-27-17-10-28/_hesai_pandar"
directory_image = "/home/cjs/rosbag/2024-09-27/gml_2024-09-27-17-10-28/_camera_infra1_image_rect_raw"
path_odom = "/home/cjs/rosbag/2024-09-27/gml_2024-09-27-17-10-28/odom_noggo_gml_2024-09-27-17-10-28.txt"

odom_list = read_odom(path_odom)
combined_pcd_list = read_pcd_list(directory_combined_pcd)
pcd_list = read_pcd_list(directory_pcd)
image_list = read_image_list(directory_image)

timestamps_combined_pcd = list_to_timestamps(combined_pcd_list)
timestamps_combined_pcd_20 = timestamps_20(timestamps_combined_pcd)
timestamps_pcd = list_to_timestamps(pcd_list)
timestamps_pcd_20 = timestamps_20(timestamps_pcd)
timestamps_image = list_to_timestamps(image_list)
timestamps_image_20 = timestamps_20(timestamps_image)

# 相机内参
## 
camera_intrinsics= np.float64([[431.574523925781, 0, 429.674438476562],
                            [0, 431.574523925781, 237.917541503906],
                            [0, 0, 1]])

## 畸变参数
dist_coeffs = np.float64([0, 0, 0, 0, 0])

# 外参: XT to RealSense
T_RM = np.array([
    [-0.0347702, -0.999329, -0.0115237, 0.113479],
    [0.0359214, 0.0102735, -0.999302, -0.216314],
    [0.99875, -0.0351599, 0.0355401, -0.00212184],
    [0, 0, 0, 1]
])

T_MR = np.linalg.inv(T_RM)

T_XM = np.array([
    [-0.002, 1, -0.019, 0.009],
    [-0.999, -0.003, -0.042, -0.008],
    [-0.042, 0.018, 0.999, 0.06],
    [0, 0, 0, 1]
])

T_MX = np.linalg.inv(T_XM)

T_1 = T_MR @ T_XM
T_2 = T_MR @ T_MX
T_3 = T_RM @ T_XM
T_4 = T_RM @ T_MX
T_5 = np.linalg.inv(T_1)
T_6 = np.linalg.inv(T_2)
T_7 = np.linalg.inv(T_3)
T_8 = np.linalg.inv(T_4)

# T_RX = np.linalg.inv(T_MR @ T_XM)

N = min(len(combined_pcd_list), len(image_list))

directory_output = "/home/cjs/rosbag/2024-09-27/gml_2024-09-27-17-10-28/projection"
# i表示为XT16时间戳序号（下标）
for i in range(N):
    # combine_pcd = get_one_pcd(i)

    timestamp_pcd = timestamps_combined_pcd_20[i]

    # 找到最接近当前雷达时间戳的相机时间戳
    stamp_image, j = find_closest_timestamp(timestamps_image_20, timestamp_pcd)

    index_pcd = timestamps_pcd_20.index(timestamp_pcd)

    T_WX, _, _ = odom_to_T_r(odom_list, index_pcd)  # #####
    T_XW = np.linalg.inv(T_WX)

    T_RW = T_3 @ T_XW

    rvec, tvec = T_to_r_t(T_RW)

    path_pcd = pcd_list[i]
    path_image = image_list[j]

    image_origin = cv2.imread(path_image)
    cloud_origin = o3d.io.read_point_cloud(path_pcd)

    path_output = os.path.join(directory_output, timestamps_image[j] + ".png")

    pts2d = pcd_projection(image_origin, cloud_origin, rvec, tvec, camera_intrinsics, dist_coeffs, path_output)
