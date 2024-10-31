import open3d as o3d
import numpy as np
import os
import sys
import yaml
import time
import cv2
sys.path.append(".")

from utils.functions import *
from utils.pcd2depth import *
from utils.functions import *
from utils.util import *
from utils.new_func import *


def pcd_to_depth(height, width, dir_pcd, path_calib, path_intrinsic, dir_output):
    pcd_lists = read_pcd_list(dir_pcd)

    T_CL = read_matrix(path_calib)

    # 相机内参
    camera_intrinsics = read_matrix(path_intrinsic)

    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(pcd_lists)

    start_time = time.time()
    print("----------------Depth Genration begins----------------")
    for i in range(5, N - 5):
        filename = pcd_lists[i]
        pcd_origin = o3d.io.read_point_cloud(filename)
        pcd_origin.transform(T_CL)
        
        path_output = os.path.join(dir_output, filename.replace('.pcd', '.png'))

        get_depth(height, width, pcd_origin, camera_intrinsics, dist_coeffs, path_output)

        print_progress(i, N)
    print("---------------End of Depth Generating---------------")
    end_time = time.time()
    print_time(start_time, end_time)

def pcd_to_com_depth(height, width, dir_pcd, path_poses, path_calib, path_intrinsic, dir_output):
    poses_lists = read_matrix(path_poses)
    pcds_list = read_pcd_list(dir_pcd)

    poses_lists = poses_to_transformation_matrix(poses_lists)

    # 外参
    T_CL = read_matrix(path_calib)

    # 相机内参
    camera_intrinsics = read_matrix(path_intrinsic)
    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(pcds_list)

    start_time = time.time()
    print("----------------Dense Depth Genration begins----------------")
    for i in range(5, N - 5):
        combined_pcd = o3d.geometry.PointCloud()
        filename = os.path.basename(pcds_list[i])
        T_WL = poses_lists[i]           ### 相机坐标系到世界坐标系
        T_LW = np.linalg.inv(T_WL)                 ####世界坐标系到新相机坐标系

        for j in range(i - 5, i + 5):
            pcd = o3d.io.read_point_cloud(pcds_list[j])

            T_WL = poses_lists[j]

            pcd.transform(T_WL)
            combined_pcd += pcd
        # 得到相机坐标系下的拼接点云
        T_CW = T_CL @ T_LW
        combined_pcd.transform(T_CW)
        ### 得到拼接点云
        
        path_output = os.path.join(dir_output, filename.replace('.pcd', '.png'))
        get_depth(height, width, combined_pcd, camera_intrinsics, dist_coeffs, path_output)

        print_progress(i, N)
    print("---------------End of Dense Depth Generating---------------")
    end_time = time.time()
    print_time(start_time, end_time)
    
