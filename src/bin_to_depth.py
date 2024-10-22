import open3d as o3d
import numpy as np
import os
import sys
import yaml
import time
import cv2
sys.path.append(".")

from utils.functions import (odom_to_R_t, T_to_r_t, read_calib, R_t_to_T,
                             read_odom, read_image_list, read_pcd_list)
from utils.pcd2depth import get_depth
from utils.functions import get_point_cloud, read_odom, odom_to_R_t, read_pcd_list, read_image_list, read_calib, R_t_to_T
from utils.util import print_progress, print_time


def bin_to_depth(height, width, dir_pcd, path_calib, dir_output):
    pcd_lists = read_pcd_list(dir_pcd)

    K, R, t = read_calib(path_calib)
    T_CL = R_t_to_T(R, t)

    # 相机内参
    camera_intrinsics = K
    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(pcd_lists)

    start_time = time.time()
    print("----------------Depth Genration begins----------------")
    for i in range(5, N - 5):
        pcd_origin = get_point_cloud(pcd_lists[i])  # 得到PointCloud对象
        pcd_origin.transform(T_CL)
        
        path_output = os.path.join(dir_output, "{:06d}".format(i) + ".png")

        get_depth(height, width, pcd_origin, camera_intrinsics, dist_coeffs, path_output)

        print_progress(i, N)
    print("---------------End of Depth Generating---------------")
    end_time = time.time()
    print_time(start_time, end_time)

def bin_to_com_depth(height, width, dir_pcd, path_odom, path_calib, dir_output):
    odom_lists = read_odom(path_odom)
    pcd_lists = read_pcd_list(dir_pcd)

    K, R, t = read_calib(path_calib)
    T_CL = R_t_to_T(R, t)

    # 相机内参
    camera_intrinsics = K
    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(pcd_lists)

    start_time = time.time()
    print("----------------Dense Depth Genration begins----------------")
    for i in range(5, N - 5):
        combined_pcd = o3d.geometry.PointCloud()
        filename = os.path.basename(pcd_lists[i])
        filename = filename.replace(".bin", ".pcd")
        T_WC, _, _ = odom_to_R_t(odom_lists, i)    ### 相机坐标系到世界坐标系
        T_CW = np.linalg.inv(T_WC)                 ####世界坐标系到新相机坐标系

        for j in range(i - 5, i + 5):
            pcd = get_point_cloud(pcd_lists[j])

            T_WC, _, _ = odom_to_R_t(odom_lists, j)
            T_WL = T_WC @ T_CL 

            pcd.transform(T_WL)
            combined_pcd += pcd
        # 得到相机坐标系下的拼接点云
        combined_pcd.transform(T_CW)
        ### 得到拼接点云
        
        path_output = os.path.join(dir_output, "{:06d}".format(i) + ".png")
        get_depth(height, width, combined_pcd, camera_intrinsics, dist_coeffs, path_output)

        print_progress(i, N)
    print("---------------End of Dense Depth Generating---------------")
    end_time = time.time()
    print_time(start_time, end_time)
    
