import open3d as o3d
import numpy as np
import os
import sys
import yaml
import time
sys.path.append(".")

from utils.functions import get_point_cloud, read_odom, odom_to_R_t, read_pcd_list, read_image_list, read_calib, R_t_to_T
from utils.util import print_progress


def combine_pcd(directory_pcd, directory_image, path_odom, path_calib, directory_output):
    odom_lists = read_odom(path_odom)
    pcd_lists = read_pcd_list(directory_pcd)
    image_lists = read_image_list(directory_image)

    _, R, t = read_calib(path_calib)
    T_CL = R_t_to_T(R, t)

    N = min(len(pcd_lists), len(image_lists))

    start_time = time.time()
    print("----------------Combining begins----------------")
    for i in range(5, N - 5):
        combined_pcd = o3d.geometry.PointCloud()
        filename = os.path.basename(pcd_lists[i])
        filename = filename.replace(".bin", ".pcd")
        T, _, _ = odom_to_R_t(odom_lists, i)    ### 
        T_CW = np.linalg.inv(T)                 ####

        for j in range(i - 5, i + 5):
            
            pcd = get_point_cloud(pcd_lists[j])

            T_WC, _, _ = odom_to_R_t(odom_lists, j)

            T_WL = T_WC @ T_CL 

            pcd.transform(T_WL)

            combined_pcd += pcd

        combined_pcd.transform(T_CW)

        path = os.path.join(directory_output, filename)
        o3d.io.write_point_cloud(path, combined_pcd)

        print_progress(i, N)
    print("----------------End of Combining----------------")
    end_time = time.time()
    dur_time = end_time - start_time
    print("Combining spends {}s.".format(dur_time))
    







