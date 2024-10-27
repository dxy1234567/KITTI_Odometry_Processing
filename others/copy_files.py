import os
import shutil
import sys
sys.path.append(".")
from utils.util import print_progress

src_dir = "/data/KITTI/data_odometry_gray/dataset/sequences/"  # 源目录
dst_to_dir = "/data/KITTI_to_DC/"  # 目标目录

for i in range(11):
    dir_img = os.path.join(src_dir, "{:02d}".format(i), "image_0")
    dir_dst = os.path.join(dst_to_dir, "{:02d}".format(i), "gray")

    for filename in os.listdir(dir_img):
        path_img = os.path.join(dir_img, filename)
        if os.path.isfile(path_img):  # 仅复制文件
            shutil.copy(path_img, dir_dst)
    print(i)



# 遍历源目录下的所有文件

