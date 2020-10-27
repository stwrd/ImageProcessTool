#提取cvat数据
import cv2
from xml.etree.cElementTree import parse
import json
import os
import numpy as np
xml_file_path = '/media/hzh/ssd_disk/Traffic/Dataset/trafficdata_multiple_attr/JTWFnewdata20200721p1.xml'
doc = parse(xml_file_path)
public_folder = os.path.split(xml_file_path)[0]
image_save_path = os.path.join(public_folder,'car_classify')
os.makedirs(image_save_path,exist_ok=True)

root = doc.getroot()
label_file = {}
target_list = []
max_limit = 1000
save_num = 1
start_order = 33

for image_item in root.iterfind('image'):
    image_path = image_item.attrib['name']
    image = cv2.imread(os.path.join(public_folder,image_path))
    if image is None:
        continue
    sub_idx = 1
    for box_item in image_item.iterfind('box'):
        print(box_item.attrib)
        label = box_item.attrib['label']
        if label == 'car':#仅保存车的数据
            bbox = np.array([float(box_item.attrib['xtl']),float(box_item.attrib['ytl']),float(box_item.attrib['xbr']),float(box_item.attrib['ybr'])],np.int32)
            image_folder,image_name = os.path.split(image_path)
            image_basename = os.path.splitext(image_name)[0]

            order_folder = int(np.ceil(save_num/max_limit)) + start_order
            image_save_path_1 = os.path.join(image_save_path, '{:0>4}'.format(order_folder))
            os.makedirs(image_save_path_1,exist_ok=True)
            sub_img_path = os.path.join(image_save_path_1,image_basename+'_{:0>3}.jpg'.format(sub_idx))
            sub_json_path = os.path.join(image_save_path_1, image_basename + '_{:0>3}.json'.format(sub_idx))
            sub_idx += 1
            sub_img = image[bbox[1]:bbox[3],bbox[0]:bbox[2],:]
            sub_json = {'img_path':sub_img_path}
            for attrib_item in box_item.iterfind('attribute'):
                attrib_name = attrib_item.attrib['name']
                attrib_label = attrib_item.text
                sub_json[attrib_name] = attrib_label
            print(sub_json)
            if sub_img.shape[0] <=30 or sub_img.shape[1] <= 30:
                continue
            print(sub_img.shape)
            cv2.imwrite(sub_img_path,sub_img)
            with open(sub_json_path,'w') as f:
                json.dump(sub_json,f)
            save_num +=1
