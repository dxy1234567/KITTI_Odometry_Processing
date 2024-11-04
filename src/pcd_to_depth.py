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
from utils.util import *
from utils.new_func import *

path_cm = 'args/Mid_to_Camera.txt'
path_xm = 'args/Mid_to_XT.txt'
path_intrinsic = 'args/intrinsic.txt'

def pcd_to_depth(height, width, dir_pcd, dir_output):
    pcd_lists = read_pcd_list(dir_pcd)

    T_CL = read_matrix(path_cm)

    # 相机内参
    camera_intrinsics = read_matrix(path_intrinsic)

    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(pcd_lists)

    start_time = time.time()
    print("----------------Depth Genration begins----------------")
    for i in range(5, N - 5):
        filename = os.path.basename(pcd_lists[i])
        pcd_origin = o3d.io.read_point_cloud(pcd_lists[i])
        pcd_origin.transform(T_CL)
        
        path_output = os.path.join(dir_output, filename.replace('.pcd', '.png'))

        get_depth(height, width, pcd_origin, camera_intrinsics, dist_coeffs, path_output)

        print_progress(i, N)
    print("---------------End of Depth Generating---------------")
    end_time = time.time()
    print_time(start_time, end_time)

def pcd_to_com_depth(height, width, dir_pcd, path_poses, dir_output):
    poses_lists = read_matrix(path_poses)
    pcds_list = read_pcd_list(dir_pcd)

    poses_lists = poses_to_transformation_matrix(poses_lists)

    # 外参
    T_CL = read_matrix(path_cm)

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
    
def pcd_xt_to_mid_depth(height, width, dir_pcd, dir_output):
    """
    点云转深度图，从XT16到MID360到相机。
    """
    pcd_lists = read_pcd_list(dir_pcd)

    T_CM = read_matrix(path_cm)
    T_XM = read_matrix(path_xm)
    T_MX = np.linalg.inv(T_XM)

    # 相机内参
    camera_intrinsics = read_matrix(path_intrinsic)

    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(pcd_lists)

    start_time = time.time()
    print("----------------Depth Genration begins----------------")
    for i in range(5, N - 5):
        filename = os.path.basename(pcd_lists[i])
        pcd_origin = o3d.io.read_point_cloud(pcd_lists[i])
        T_CX = T_CM @ T_MX
        pcd_origin.transform(T_CX)
        
        path_output = os.path.join(dir_output, filename.replace('.pcd', '.png'))

        get_depth(height, width, pcd_origin, camera_intrinsics, dist_coeffs, path_output)

        print_progress(i, N)
    print("---------------End of Depth Generating---------------")
    end_time = time.time()
    print_time(start_time, end_time)

def pcd_xt_to_mid_com_depth(height, width, dir_pcd, path_poses, dir_output):
    """
    拼接点云，转深度图，从XT16到MID360到相机。
    """
    hf_poses_lists = read_matrix(path_poses)       # 读取高频位姿，第一列是时间戳
    pcds_list = read_pcd_list(dir_pcd)


    # 外参
    T_CM = read_matrix(path_cm)
    T_XM = read_matrix(path_xm)
    T_MX = np.linalg.inv(T_XM)
    T_CX = T_CM @ T_MX

    # 相机内参
    camera_intrinsics = read_matrix(path_intrinsic)
    ## 畸变参数
    dist_coeffs = np.float64([0, 0, 0, 0, 0])

    N = len(pcds_list)

    start_time = time.time()
    print("----------------Dense Depth Genration begins----------------")
    for i in range(5, N - 5):
        combined_pcd = o3d.geometry.PointCloud()
        filename = os.path.basename(pcds_list[i])   # basename带后缀
        t = find_closest_timestamp_index(filename, hf_poses_lists[:, 0])    # 对应高频位姿的下标

        T_WM = pose_to_T(hf_poses_lists, t)     ### MID坐标系到世界坐标系
        T_WX = T_WM @ T_MX              ### X坐标系到世界坐标系
        T_XW = np.linalg.inv(T_WX)      

        for j in range(i - 5, i + 5):
            pcd = o3d.io.read_point_cloud(pcds_list[j])

            T_WM = hf_poses_lists[j]
            T_WX = T_WM @ T_MX

            pcd.transform(T_WX)
            combined_pcd += pcd
        # 得到相机坐标系下的拼接点云
        T_CW = T_CX @ T_XW
        combined_pcd.transform(T_CW)
        ### 得到拼接点云
        
        path_output = os.path.join(dir_output, filename.replace('.pcd', '.png'))
        get_depth(height, width, combined_pcd, camera_intrinsics, dist_coeffs, path_output)

        print_progress(i, N)
    print("---------------End of Dense Depth Generating---------------")
    end_time = time.time()
    print_time(start_time, end_time)