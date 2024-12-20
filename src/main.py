import sys
sys.path.append(".")
import yaml
import os
from utils.functions import get_image_dimensions
from combined_pcd import combine_pcd
from projection import project, generate_depth_gt, generate_depth
from utils.util import read_config
from utils.new_func import *
from src.bin_to_depth import *
from src.pcd_to_depth import *

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

    dir_pcd = '/data/gml/20241025/gml_2024-10-25-15-59-06/_livox_lidar/'
    dir_DC = '/data/gml_to_DC'

    sequence = 0

    path_d = '/data/gml_to_DC/' + '{:02d}'.format(sequence) + '/depth'
    path_g = '/data/gml_to_DC/' + '{:02d}'.format(sequence) + '/depth_gt'
    path_gary = '/data/gml_to_DC/' + '{:02d}'.format(sequence) + '/gray'


    height, width = get_image_dimensions(dir_DC, sequence)

    pcd_to_depth(height, width, dir_pcd, path_d)
    # pcd_to_com_depth(height, width, dir_pcd, path_poses, path_g)

    # pcd_xt_to_mid_depth(height, width, dir_pcd, path_d)
    # pcd_xt_to_mid_com_depth(height, width, dir_pcd, path_poses, path_g)

    post_processing(path_d, path_g, path_gary)





if __name__ == "__main__":
    main()
