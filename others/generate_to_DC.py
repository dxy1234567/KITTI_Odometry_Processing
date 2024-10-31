import os
import shutil
import sys
sys.path.append(".")
from utils.new_func import *
from utils.util import *

src_dir = "/data/gml/20241025/gml_2024-10-25-15-59-06/_camera_infra1_image_rect_raw/"  # 源目录
pcd_dir = '/data/gml/20241025/gml_2024-10-25-15-59-06/_livox_lidar/'
dir_dc = "/data/gml_to_DC/"

imgs_list = os.listdir(src_dir)
pcds_list = os.listdir(pcd_dir)

matched_indices = match_closest_timestamps(pcds_list, imgs_list)

N = 1

for i in range(N):
    os.makedirs(os.path.join(dir_dc, "{:02d}".format(i)), exist_ok=True)

for item in os.listdir(dir_dc):
    dir_path = os.path.join(dir_dc, item)
    if os.path.isdir(dir_path):  # 检查是否为目录
        os.makedirs(os.path.join(dir_path, "gray"), exist_ok=True)
        os.makedirs(os.path.join(dir_path, "depth"), exist_ok=True)
        os.makedirs(os.path.join(dir_path, "depth_gt"), exist_ok=True)

for i in range(N):
    # dir_img = os.path.join(src_dir, "{:02d}".format(i), "image_0")
    dir_img = src_dir
    dir_dst = os.path.join(dir_dc, "{:02d}".format(i), "gray")

    for i in range(len(imgs_list)):
        if i in matched_indices:
            filename = imgs_list[i]
            path_img = os.path.join(dir_img, filename)
            if os.path.isfile(path_img):  # 仅复制文件
                shutil.copy(path_img, dir_dst)
    print_progress(i, len(imgs_list))



