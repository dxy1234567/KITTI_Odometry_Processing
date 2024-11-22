import numpy as np
import cv2
import os
import sys
sys.path.append('.')
from utils.util import *

def get_color(cur_depth, max_depth, min_depth):
    scale = (max_depth - min_depth) / 10
    if cur_depth < min_depth:
        return (255, 0, 0)  # 红色
    elif cur_depth < min_depth + scale:
        green = int((cur_depth - min_depth) / scale * 165)
        return (255, green, 0)  # 红到橙的渐变
    elif cur_depth < min_depth + scale * 2:
        green = int((cur_depth - min_depth - scale) / scale * 255)
        return (255, green, 0)  # 橙到黄的渐变
    elif cur_depth < min_depth + scale * 4:
        red = int(255 - (cur_depth - min_depth - scale * 2) / scale * 255)
        return (red, 255, 0)  # 黄到绿的渐变
    elif cur_depth < min_depth + scale * 7:
        blue = int((cur_depth - min_depth - scale * 4) / scale * 255)
        return (0, 255, blue)  # 绿到青的渐变
    elif cur_depth < min_depth + scale * 10:
        red = int((cur_depth - min_depth - scale * 7) / scale * 255)
        return (0, 255 - red, 255)  # 青到蓝的渐变
    else:
        return (128, 0, 128)  # 紫色

def depth_to_color(dir_imgs, dir_output):
    os.makedirs(dir_output, exist_ok=True)

    depths_list = os.listdir(dir_imgs)
    
    N = len(depths_list)
    for idx, depth in enumerate(depths_list):
        path_depth = os.path.join(dir_imgs, depth)

        # 读取深度图像
        image_depth = cv2.imread(path_depth, cv2.IMREAD_UNCHANGED).astype(np.float32)

        # 检查图像是否正确加载
        if image_depth is None:
            print(f"[{idx}] 无法读取图像: {path_depth}")
            continue

        # 获取深度图的最大和最小值
        max_depth = np.max(image_depth)
        min_depth = np.min(image_depth[image_depth > 0])  # 忽略零值

        # 将灰度图转换为三通道以便进行彩色覆盖
        image_copy = cv2.cvtColor(image_depth, cv2.COLOR_GRAY2BGR)

        # 应用颜色映射
        for i in range(image_depth.shape[0]):
            for j in range(image_depth.shape[1]):
                if image_depth[i, j] != 0:
                    color = get_color(image_depth[i, j], max_depth, min_depth)
                    image_copy[i, j] = color

        # 保存彩色图像
        path_output = os.path.join(dir_output, depth)
        cv2.imwrite(path_output, image_copy)
        print_progress(idx, N)


dir_imgs = '/data/gml_to_DC/02/depth/'
dir_output = 'output/gml_udgd_color'

depth_to_color(dir_imgs, dir_output)
