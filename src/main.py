from combined_pcd import combine_pcd
from projection import project, generate_depth_gt, generate_depth_normal
import yaml
import os

def main():
    with open("cfg/configure.yaml", "r") as file:
        config = yaml.safe_load(file)

    directory_combined_pcd = config["directory_combined_pcd"]   # 直接对拼接好的点云组进行操作
    directory_pcd = config["directory_pcd"]
    # directory_pcd = config["directory_pcd_"]
    directory_image = config["directory_image"]
    path_odom = config["path_odom"]
    path_calib = config["path_calib"]

    directory_output_com = config["directory_output_com"]
    directory_output_pro = config["directory_output_pro"]
    directory_output_depth = config["directory_output_depth"]
    directory_output_com_depth = config["directory_output_com_depth"]

    dir_to_pcd_bin = "/data/KITTI/data_odometry_velodyne/dataset/sequences/"
    dir_to_img = "/data/KITTI_to_DC/"
    dir_to_poses = "/data/KITTI/data_odometry_poses/dataset/poses/"
    dir_to_calib = "/data/KITTI/data_odometry_calib/dataset/sequences/"
    dir_to_depth = "/data/KITTI_to_DC/"

    for i in range(11):
        dir_pcd_bin = os.path.join(dir_to_pcd_bin, "{:02d}".format(i), "velodyne")
        dir_img = os.path.join(dir_to_img, "{:02d}".format(i), "gray")
        path_pose = os.path.join(dir_to_poses, "{:02d}.txt".format(i))
        path_calib = os.path.join(dir_to_calib, "{:02d}".format(i), "calib.txt")

        dir_output_com = "/data/KITTI_to_DC/tmp/"
        dir_depth = os.path.join(dir_to_depth, "{:02d}".format(i), "depth")
        dir_depth_gt = os.path.join(dir_to_depth, "{:02d}".format(i), "depth_gt")

        combine_pcd(dir_pcd_bin, dir_img, path_pose, path_calib, dir_output_com)
        generate_depth_normal(dir_output_com, dir_img, path_calib, dir_depth)
        generate_depth_gt(dir_output_com, dir_img, path_calib, dir_depth_gt)
        
        print("----------\nSequnce {} done.\n----------".format(i))





    # combine_pcd(directory_pcd, directory_image, path_odom, path_calib, directory_output_com)

    # project(directory_combined_pcd, directory_image, path_odom, path_calib, directory_output_pro)

    # generate_depth(directory_combined_pcd, directory_image, path_calib, directory_output_com_depth)



if __name__ == "__main__":
    main()
