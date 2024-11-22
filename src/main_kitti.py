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

    dir_pcd = '/data/KITTI/data_odometry_velodyne/dataset/sequences/'
    dir_DC = '/data/KITTI_to_DC'
    dir_calib = '/data/KITTI/data_odometry_calib/dataset/sequences/'    
    dir_odom = '/data/KITTI/data_odometry_poses/dataset/poses/'

    for sequence in range(4, 9):        
        print("***********************\nSequnce {} begins.\n***********************".format(sequence))

        dir_pcd_ = os.path.join(dir_pcd, '{:02d}'.format(sequence), 'velodyne')
        path_d = '/data/KITTI_to_DC/' + '{:02d}'.format(sequence) + '/depth'
        path_g = '/data/KITTI_to_DC/' + '{:02d}'.format(sequence) + '/depth_gt_81'
        path_gary = '/data/KITTI_to_DC/' + '{:02d}'.format(sequence) + '/gray'
        path_calib = os.path.join(dir_calib, '{:02d}'.format(sequence), 'calib.txt')
        path_odom = os.path.join(dir_odom, '{:02d}.txt'.format(sequence))
        height, width = get_image_dimensions(dir_DC, sequence)

        # bin_to_depth(height, width, dir_pcd_, path_calib, path_d)
        bin_to_n_com_depth(height, width, dir_pcd_, path_odom, path_calib, path_g, 40)

        print("***********************\nSequnce {} done.\n***********************\n\n\n".format(sequence))






if __name__ == "__main__":
    main()
