#提取cvat数据
import cv2
from xml.etree.cElementTree import parse
import json
import os
import numpy as np
import shutil

classname_2_idx = {"car":0,
"truck":1,
"bus":2,
"non_motor":3,
"people":4,
"motor":5,
"plate":6,
"straight":7,
"straight_right":8,
"straight_left":9,
"right":10,
"left":11,
"stop_line":12,
"zebra":13,
"road_block":14}

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
    # class, x, y, theta, length, attrib,sharpness,aspect
    xml_file_path = '/media/hzh/docker_disk/dataset/traffic/交通违法2020年12月版通用数据/traffic_common_detect.xml'
    darknet_label_path = '/media/hzh/docker_disk/dataset/traffic/交通违法2020年12月版通用数据/darknetlabel/data'
    doc = parse(xml_file_path)
    public_folder = os.path.split(xml_file_path)[0]

    root = doc.getroot()
    label_file = {}
    target_list = []
    max_limit = 1000
    save_num = 1
    start_order = 1
    lane_line_attrib_id = {}
    for image_item in root.iterfind('image'):
        image_path = image_item.attrib['name']
        width = float(image_item.attrib['width'])
        height = float(image_item.attrib['height'])
        print('process ',image_path)
        image = cv2.imread(os.path.join(public_folder,image_path))
        if image is None:
            continue

        out_name = image_path.replace(os.path.splitext(image_path)[1], '.txt')
        out_name = os.path.join(darknet_label_path,out_name)
        os.makedirs(os.path.split(out_name)[0],exist_ok=True)
        out_file = open(out_name, 'w')
        for box_item in image_item.iterfind('box'):
            # print(box_item.attrib)
            cls_id = classname_2_idx[box_item.attrib['label']]
            x1 = float(box_item.attrib['xtl'])
            y1 = float(box_item.attrib['ytl'])
            x2 = float(box_item.attrib['xbr'])
            y2 = float(box_item.attrib['ybr'])
            bb = convert((width,height),(x1,x2,y1,y2))
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        out_file.close()

        #是否复制图像
        new_image_path = os.path.join(darknet_label_path,image_path)
        shutil.copy(os.path.join(public_folder,image_path),new_image_path)
