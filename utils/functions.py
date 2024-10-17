import open3d as o3d
import os
import numpy as np
import bisect
import cv2

def read_calib(path_file):
    """
        读取KITTI的外参信息，读取左相机。
    """
    with open(path_file, 'r') as file:
        for line in file:
            if line.startswith("P0"):
                key, values = line.split(":")
                values = values.split()
                projections_list = [float(v) for v in values]   # 投影矩阵 
            elif line.startswith("Tr"):
                key, values = line.split(":")
                values = values.split()
                trans_list = [float(v) for v in values]         # 变换矩阵

    K = np.array([[projections_list[0], projections_list[1], projections_list[2]],
                  [projections_list[4], projections_list[5], projections_list[6]],
                  [projections_list[8], projections_list[9], projections_list[10]]])

    R = np.array([[trans_list[0], trans_list[1], trans_list[2]],
                  [trans_list[4], trans_list[5], trans_list[6]],
                  [trans_list[8], trans_list[9], trans_list[10]]])
    
    t = np.array([[trans_list[3]], [trans_list[7]], [trans_list[11]]])

    return K, R, t

def read_kitti_bin_file(bin_path):
    # 读取二进制文件
    point_cloud = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 4)
    # 将点的x, y, z坐标提取出来
    points = point_cloud[:, :3]
    return points

def get_point_cloud(bin_path):
    # 将点转换为 Open3D 的 PointCloud 对象
    points = read_kitti_bin_file(bin_path)

    points_3d = o3d.geometry.PointCloud()
    points_3d.points = o3d.utility.Vector3dVector(points)
    return points_3d


def read_calibration_file(file_path):
    calibration_data = {}

    with open(file_path, 'r') as file:
        for line in file:
            # 去除前后空格并分割成key-value对
            line = line.strip()
            if line:
                key, value = line.split(':', 1)
                # 将矩阵元素转换为浮点数
                calibration_data[key] = [float(x) for x in value.split()]

    return calibration_data

def extract_timestamp(file_name):
    # 提取文件名中的时间戳部分（假设格式如 "file_<秒数>_<纳秒数>.txt"）
    # 先移除前缀 "file_" 和后缀 ".txt"
    timestamp = os.path.splitext(file_name)[0]
    sec, nsec = map(int, timestamp.split('_'))
    return sec, nsec

def read_odom(path_odom):
    odom_lists = []
    with open(path_odom) as file:
        for line in file:
            line = line.strip()
            data = list(map(float, line.split()))
            odom_lists.append(data)

    return odom_lists

def odom_to_T_r(odom_lists, i):
    """
        将第i行对应的位姿信息转换成旋转矩阵T和平移向量t
    """
    odom = odom_lists[i]

    R = np.zeros((3, 3))
    t = np.zeros((3, 1))

    R[0, :3] = odom[0:3]
    R[1, :3] = odom[4:7]
    R[2, :3] = odom[8:11]

    t[0] = odom[3]
    t[1] = odom[7]
    t[2] = odom[11]
    t = t.flatten()

    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t

    return T, R, t

def pad_to_20_chars(s):
    """
    如果字符串长度不足20位，则在第11位处插入'0'，直到其长度为20位。
    """
    # 检查字符串长度
    if len(s) < 20:
        # 计算需要插入多少个'0'
        num_zeros = 20 - len(s)
        
        # 插入'0'，在第11位处插入
        s = s[:11] + '0' * num_zeros + s[11:]
    
    return s

def timestamps_20(timestamps):
    """
        return: float
    """
    return [float(pad_to_20_chars(timestamp)) for timestamp in timestamps]

def find_closest_timestamp(timestamps, timestamp):
    """
        从时间戳组中找到最接近时间戳的时间戳。
        这里的比较不能是字符串比较，存在缺位问题、求差问题。
    """
    # 使用bisect模块的bisect_left函数查找插入点
    idx = bisect.bisect_left(timestamps, timestamp)
    
    # 边界条件处理
    if idx == 0:
        return timestamps[0], -1
    elif idx == len(timestamps):
        return timestamps[-1], -1
    
    # 找到最接近的时间戳
    before = timestamps[idx - 1]
    after = timestamps[idx]
    
    # 比较哪个时间戳更接近雷达时间戳
    if timestamp - before < after - timestamp:
        return before, idx - 1
    else:
        return after, idx
    
def path_to_timestamp(file_path):
    """
        单个路径转为整数时间戳
    """
    filename = os.path.basename(file_path)      # 去除父文件
    timestamp, _ = os.path.splitext(filename)   # 去除后缀
    timestamp = timestamp.replace('_', '.')     # 下划线转为点.
    timestamp = float(timestamp)
    return timestamp

def T_to_r_t(T):
    R = T[:3, :3]
    r, _ = cv2.Rodrigues(R)

    t = T[:3, 3]

    return r, t

def read_pcd_list(directory_pcd):
    pcd_lists = []

    for file_name in sorted(os.listdir(directory_pcd)):
        if file_name.endswith(".bin"):
            file_path = os.path.join(directory_pcd, file_name)
            pcd_lists.append(file_path)
    return pcd_lists

def read_image_list(directory_image):
    image_lists = []

    for file_name in sorted(os.listdir(directory_image)):
        if file_name.endswith(".png"):
            file_path = os.path.join(directory_image, file_name)
            image_lists.append(file_path)
    return image_lists

def list_to_timestamps(list):
    """
        return: String
    """
    return [os.path.splitext(os.path.basename(path))[0] for path in list]

def depth_within_255(max_depth, min_depth, cur_depth):
    # 防止除以零的情况
    if max_depth == min_depth:
        return 0
    
    # 按照 [0, 255] 的范围进行线性放缩
    scaled_depth = 255 * (cur_depth - min_depth) / (max_depth - min_depth)
    
    # 确保返回的是 uint8 类型的值（深度值在 0 到 255 范围）
    return int(scaled_depth)

