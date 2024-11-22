import cv2
import os

def resize_images_in_place(folder_path, target_size=(1216, 352)):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 确保处理的是图片文件
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            
            # 检查是否成功读取图片
            if img is None:
                print(f"无法读取文件 {img_path}")
                continue
            
            # 调整分辨率
            img_resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)
            
            # 保存调整后的图片，覆盖原文件
            cv2.imwrite(img_path, img_resized)
            print(f"{filename} 已调整并覆盖原文件")

resize_images_in_place('.')
