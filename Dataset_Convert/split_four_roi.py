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
ImageFile.LOAD_TRUNCATED_IMAGES = True

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

father_folder = r'/media/hzh/work/data/7.13测试数据/百色数据-7.13整理/1625'
dst_folder = r'/media/hzh/work/data/7.13测试数据/百色数据-7.13整理/1625_new'

path_list = os.listdir(father_folder)
for sub_path in path_list:
    new_path = os.path.join(dst_folder,sub_path)#新的子目录路径
    os.makedirs(new_path,exist_ok=True)
    full_path = os.path.join(father_folder,sub_path)
    filename_list = [os.path.join(full_path,filename) for filename in os.listdir(full_path) if filename.endswith('.jpg')]
    idx = 1
    for filename in filename_list:
        big_img = Image.open(filename)
        images = split_img(big_img,grid=(1,1))

        folder,name = os.path.split(filename)
        basename = os.path.splitext(name)[0]
        new_basename = basename
        target_str = None
        invalid_len = 0
        for c in basename:
            if not isvalid_symbol(c):
                if invalid_len == 0:
                    target_str = c
                else:
                    target_str = target_str + c
                invalid_len += 1
            else:
                if invalid_len != 0:
                    new_basename = new_basename.replace(target_str,'null_')
                    invalid_len = 0

        str_dict = ['_1','_2','_3','_4']
        for i,image in enumerate(images):
            new_save_path = os.path.join(new_path,new_basename+str_dict[i]+'.jpg')
            print(idx,' save to ',new_save_path)
            image.save(new_save_path)
        idx+=1

