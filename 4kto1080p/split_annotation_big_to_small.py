# -*- coding: utf8 -*-
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import glob
import json
import numpy as np
import cv2
import copy

classes = ["qizhongji","wajueji","dazhuangji"]

#图像被划分为大小为size的grid[0]*grid[1]个子图像，子图像间存在重叠
#size为子图像的大小
#stride(X,Y)表示x方向上，y方向上进进
def splitBigImg(big_img,size,stride):
    stride_x = stride[0]
    stride_y = stride[1]
    images = []
    for x in range(0,big_img.shape[1] - size[0] + stride_x,stride_x):
        for y in range(0,big_img.shape[0] - size[1] + stride_y,stride_y):
            roi = big_img[y:y+size[1],x:x+size[0],:]
            offset = (x,y)
            images.append({'image':roi,'offset':offset})
    return images

def splitJsonToSmall(img_file,label_file,out_path,size,stride=(720,450)):
    img_4k = cv2.imread(img_file)
    roiImages = splitBigImg(img_4k,size,stride)
    os.makedirs(out_path,exist_ok=True)
    basename = os.path.split(img_file)[1]
    basename = os.path.splitext(basename)[0]

    with open(label_file) as f:
        data = json.load(f)
        shapes = data['shapes']

    for i,roiImage in enumerate(roiImages):
        image, offset = roiImage['image'],roiImage['offset']
        save_name_json = os.path.join(out_path, '{}_{}.json'.format(basename, i))
        save_name_jpg = os.path.join(out_path, '{}_{}.jpg'.format(basename, i))
        new_json_data = {"version": data["version"],
                         "flags": data["flags"],
                         "imagePath": save_name_jpg,
                         "imageData": data["imageData"],
                         "imageHeight": image.shape[0],
                         "imageWidth": image.shape[1]}
        new_shapes = []
        for shape in shapes:
            init_img = np.zeros(image.shape[:2], dtype=np.uint8)
            points = copy.deepcopy(shape['points'])
            for point in points:
                point[0] = int(point[0]-offset[0])
                point[1] = int(point[1]-offset[1])

            mask = labelme.utils.shape_to_mask(init_img.shape,points)
            init_img[mask] = 255
            contours,_ = cv2.findContours(init_img,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
            if len(contours) == 0:
                continue
            new_shape = {'label':shape['label'],
                         'line_color':shape['line_color'],
                         'fill_color':shape['fill_color'],
                         'shape_type':shape['shape_type'],
                         'flags':shape['flags']}
            new_points = contours[0].reshape(-1,2).tolist()
            new_shape['points'] = new_points
            new_shapes.append(new_shape)
        new_json_data['shapes'] = new_shapes

        cv2.imwrite(save_name_jpg,image)

        with open(save_name_json,'w') as f:
            json.dump(new_json_data,f)
    return roiImages

import labelme
def draw_mask(img,label_file):
    if os.path.exists(label_file):
        with open(label_file) as f:
            data = json.load(f)
            img_shape = img.shape
            for shape in data['shapes']:
                if shape['shape_type'] != 'polygon':
                    print('Skipping shape: label={label}, shape_type={shape_type}'
                          .format(**shape))
                    continue
                mask = labelme.utils.shape_to_mask(img_shape,shape["points"])
                img[mask] = 255
    return img

# #利用小图在大图中的相对偏移，将出界的标签过滤掉
# def filter_labels(labels, offset, size, threshold = 0.6):
#     rect = np.array([0,0,*size])
#     correct_labels = []
#     for i,label in enumerate(labels):
#         c_x,c_y = label[1:3] - np.array(offset)
#         real_rect = np.array([c_x,c_y,*label[3:]])
#         iou = overlap_to_target(real_rect,rect)
#         if iou > threshold:
#             c_width = label[3]
#             c_height = label[4]
#             if c_x < 0:
#                 c_width = c_width + c_x
#                 c_x = 0
#             if c_y < 0:
#                 c_height = c_height + c_y
#                 c_y = 0
#             if c_x+c_width > size[0]:
#                 c_width = size[0] - c_x
#             if c_y + c_height > size[1]:
#                 c_height = size[1] - c_y
#             c_label = np.array([label[0], c_x, c_y, c_width, c_height])
#             correct_labels.append(c_label)
#     return np.array(correct_labels)

if __name__ == '__main__':
    input_path = r'/media/hzh/work/workspace/mmdetection/data/src_data'
    output_path = r'/media/hzh/work/workspace/mmdetection/data/coco_split1'
    os.makedirs(output_path,exist_ok=True)
    tar_str = os.path.join(input_path,'*.png')
    file_list = glob.glob(tar_str)

    size = (1920,1080)
    idx = 1
    for file_name in file_list:
        print('process ',file_name)
        json_name = file_name.replace('.png', '.json')
        basename = os.path.splitext(os.path.split(file_name)[1])[0]
        darknet_obj = splitJsonToSmall(file_name, json_name,output_path,size,stride=(960,540))
