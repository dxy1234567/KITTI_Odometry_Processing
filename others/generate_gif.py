import os
import cv2
import imageio

def create_gif_from_folder(image_folder, output_gif, duration=0.5, resize=None):
    """
    将文件夹中的图像按顺序生成 GIF 动画。
    
    :param image_folder: 存储图像的文件夹路径
    :param output_gif: 生成的 GIF 文件路径
    :param duration: 每帧持续时间（单位：秒），默认为 0.5 秒
    :param resize: 如果指定，图像将被调整为指定的大小 (width, height)，默认为 None
    """
    # 获取文件夹中的所有图像文件，并按名称排序
    image_files = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if img.endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff'))]
    
    # 使用 imageio 创建 GIF
    with imageio.get_writer(output_gif, mode='I', duration=duration) as writer:
        for img_path in image_files:
            image = imageio.imread(img_path)
            
            # 如果提供了 resize 参数，调整图像大小
            if resize:
                image = imageio.core.util.Array(image)  # 将其转回 numpy 数组
                image = cv2.resize(image, resize)  # 使用 OpenCV 来调整尺寸
            
            writer.append_data(image)
    
    print(f"GIF 已生成: {output_gif}")

# 使用示例
image_folder = '/root/ChenJiasheng/Low_Illuminated_Depth_Completion/output/gml_udgd_stacked'  # 替换为你的图像文件夹路径
output_gif = 'output.gif'  # 输出 GIF 的路径
create_gif_from_folder(image_folder, output_gif, duration=0.03, resize=(848, 1920))


