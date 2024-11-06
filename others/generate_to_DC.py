import os
import shutil
import sys
sys.path.append(".")
from utils.new_func import *
from utils.util import *


def generate_to_DC(src_dir, pcd_dir, dir_dc, sequence):
    imgs_list = os.listdir(src_dir)
    pcds_list = os.listdir(pcd_dir) 

    matched_indices = match_closest_timestamps(pcds_list, imgs_list)

    os.makedirs(os.path.join(dir_dc, "{:02d}".format(sequence)), exist_ok=True)

    for item in os.listdir(dir_dc):
        dir_path = os.path.join(dir_dc, item)
        if os.path.isdir(dir_path):  # 检查是否为目录
            os.makedirs(os.path.join(dir_path, "gray"), exist_ok=True)
            os.makedirs(os.path.join(dir_path, "depth"), exist_ok=True)
            os.makedirs(os.path.join(dir_path, "depth_gt"), exist_ok=True)

        # dir_img = os.path.join(src_dir, "{:02d}".format(sequence), "image_0")
    dir_img = src_dir
    dir_dst = os.path.join(dir_dc, "{:02d}".format(sequence), "gray")

    for i in range(len(imgs_list)):
        if i in matched_indices:
            filename = imgs_list[i]
            path_img = os.path.join(dir_img, filename)
            if os.path.isfile(path_img):  # 仅复制文件
                shutil.copy(path_img, dir_dst)

src_dir = "/data/gml/20241103/gml_2024-11-03-17-26-31/_camera_infra1_image_rect_raw/"  # 源目录
pcd_dir = '/data/gml/20241103/gml_2024-11-03-17-26-31/_livox_lidar/'
dir_dc = "/data/gml_to_DC/"

sequence = 4

generate_to_DC(src_dir, pcd_dir, dir_dc, sequence)

