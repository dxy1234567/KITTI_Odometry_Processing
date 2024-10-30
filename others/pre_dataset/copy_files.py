import os
import shutil
import sys
import argparse
sys.path.append(".")
from utils.util import print_progress

parser = argparse.ArgumentParser()

parser.add_argument('--src_dir', default="/data/KITTI/data_odometry_gray/dataset/sequences/")
parser.add_argument('--dst_to_dir', default='/data/KITTI_to_DC/')
parser.add_argument('--folder1', default='gray')
parser.add_argument('--folder2', default='depth')
parser.add_argument('--folder3', default='depth_gt')

args = parser.parse_args()

src_dir = args.src_dir          # 源目录
dst_to_dir = args.dst_to_dir    # 目标目录
folder1_name = args.folder1
folder2_name = args.folder2
folder3_name = args.folder3

# 创建序列文件夹
for i in range(11):
    os.makedirs(os.path.join(dst_to_dir, "{:02d}".format(i)))

# 创建文件夹
for item in os.listdir(dst_to_dir):
    dir_path = os.path.join(dst_to_dir, item)
    if os.path.isdir(dir_path):  # 检查是否为目录
        os.makedirs(os.path.join(dir_path, folder1_name), exist_ok=True)
        os.makedirs(os.path.join(dir_path, folder2_name), exist_ok=True)
        os.makedirs(os.path.join(dir_path, folder3_name), exist_ok=True)

# # 复制灰度图
# for i in range(11):
#     dir_img = os.path.join(src_dir, "{:02d}".format(i), "image_0")
#     dir_dst = os.path.join(dst_to_dir, "{:02d}".format(i), folder1_name)

#     for filename in os.listdir(dir_img):
#         path_img = os.path.join(dir_img, filename)
#         if os.path.isfile(path_img):  # 仅复制文件
#             shutil.copy(path_img, dir_dst)
#     print(i)

