#分割交通违法数据集
import os
import numpy as np
import shutil
from PIL import Image
from PIL import ImageFile
str_dict = ['_a','_b','_c','_d']
def split_img(big_img, grid = (2,2)):
    stride_y = big_img.height/grid[1]#图像的步进
    stride_y = np.floor(stride_y).astype('int')
    stride_x = big_img.width/grid[0]
    stride_x = np.floor(stride_x).astype('int')
    images = []
    for x in range(0,stride_x*grid[0],stride_x):
        for y in range(0,stride_y*grid[1],stride_y):
            try:
                roi = big_img.crop((x,y,x+stride_x,y+stride_y))
            except IOError:
                print('OSError: broken data stream when reading image file')
            else:
                images.append(roi)
    return images

def isvalid_symbol(code):
    if ord(code) >=32 and ord(code) <=122:
        return True
    else:
        return False
tar_path = '/media/hzh/work/data/wuxi_new_data1'
dst_path = '/media/hzh/ssd_disk/Traffic/split_data_1213_1'


# tar_path = '/media/hzh/No.7/全国一百支队违法数据/sample200'
subfolders1 = [ os.path.join(tar_path,subfolder) for subfolder in os.listdir(tar_path) if os.path.isdir(os.path.join(tar_path,subfolder))]
for subfolder1 in subfolders1:
    subfolders2 = [os.path.join(subfolder1,subfolder) for subfolder in os.listdir(subfolder1) if os.path.isdir(os.path.join(subfolder1,subfolder)) and ('1345' in subfolder or '1208' in subfolder or '1301' in subfolder)]#1345
    for subfolder2 in subfolders2:
        # print(subfolder2)
        # shutil.copytree(subfolder2,os.path.join('/media/hzh/work/data/wuxi_new_data1',os.path.split(subfolder1)[1],os.path.split(subfolder2)[1]))
        subfolders3 = os.listdir(subfolder2)
        for subfolder3 in subfolders3:
            full_path = os.path.join(subfolder2,subfolder3)
            if os.path.isdir(full_path):
                filenames = os.listdir(full_path)
                os.makedirs(os.path.join(dst_path, os.path.split(subfolder2)[1]), exist_ok=True)
                for filename in filenames:
                    basename = os.path.splitext(filename)[0]
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
                                new_basename = new_basename.replace(target_str, 'null_')
                                invalid_len = 0

                    old_name = os.path.join(full_path, filename)
                    if os.path.isdir(old_name):
                        continue
                    print('process ',old_name)
                    if subfolder3 == 'dantu1' or subfolder3 == 'dantu2' or subfolder3 == 'dantu3':
                        new_name = os.path.join(dst_path, os.path.split(subfolder2)[1], new_basename + '.jpg')
                        if len(filenames) > 300:
                            if np.random.random() < 0.1:
                                shutil.copy(old_name,new_name)
                        else:
                            shutil.copy(old_name, new_name)
                    elif subfolder3 == 'shang2xia2':
                        if len(filenames) > 100:
                            if np.random.random() < 0.1:
                                try:
                                    big_img = Image.open(old_name)
                                except IOError:
                                    continue
                                else:
                                    image_2_2 = split_img(big_img, (2, 2))
                                    for i,img in enumerate(image_2_2):
                                        new_name = os.path.join(dst_path, os.path.split(subfolder2)[1], new_basename + str_dict[i] + '.jpg')
                                        img.save(new_name)
                        else:
                            try:
                                big_img = Image.open(old_name)
                            except IOError:
                                continue
                            else:
                                image_2_2 = split_img(big_img, (2, 2))
                                for i,img in enumerate(image_2_2):
                                    new_name = os.path.join(dst_path, os.path.split(subfolder2)[1], new_basename + str_dict[i] + '.jpg')
                                    img.save(new_name)
                    elif subfolder3 == 'zuo1you1':
                        if len(filenames) > 100:
                            if np.random.random() < 0.1:
                                try:
                                    big_img = Image.open(old_name)
                                except IOError:
                                    continue
                                else:
                                    image_2_2 = split_img(big_img, (2, 1))
                                    for i,img in enumerate(image_2_2):
                                        new_name = os.path.join(dst_path, os.path.split(subfolder2)[1], new_basename + str_dict[i] + '.jpg')
                                        img.save(new_name)
                        else:
                            try:
                                big_img = Image.open(old_name)
                            except IOError:
                                continue
                            else:
                                image_2_2 = split_img(big_img, (2, 1))
                                for i,img in enumerate(image_2_2):
                                    new_name = os.path.join(dst_path, os.path.split(subfolder2)[1], new_basename + str_dict[i] + '.jpg')
                                    img.save(new_name)
                    elif subfolder3 == 'shang1xia1':
                        if len(filenames) > 100:
                            if np.random.random() < 0.1:
                                try:
                                    big_img = Image.open(old_name)
                                except IOError:
                                    continue
                                else:
                                    image_2_2 = split_img(big_img, (1, 2))
                                    for i,img in enumerate(image_2_2):
                                        new_name = os.path.join(dst_path, os.path.split(subfolder2)[1], new_basename + str_dict[i] + '.jpg')
                                        img.save(new_name)
                        else:
                            try:
                                big_img = Image.open(old_name)
                            except IOError:
                                continue
                            else:
                                image_2_2 = split_img(big_img, (1, 2))
                                for i, img in enumerate(image_2_2):
                                    new_name = os.path.join(dst_path, os.path.split(subfolder2)[1],
                                                            new_basename + str_dict[i] + '.jpg')
                                    img.save(new_name)
                    elif subfolder3 == 'heng3he1':
                        if len(filenames) > 100:
                            if np.random.random() < 0.3:
                                try:
                                    big_img = Image.open(old_name)
                                except IOError:
                                    continue
                                else:
                                    image_2_2 = split_img(big_img, (3, 1))
                                    for i,img in enumerate(image_2_2):
                                        new_name = os.path.join(dst_path, os.path.split(subfolder2)[1], new_basename + str_dict[i] + '.jpg')
                                        img.save(new_name)
                        else:
                            try:
                                big_img = Image.open(old_name)
                            except IOError:
                                continue
                            else:
                                image_2_2 = split_img(big_img, (3, 1))
                                for i, img in enumerate(image_2_2):
                                    new_name = os.path.join(dst_path, os.path.split(subfolder2)[1],
                                                            new_basename + str_dict[i] + '.jpg')
                                    img.save(new_name)
                    elif subfolder3 == 'shu3he1':
                        if len(filenames) > 100:
                            if np.random.random() < 0.3:
                                try:
                                    big_img = Image.open(old_name)
                                except IOError:
                                    continue
                                else:
                                    image_2_2 = split_img(big_img, (1, 3))
                                    for i,img in enumerate(image_2_2):
                                        new_name = os.path.join(dst_path, os.path.split(subfolder2)[1], new_basename + str_dict[i] + '.jpg')
                                        img.save(new_name)
                        else:
                            try:
                                big_img = Image.open(old_name)
                            except IOError:
                                continue
                            else:
                                image_2_2 = split_img(big_img, (1, 3))
                                for i, img in enumerate(image_2_2):
                                    new_name = os.path.join(dst_path, os.path.split(subfolder2)[1],
                                                            new_basename + str_dict[i] + '.jpg')
                                    img.save(new_name)
