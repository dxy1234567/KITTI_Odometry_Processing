import os
import shutil
import sys
sys.path.append(".")
from utils.new_func import *
from utils.util import *


def generate_to_DC(src_dir, bin_dir, dir_dc, sequence):
    """
        Params:
            src_dir: 图片目录
            pcd_dir: 点云目录
            dir_dc: 要生成的目录的名字
            sequence: 序列数
    """
    src_dir = os.path.join(src_dir, '{:02d}'.format(sequence), 'image_0')
    bin_dir = os.path.join(bin_dir, '{:02d}'.format(sequence), 'velodyne')

    imgs_list = os.listdir(src_dir)
    pcds_list = os.listdir(bin_dir) 

    os.makedirs(os.path.join(dir_dc, "{:02d}".format(sequence)), exist_ok=True)


    # 创建toDC目录及子目录
    for item in os.listdir(dir_dc):
        dir_path = os.path.join(dir_dc, item)
        if os.path.isdir(dir_path):  # 检查是否为目录
            os.makedirs(os.path.join(dir_path, "gray"), exist_ok=True)
            os.makedirs(os.path.join(dir_path, "depth"), exist_ok=True)
            os.makedirs(os.path.join(dir_path, "depth_gt"), exist_ok=True)


    dir_img = src_dir
    dir_dst = os.path.join(dir_dc, "{:02d}".format(sequence), "gray")

    N = len(imgs_list)
    for i in range(N):
        filename = imgs_list[i]
        path_img = os.path.join(dir_img, filename)
        if os.path.isfile(path_img):  # 仅复制文件
            shutil.copy(path_img, dir_dst)
        print_progress(i, N)



src_dir = "/data/KITTI/data_odometry_gray/dataset/sequences/"  # 源目录
bin_dir = '/data/KITTI/data_odometry_velodyne/dataset/sequences/'
dir_dc = "/data/KITTI_to_DC/"

for sequence in range(4, 9):
    print(f'---------Sequence {sequence} begins')

    generate_to_DC(src_dir, bin_dir, dir_dc, sequence)

    print(f'---------Seuqnce {sequence} done.---------')

