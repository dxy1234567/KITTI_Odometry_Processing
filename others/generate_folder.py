import os

dir_dc = "/data/KITTI_to_DC/"

for item in os.listdir(dir_dc):
    dir_path = os.path.join(dir_dc, item)
    if os.path.isdir(dir_path):  # 检查是否为目录
        os.makedirs(os.path.join(dir_path, "gray"), exist_ok=True)
        os.makedirs(os.path.join(dir_path, "depth"), exist_ok=True)
        os.makedirs(os.path.join(dir_path, "depth_gt"), exist_ok=True)