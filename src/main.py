import sys
sys.path.append(".")
import yaml
import os
from utils.functions import get_image_dimensions
from combined_pcd import combine_pcd
from projection import project, generate_depth_gt, generate_depth
from utils.util import read_config
from src.bin_to_depth import bin_to_depth, bin_to_com_depth

def main():
    # path_to_yaml = ""
    # read_config(path_to_yaml)

    # with open(path_to_yaml, "r") as file:
    #     config = yaml.safe_load(file)

    # directory_combined_pcd = config["directory_combined_pcd"]   # 直接对拼接好的点云组进行操作
    # directory_pcd = config["directory_pcd"]
    # # directory_pcd = config["directory_pcd_"]
    # directory_image = config["directory_image"]
    # path_odom = config["path_odom"]
    # path_calib = config["path_calib"]

    # directory_output_com = config["directory_output_com"]
    # directory_output_pro = config["directory_output_pro"]
    # directory_output_depth = config["directory_output_depth"]
    # directory_output_com_depth = config["directory_output_com_depth"]

    dir_to_pcd_bin = "/data/KITTI/data_odometry_velodyne/dataset/sequences/"
    dir_to_img = "/data/KITTI_to_DC/"
    dir_to_poses = "/data/KITTI/data_odometry_poses/dataset/poses/"
    dir_to_calib = "/data/KITTI/data_odometry_calib/dataset/sequences/"
    dir_to_depth = "/data/KITTI_to_DC/"

    height, width = get_image_dimensions(dir_to_img)

    for i in range(1, 2):
        dir_pcd_bin = os.path.join(dir_to_pcd_bin, "{:02d}".format(i), "velodyne")
        path_pose = os.path.join(dir_to_poses, "{:02d}.txt".format(i))
        path_calib = os.path.join(dir_to_calib, "{:02d}".format(i), "calib.txt")

        dir_output_depth = os.path.join(dir_to_depth, "{:02d}".format(i), "depth")
        dir_output_depth_gt = os.path.join(dir_to_depth, "{:02d}".format(i), "depth_gt")

        # bin_to_depth(height, width, dir_pcd_bin, path_calib, dir_output_depth)
        bin_to_com_depth(height, width, dir_pcd_bin, path_pose, path_calib, dir_output_depth_gt)

        # combine_pcd(dir_pcd_bin, path_pose, path_calib, dir_output_com)
        # generate_depth(height, width, dir_depth, path_calib, dir_depth)
        # generate_depth_gt(height, width, dir_output_com, path_calib, dir_depth_gt)
        
        print("***********************\nSequnce {} done.\n***********************\n\n\n".format(i))





    # combine_pcd(directory_pcd, directory_image, path_odom, path_calib, directory_output_com)

    # project(directory_combined_pcd, directory_image, path_odom, path_calib, directory_output_pro)

    # generate_depth(directory_combined_pcd, directory_image, path_calib, directory_output_com_depth)



if __name__ == "__main__":
    main()
