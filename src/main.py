from combined_pcd import combine_pcd
from projection import project, generate_depth
import yaml

def main():
    with open("cfg/configure.yaml", "r") as file:
        config = yaml.safe_load(file)

    directory_combined_pcd = config["directory_combined_pcd"]   # 直接对拼接好的点云组进行操作
    directory_pcd = config["directory_pcd"]
    directory_image = config["directory_image"]
    path_odom = config["path_odom"]
    path_calib = config["path_calib"]

    directory_output_com = config["directory_output_com"]
    directory_output_pro = config["directory_output_pro"]
    directory_output_depth = config["directory_output_depth"]

    combine_pcd(directory_pcd, directory_image, path_odom, path_calib, directory_output_com)

    project(directory_combined_pcd, directory_image, path_odom, path_calib, directory_output_pro)

    generate_depth(directory_combined_pcd, directory_image, path_odom, path_calib, directory_output_depth)


if __name__ == "__main__":
    main()
