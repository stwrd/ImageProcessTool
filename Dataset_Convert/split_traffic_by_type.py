#按照合成模式分类，相同合成模式的放入同一个文件夹
#分割交通违法数据集
import os
import numpy as np
import shutil
from PIL import Image
from PIL import ImageFile

def search_all_folder(input_path):
    totalfolders = []
    for root,dirs,files in os.walk(input_path):
        totalfolders.append(root)
    return totalfolders

tar_path = '/media/hzh/docker_disk/sample200'
dst_path = '/media/hzh/docker_disk/hcms'


subfolders = search_all_folder(tar_path)
for subfolder in subfolders:
    if 'dantu' in os.path.split(subfolder)[1]:
        print('copy {} to {}'.format(subfolder,subfolder.replace(tar_path, dst_path)))
        shutil.copytree(subfolder, subfolder.replace(tar_path, dst_path))