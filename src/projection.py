"""
    现在已获得在世界坐标系下的拼接点云，现在要将点云转换到相机坐标系下，并投影。
    World -> XT-16 -> RealSense
"""

import open3d as o3d
import numpy as np
import os
import cv2
import sys
import yaml
import time
sys.path.append(".")

from utils.functions import (odom_to_R_t, T_to_r_t, read_calib, R_t_to_T,
                             read_odom, read_image_list, read_pcd_list)
from utils.pcd2depth import pcd_projection, get_depth
from utils.util import print_progress, print_time


def project(directory_combined_pcd, directory_image, path_calib, directory_output):
    combined_pcd_list = read_pcd_list(directory_combined_pcd)
    image_list = read_image_list(directory_image)

    K, R, t = read_calib(path_calib)

    # 相机内参
    camera_intrinsics = K

    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(combined_pcd_list)

    start_index = int(os.path.splitext(os.path.basename(combined_pcd_list[0]))[0])
    # i表示为XT16时间戳序号（下标）
    for i in range(N):
        j = i + start_index
        if j >= N - 5:
            break

        path_pcd = combined_pcd_list[i]
        path_image = image_list[j]

        image_origin = cv2.imread(path_image)
        cloud_origin = o3d.io.read_point_cloud(path_pcd)

        path_output = os.path.join(directory_output, "{:06d}".format(j) + ".png")

        pcd_projection(image_origin, cloud_origin, camera_intrinsics, dist_coeffs, path_output)
        print_progress(i, N)

def generate_depth_gt(height, width, directory_combined_pcd, path_calib, directory_output_depth):
    combined_pcd_list = read_pcd_list(directory_combined_pcd)

    K, R, t = read_calib(path_calib)
    ### rrr
    # T = R_t_to_T(R, t)

    # 相机内参
    camera_intrinsics = K

    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(combined_pcd_list)

    start_index = int(os.path.splitext(os.path.basename(combined_pcd_list[0]))[0])
    # i表示为XT16时间戳序号（下标）
    start_time = time.time()
    print("---------------Depth Generating---------------")
    for i in range(N):
        j = i + start_index
        if j >= N - 5:
            break

        path_pcd = combined_pcd_list[i]
        cloud_origin = o3d.io.read_point_cloud(path_pcd)
        ### rrr
        # cloud_origin.transform(T)

        path_output = os.path.join(directory_output_depth, "{:06d}".format(j) + ".png")

        get_depth(height, width, cloud_origin, camera_intrinsics, dist_coeffs, path_output)
        print_progress(i, N)
    print("---------------End of Depth Generating---------------")
    end_time = time.time()
    dur_time = end_time - start_time
    print("Depth Spends {}s.".format(dur_time))

def generate_depth(height, width, directory_pcd, path_calib, directory_output_depth):
    pcd_list = read_pcd_list(directory_pcd)

    K, R, t = read_calib(path_calib)
    T = R_t_to_T(R, t)

    # 相机内参
    camera_intrinsics = K

    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(pcd_list)

    start_index = int(os.path.splitext(os.path.basename(pcd_list[0]))[0])
    # i表示为XT16时间戳序号（下标）
    start_time = time.time()
    print("---------------Depth Generating---------------")
    for i in range(N):
        j = i + start_index
        if j >= N - 5:
            break

        path_pcd = pcd_list[i]
        cloud_origin = o3d.io.read_point_cloud(path_pcd)
        cloud_origin.transform(T)

        path_output = os.path.join(directory_output_depth, "{:06d}".format(j) + ".png")

        get_depth(height, width, cloud_origin, camera_intrinsics, dist_coeffs, path_output)
        print_progress(i, N)
    print("---------------End of Depth Generating---------------")
    end_time = time.time()
    print_time(start_time, end_time)
    