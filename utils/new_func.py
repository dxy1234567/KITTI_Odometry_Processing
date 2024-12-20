"""
读取实景实验中的数据所需的函数
"""

import numpy as np
import open3d as o3d
import os

def align_timestamps(poses_list, pcds_list):
    """
        位姿与点云的时间戳对齐
    """
    # 从第5个点云开始保留
    pcds_list = pcds_list[4:]

    # 获取两个列表的长度
    num_poses = len(poses_list)
    num_pcds = len(pcds_list)

    # 取两者中较小的长度
    num = min(num_poses, num_pcds)

    # 截断两个列表到相同长度
    poses_list = poses_list[:num]
    pcds_list = pcds_list[:num]

    return poses_list, pcds_list

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

def pose_to_T(poses_lists, i):
    """
    单个位姿转换为变换矩阵
    """
    pose = poses_lists[i]
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
    
    return np.array(T)

def poses_to_transformation_matrix(poses_lists):
    """
        将poses列表转换为变换矩阵列表T
    """

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
    """
    在15Hz时间戳中找到与10Hz时间戳数量相等的最接近的时间戳组。
    """
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

def find_closest_timestamp_index(target, timestamps):
    if target.endswith('.pcd'):
        target = target.replace('.pcd', '')

    target_float = float(target.replace('_', '.'))
    
    # 初始化最小差值和最近的时间戳下标
    min_diff = float("inf")
    closest_index = -1

    # 遍历时间戳组，将每个时间戳转换为浮点数并计算差值
    for i, ts in enumerate(timestamps):
        ts_float = float(ts)
        
        diff = abs(ts_float - target_float)
        if diff < min_diff:
            min_diff = diff
            closest_index = i

    return closest_index

def delete_files_before_common_timestamp(folder1, folder2, folder3):
    # 获取三个文件夹中的文件名列表，并提取时间戳
    timestamps1 = sorted([float(os.path.splitext(f)[0]) for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))])
    timestamps2 = sorted([float(os.path.splitext(f)[0]) for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))])
    timestamps3 = sorted([float(os.path.splitext(f)[0]) for f in os.listdir(folder3) if os.path.isfile(os.path.join(folder3, f))])

    # 找到三个文件夹中最小时间戳的最大值
    min_timestamp = max(timestamps1[0], timestamps2[0], timestamps3[0])

    # 定义删除文件的函数
    def delete_older_files(folder, min_timestamp):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            # 提取文件的时间戳并进行比较
            timestamp = float(os.path.splitext(filename)[0])
            if timestamp < min_timestamp:
                os.remove(file_path)  # 删除文件
                print(f"删除文件: {file_path}")

    # 删除三个文件夹中小于 min_timestamp 的文件
    delete_older_files(folder1, min_timestamp)
    delete_older_files(folder2, min_timestamp)
    delete_older_files(folder3, min_timestamp)

    # 对比并删除末尾文件，使文件数量相同
    def equalize_file_counts(folder1, folder2, folder3):
        # 获取每个文件夹中剩余文件的时间戳数量
        timestamps1 = sorted([f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))])
        timestamps2 = sorted([f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))])
        timestamps3 = sorted([f for f in os.listdir(folder3) if os.path.isfile(os.path.join(folder3, f))])

        # 获取最小的文件数量
        min_count = min(len(timestamps1), len(timestamps2), len(timestamps3))

        # 删除多出的文件（从末尾删除）
        for folder, timestamps in zip([folder1, folder2, folder3], [timestamps1, timestamps2, timestamps3]):
            if len(timestamps) > min_count:
                extra_files = timestamps[min_count:]  # 选取多出的文件
                for file in extra_files:
                    file_path = os.path.join(folder, file)
                    os.remove(file_path)
                    print(f"删除文件: {file_path}")

    # 调用函数对三个文件夹进行文件数量对齐
    equalize_file_counts(folder1, folder2, folder3)

def rename_files_in_sequence(folder):
    """
    将制作好的数据集按照顺序命名。
    """
    # 获取文件列表并按时间戳排序
    files = sorted([f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))],
                   key=lambda x: float(os.path.splitext(x)[0]))

    # 遍历并重命名文件
    for i, filename in enumerate(files):
        # 创建新的文件名，6位数，不足补0
        new_name = f"{i+1:06}.png"  # 假设文件后缀是.png
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)

        os.rename(old_path, new_path)
        print(f"重命名文件: {old_path} -> {new_path}")

def post_processing(folder1, folder2, folder3):
    delete_files_before_common_timestamp(folder1, folder2, folder3)
    rename_files_in_sequence(folder1)
    rename_files_in_sequence(folder2)
    rename_files_in_sequence(folder3)


