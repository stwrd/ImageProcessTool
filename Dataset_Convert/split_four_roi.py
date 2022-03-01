#将一个图片切成n等分，并重命名该图片
#交通违法的数据比较繁杂，没有标准形式，将数据分配一下，先把大图裁剪出小图，重命名，重命名时把中文替换成中文拼音，用下划线隔开，小图名称就是在原来基础上末尾加a,b,c,d等。
# 比如1310240300225204_131024000000010014_02_京QB59V8_20181128170413_1625_1_1.jpg，
# 变成1310240300225204_131024000000010014_02_jing_QB59V8_20181128170413_1625_1_1a.jpg,
# 1310240300225204_131024000000010014_02_jing_QB59V8_20181128170413_1625_1_1b.jpg等

import cv2
import os
import numpy as np
from PIL import Image
from PIL import ImageFile
from pathlib import Path
ImageFile.LOAD_TRUNCATED_IMAGES = True

split_mode = {'zuo1you1':(2,1),'shang1xia1':(1,2),'shang2xia2':(2,2),'shang3xia3':(3,2),'dantu':(1,1),'shang1zhong1xia1':(1,3)}
father_folder = r'/media/hzh/docker_disk/dataset/traffic/交通违法第四次标注/待标注数据已分类' #源路径
dst_folder = r'/media/hzh/docker_disk/dataset/traffic/交通违法第四次标注/test1' #目标路径

def match_hcms(full_path):
    hcms = (1,1)
    for key in split_mode:
        if key in full_path:
            hcms = split_mode[key]
    return hcms

def split_img(big_img, grid = (2,2)):
    stride_y = big_img.height/grid[1]#图像的步进
    stride_y = np.floor(stride_y).astype('int')
    stride_x = big_img.width/grid[0]
    stride_x = np.floor(stride_x).astype('int')
    images = []
    for x in range(0,stride_x*grid[0],stride_x):
        for y in range(0,stride_y*grid[1],stride_y):
            roi = big_img.crop((x,y,x+stride_x,y+stride_y))
            images.append(roi)
    return images

def isvalid_symbol(code):
    if ord(code) >=32 and ord(code) <=122:
        return True
    else:
        return False



p_father = Path(father_folder)
filename_list = p_father.rglob('*.jpg')
idx = 1
for filename in filename_list:
    filename = filename.as_posix()
    hcms = match_hcms(filename)
    big_img = Image.open(filename)
    images = split_img(big_img, grid=hcms)

    folder, name = os.path.split(filename)
    new_name = name
    target_str = None
    invalid_len = 0
    for c in name:
        if not isvalid_symbol(c):
            if invalid_len == 0:
                target_str = c
            else:
                target_str = target_str + c
            invalid_len += 1
        else:
            if invalid_len != 0:
                new_name = new_name.replace(target_str, 'null_')
                invalid_len = 0
    new_filename = os.path.join(folder,new_name)

    str_dict = ['_1', '_2', '_3', '_4','_5','_6']
    for i, image in enumerate(images):
        new_save_path = new_filename.replace(father_folder,dst_folder).replace('.jpg',str_dict[i]+'.jpg')
        os.makedirs(os.path.split(new_save_path)[0],exist_ok=True)
        print(idx, ' save to ', new_save_path)
        image.save(new_save_path)
    idx += 1

