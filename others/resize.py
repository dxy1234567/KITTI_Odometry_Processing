import cv2
import os
import sys
sys.path.append('.')
from utils.util import *

def crop_images_in_folder(input_folder, output_folder, target_width=1216, target_height=352):
    """
    对文件夹中的所有图片进行中心剪裁，并保存到指定输出文件夹。

    Args:
        input_folder (str): 输入图片文件夹路径。
        output_folder (str): 输出图片文件夹路径。
        target_width (int): 剪裁后图像的宽度。
        target_height (int): 剪裁后图像的高度。
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    def center_crop(img, target_width, target_height):
        """对单张图片进行中心剪裁。"""
        height, width = img.shape[:2]
        center_x, center_y = width // 2, height // 2
        crop_x1 = max(center_x - target_width // 2, 0)
        crop_x2 = min(center_x + target_width // 2, width)
        crop_y1 = max(center_y - target_height // 2, 0)
        crop_y2 = min(center_y + target_height // 2, height)
        return img[crop_y1:crop_y2, crop_x1:crop_x2]

    imgs_list = os.listdir(input_folder)

    N = len(imgs_list)
    # 遍历文件夹中的所有图片
    for idx, filename in enumerate(imgs_list):
        input_path = os.path.join(input_folder, filename)

        # 确保文件是图片
        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # img = cv2.imread(input_path)
            img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

            # 检查是否成功加载图片
            if img is None:
                print(f"无法读取文件: {filename}, 跳过...")
                continue

            # 中心剪裁
            cropped_img = center_crop(img, target_width, target_height)

            # 保存到输出文件夹
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, cropped_img)

            print(f"已处理并保存: {filename}")
            print_progress(idx, N)


dir_img = '/data/KITTI_to_DC/dataset_1_frames/'
dir_output = '/data/KITTI_to_DC/dataset_1_frames_cropped'

os.makedirs(dir_output, exist_ok=True)
# 调用函数

folders_set = os.listdir(dir_img)
# 遍历每个子集 e.g. train, test, val
for folder in folders_set:
    folder1 = os.path.join(dir_img, folder)
    folder2 = os.path.join(dir_output, folder)
    os.makedirs(folder2, exist_ok=True)
    folders_img = os.listdir(folder1)

    print(f'------------------------------------{folder} Begins------------------------------------')

    N = len(folders_img)
    for idx, f in enumerate(folders_img):
        folder_img = os.path.join(folder1, f)
        folder_img_output = os.path.join(folder2, f)
        os.makedirs(folder_img_output, exist_ok=True)

        crop_images_in_folder(folder_img, folder_img_output)
    

    print(f'------------------------------------{folder} Ends------------------------------------')
    

          
