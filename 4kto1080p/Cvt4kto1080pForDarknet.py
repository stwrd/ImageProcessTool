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

classes = ["qizhongji","wajueji","dazhuangji"]

#4k图像被划分为大小为size的grid[0]*grid[1]个子图像，子图像间存在重叠
#size为子图像的大小
#grid(X,Y)表示x方向上子图像为x个，y方向上子图像为y个
def split4K(img_4k,size,grid=(3,3)):
    stride_y = (img_4k.shape[0] - size[1])/(grid[1]-1)#图像的步进
    stride_y = np.floor(stride_y).astype('int')
    stride_x = (img_4k.shape[1] - size[0])/(grid[0]-1)
    stride_x = np.floor(stride_x).astype('int')
    images = []
    for x in range(0,img_4k.shape[1]-size[0] + stride_x,stride_x):
        for y in range(0,img_4k.shape[0]-size[1] + stride_y,stride_y):
            roi = img_4k[y:y+size[1],x:x+size[0],:]
            offset = (x,y)
            images.append({'image':roi,'offset':offset})
    return images

def cvtJsonToDarknet(img_file,label_file,size,grid=(3,3)):
    img_4k = cv2.imread(img_file)
    roiImages = split4K(img_4k,size,grid=grid)

    if os.path.exists(label_file):
        with open(label_file) as f:
            data = json.load(f)
            labels = []
            for shape in data['shapes']:
                if shape['shape_type'] != 'rectangle':
                    print('Skipping shape: label={label}, shape_type={shape_type}'
                          .format(**shape))
                    continue

                class_name = shape['label']
                class_id = classes.index(class_name)
                pt1, pt2 = shape['points']
                pt1 = np.array(pt1).astype('int')
                pt2 = np.array(pt2).astype('int')

                # 调换位置(左上，右下）
                if pt1[0] > pt2[0]:
                    pt1[0],pt2[0] = pt2[0],pt1[0]
                if pt1[1] > pt2[1]:
                    pt1[1],pt2[1] = pt2[1],pt1[1]
                if np.sum(np.array([class_id,pt1[0],pt1[1],pt2[0]-pt1[0],pt2[1]-pt1[1]]) < 0) > 0:
                    print(np.array([class_id,pt1[0],pt1[1],pt2[0]-pt1[0],pt2[1]-pt1[1]]))
                labels.append(np.array([class_id,pt1[0],pt1[1],pt2[0]-pt1[0],pt2[1]-pt1[1]]))#(id,x,y,wh,h)
            labels = np.array(labels)
    else:
        labels = np.empty([0])

    for roiObj in roiImages:
        offset = roiObj['offset']
        correct_label = filter_labels(labels,offset,size,0.4)
        roiObj['label'] = correct_label
    return roiImages

#利用小图在大图中的相对偏移，将出界的标签过滤掉
def filter_labels(labels, offset, size, threshold = 0.6):
    rect = np.array([0,0,*size])
    correct_labels = []
    for i,label in enumerate(labels):
        c_x,c_y = label[1:3] - np.array(offset)
        real_rect = np.array([c_x,c_y,*label[3:]])
        iou = overlap_to_target(real_rect,rect)
        if iou > threshold:
            c_width = label[3]
            c_height = label[4]
            if c_x < 0:
                c_width = c_width + c_x
                c_x = 0
            if c_y < 0:
                c_height = c_height + c_y
                c_y = 0
            if c_x+c_width > size[0]:
                c_width = size[0] - c_x
            if c_y + c_height > size[1]:
                c_height = size[1] - c_y
            c_label = np.array([label[0], c_x, c_y, c_width, c_height])
            correct_labels.append(c_label)
    return np.array(correct_labels)

#rect a 与目标rect b的重叠部分所占的a的比例
def overlap_to_target(a,b):
    if (a[0] > b[0] + b[2]):
        return 0
    if (a[1] > b[1] + b[3]):
        return 0
    if (a[0]+a[2] < b[0]):
        return 0
    if (a[1]+a[3] < b[1]):
        return 0
    colInt =  min(a[0]+a[2], b[0]+b[2]) - max(a[0], b[0])
    rowInt =  min(a[1]+a[3], b[1]+b[3]) - max(a[1],b[1])
    intersection = colInt * rowInt
    return intersection/(a[2]*a[3])


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

if __name__ == '__main__':
    input_path = r'H:\hangpai\image\001'
    output_path = r'E:\workspace\data\remote_sensing_data\data'
    os.makedirs(output_path,exist_ok=True)
    tar_str = os.path.join(input_path,'*.jpg')
    file_list = glob.glob(tar_str)

    size = (1920,1080)
    idx = 1
    for file_name in file_list:
        print('process ',file_name)
        json_name = file_name.replace('.jpg', '.json')
        basename = os.path.splitext(os.path.split(file_name)[1])[0]

        darknet_obj = cvtJsonToDarknet(file_name, json_name, size, grid=(3, 3))
        for obj in darknet_obj:
            img = obj['image'].copy()
            offset = obj['offset']
            label = obj['label']
            img_out_name = os.path.join(output_path, '{}_{}_{}.jpg'.format(basename, offset[0], offset[1]))
            txt_out_name = os.path.join(output_path, '{}_{}_{}.txt'.format(basename, offset[0], offset[1]))
            out_file = open(txt_out_name, 'w')

            for b in label:
                bb = convert(size,np.array([b[1],b[3]+b[1],b[2],b[4]+b[2]]))#np.array([b[1],b[3]+b[1],b[2],b[4]+b[2]]) --->[xmin,xmax,ymin,ymax]
                # test show
                # cv2.rectangle(img, (b[1],b[2]),(b[3]+b[1],b[4]+b[2]),(0,255,0),2)
                out_file.write(str(b[0]) + " " + " ".join([str(a) for a in bb]) + '\n')
            #     print(b)
            #     print('label:',bb)
            # print('--------------------------------------------')
            # cv2.namedWindow('tt')
            # cv2.imshow('tt',img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            out_file.close()
            cv2.imwrite(img_out_name,img)
