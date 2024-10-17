import imageio
import os
import sys
sys.path.append(".")

from utils.util import print_progress

gif = []
# 存放多张测试图片的路径拼接
dir_images = "/root/data/output/for_com_gif/"
# 获取该文件夹内的全部文件
list_files = sorted(os.listdir(dir_images))
N = len(list_files)
i = 0
for filename in list_files:
    file_path = os.path.join(dir_images, filename)
    gif.append(imageio.imread(file_path))
    i += 1
    print_progress(i, N)
path_output = "/root/data/output/gif_projection/com_projection.gif"
# 生成GIF图
imageio.mimsave(path_output, gif, fps=40)	# fps值越大，生成的gif图播放就越快