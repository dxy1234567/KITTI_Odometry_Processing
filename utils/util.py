import yaml

def print_progress(i, N):
    """
    打印当前进度。

    Params:
        i: 当前进度（第i次迭代）
        N: 总迭代次数
    """
    if i % 100 == 0 or i == N:  # 每 100 次迭代或最后一次迭代时更新进度
        run = i / N * 100
        print("Runing: {:.2f}% done.".format(run))

def print_time(start_time, end_time):
    dur_time = end_time - start_time

    hours = int(dur_time // 3600)
    minutes = int((dur_time % 3600) // 60)
    seconds = round(dur_time % 60, 2)  # 保留两位小数

    if hours > 0:
        print("It takes {}h {}min {:.2f}s.".format(hours, minutes, seconds))
    else:
        print("It takes {}min {:.2f}s.".format(minutes, seconds))

def read_config(path_to_yaml):
    with open(path_to_yaml, "r") as file:
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