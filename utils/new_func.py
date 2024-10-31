"""
读取实景实验中的数据所需的函数
"""

import numpy as np
import open3d as o3d
import os

def read_matrix(path_file):
    """
    读取矩阵，跳过注释行
    """
    matrix = []
    with open(path_file, 'r') as file:
        for line in file:
            # 去掉空白字符，并跳过注释行（以#开头）
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            matrix.append(list(map(float, line.split())))
    return np.array(matrix)

def poses_to_transformation_matrix(poses_lists):
    transformation_matrices = []
    for pose in poses_lists:
        # 提取平移向量 (tx, ty, tz) 和四元数 (qx, qy, qz, qw)
        tx, ty, tz = pose[1], pose[2], pose[3]
        qx, qy, qz, qw = pose[4], pose[5], pose[6], pose[7]

        # 使用四元数创建旋转矩阵
        rotation_matrix = o3d.geometry.get_rotation_matrix_from_quaternion([qw, qx, qy, qz])  # 注意四元数的顺序

        # 构建变换矩阵 T
        T = np.eye(4)
        T[:3, :3] = rotation_matrix  # 设置旋转矩阵
        T[:3, 3] = [tx, ty, tz]      # 设置平移向量

        # 存储变换矩阵
        transformation_matrices.append(T)
    
    return np.array(transformation_matrices)

def convert_timestamp_strings_to_floats(timestamps_list):
    """
    将时间戳字符串列表转换为浮点数列表
    """
    timestamps = []
    for timestamp in timestamps_list:
        timestamp_str = os.path.splitext(os.path.basename(timestamp))[0]
        timestamp_str.replace('_', ".")

        timestamps.append(float(timestamp_str))

    return timestamps

def match_closest_timestamps(timestamps_10hz_list, timestamps_15hz_list):
    timestamps_10hz = convert_timestamp_strings_to_floats(timestamps_10hz_list)
    timestamps_15hz = convert_timestamp_strings_to_floats(timestamps_15hz_list)

    start_timestamps = max(min(timestamps_10hz), min(timestamps_15hz))

    # matched_timestamps = []
    matched_indices = []  # 用于存储对应下标

    for t in timestamps_10hz:
        if t < start_timestamps:
            continue
        # 找到与当前10Hz时间戳t最接近的15Hz时间戳及其下标
        closest_index = min(range(len(timestamps_15hz)), key=lambda i: abs(timestamps_15hz[i] - t))
        # matched_timestamps.append(timestamps_15hz[closest_index])

        matched_indices.append(closest_index)

    return matched_indices


