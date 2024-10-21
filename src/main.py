from combined_pcd import combine_pcd
from projection import project
import yaml

def main():
    with open("cfg/configure.yaml", "r") as file:
        config = yaml.safe_load(file)

    directory_combined_pcd = config["directory_combined_pcd"]   # 直接对拼接好的点云组进行操作
    directory_pcd = config["directory_pcd"]
    directory_image = config["directory_image"]
    path_odom = config["path_odom"]
    path_calib = config["path_calib"]

    directory_output_com = config["path_output_com"]
    directory_output_pro = config["path_output_pro"]

    combine_pcd(directory_pcd, directory_image, path_odom, path_calib, directory_output_com)

    project(directory_combined_pcd, directory_image, path_odom, path_calib, directory_output_pro)


if __name__ == "__main__":
    main()
