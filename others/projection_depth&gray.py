"""
    在已经得到深度图和灰度图的情况下，将深度图相应的点覆盖到灰度图上，以查看投影情况。
"""
import os
import numpy as np
import cv2
import sys
sys.path.append('.')
from utils.util import *

def get_color(cur_depth, max_depth, min_depth):
    scale = (max_depth - min_depth) / 10
    if cur_depth < min_depth:
        return (255, 0, 0)  # 返回红色
    elif cur_depth < min_depth + scale:
        green = int((cur_depth - min_depth) / scale * 165)
        return (255, green, 0)  # 返回红到橙的渐变色
    elif cur_depth < min_depth + scale * 2:
        green = int((cur_depth - min_depth - scale) / scale * 255)
        return (255, green, 0)  # 返回橙到黄的渐变色
    elif cur_depth < min_depth + scale * 4:
        red = int(255 - (cur_depth - min_depth - scale * 2) / scale * 255)
        return (red, 255, 0)  # 返回黄到绿的渐变色
    elif cur_depth < min_depth + scale * 7:
        blue = int((cur_depth - min_depth - scale * 4) / scale * 255)
        return (0, 255, blue)  # 返回绿到青的渐变色
    elif cur_depth < min_depth + scale * 10:
        red = int((cur_depth - min_depth - scale * 7) / scale * 255)
        return (0, 255 - red, 255)  # 返回青到蓝的渐变色
    else:
        return (128, 0, 128)  # 返回紫色

def projection(dir_depths, dir_grays, dir_output):
    os.makedirs(dir_output, exist_ok=True)

    depths_list = sorted(os.listdir(dir_depths))
    grays_list = sorted(os.listdir(dir_grays))

    N = len(depths_list)
    assert N == len(grays_list), "深度图和灰度图数量不匹配"

    for idx, (depth, gray) in enumerate(zip(depths_list, grays_list)):
        path_depth = os.path.join(dir_depths, depth)
        path_gray = os.path.join(dir_grays, gray)

        img_depth = cv2.imread(path_depth, cv2.IMREAD_UNCHANGED)  # 确保读取深度图为原始值
        img_gray = cv2.imread(path_gray, cv2.IMREAD_GRAYSCALE)  # 读取灰度图

        if img_depth is None:
            print(f"[{idx}] 无法读取深度图像: {depth}")
            continue
        if img_gray is None:
            print(f"[{idx}] 无法读取灰度图像: {gray}")
            continue

        # 创建灰度图的副本
        gray_copy = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

        # 获取深度图的最大值
        max_depth = np.max(img_depth)
        
        # 归一化深度图并转换为 0-255 范围
        if max_depth > 0:
            img_depth = img_depth / max_depth * 255.0
            img_depth = np.uint8(img_depth)

        # 遍历深度图像素，若不为 0 则覆盖到 gray_copy 中
        for i in range(img_depth.shape[0]):
            for j in range(img_depth.shape[1]):
                if img_depth[i, j] != 0:
                    cur_depth = get_color(img_depth[i, j], 255, 0)
                    gray_copy[i, j] = cur_depth

        # 保存结果
        output_path = os.path.join(dir_output, f"output_{idx}.png")
        cv2.imwrite(output_path, gray_copy)
        print_progress(idx, N)
        print(f"[{idx}] 图像已保存: {output_path}")

dir_depths = '/data/gml_to_DC/04/depth_gt/'
dir_grays = '/data/gml_to_DC/04/gray/'
dir_output = 'output/projection_gt_04'

projection(dir_depths, dir_grays, dir_output)

