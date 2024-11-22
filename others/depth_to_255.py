import numpy as np
import cv2
import os
import sys
sys.path.append('.')
from utils.util import *

def depth_to_255(dir_imgs, dir_output):
    os.makedirs(dir_output, exist_ok=True)

    imgs_list = os.listdir(dir_imgs)
    
    N = len(imgs_list)
    for idx, img in enumerate(imgs_list):
        path_img = os.path.join(dir_imgs, img)

        image = cv2.imread(path_img, cv2.IMREAD_UNCHANGED)
        
        # 获取图像的最大值并避免除以零
        max_image = np.max(image)
    
        image = image / max_image * 255.0
        image = np.uint8(image)

        path_output = os.path.join(dir_output, img)

        # 保存图像
        cv2.imwrite(path_output, image)
        print_progress(idx, N)


dir_imgs = '/data/gml_to_DC/04/depth/'
dir_output = '/data/gml/test_gt/'

depth_to_255(dir_imgs, dir_output)