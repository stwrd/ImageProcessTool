#转换cvat的关键点标注到labelme的标注格式
import cv2
from xml.etree.cElementTree import parse
import json
import os
import shutil
import numpy as np
xml_file_path = '/media/hzh/docker_disk/dataset/交通违法压线分类标注/small_yx/small_yx.xml'
doc = parse(xml_file_path)
public_folder = os.path.split(xml_file_path)[0]

root = doc.getroot()
label_file = {}
target_list = []
max_limit = 1000
save_num = 1
start_order = 1

def isvalid_symbol(code):
    if ord(code) >=32 and ord(code) <=122:
        return True
    else:
        return False

def strip_chinese_character(base_name):
    new_basename = ''
    for c in base_name:
        if isvalid_symbol(c):
            new_basename += c
    return new_basename

for image_item in root.iterfind('image'):
    image_path = image_item.attrib['name']
    image_width = int(image_item.attrib['width'])
    image_height = int(image_item.attrib['height'])
    image_folder, image_name = os.path.split(image_path)
    image_name = strip_chinese_character(image_name)
    image_path = os.path.join(image_folder,image_name)
    # image_basename = os.path.splitext(image_name)[0]
    image = cv2.imread(os.path.join(public_folder,image_path))
    json_path = os.path.join(public_folder,image_path).replace('.jpg','.json')
    if image is None:
        print('strip ',image_path)
        continue
    json_file = None

    for point_item in image_item.iterfind('points'):
        # print(point_item.attrib)
        label = point_item.attrib['label']
        points = point_item.attrib['points'].split(';')
        if len(points)  != 3:
            print('label maybe error:',image_path)
            error_folder = os.path.join(public_folder,'error_images')
            os.makedirs(error_folder,exist_ok=True)
            shutil.move(os.path.join(public_folder,image_path),os.path.join(error_folder,image_name))
            break
        point0 = points[0].split(',')
        point1 = points[1].split(',')
        point2 = points[2].split(',')
        point0[0],point0[1] = float(point0[0]),float(point0[1])
        point1[0],point1[1] = float(point1[0]),float(point1[1])
        point2[0],point2[1] = float(point2[0]),float(point2[1])
        json_file = {
            "shapes": [
            {"label": "yx",
             "points": [point0],
             "shape_type": "point",
             "flags": {}
             },
            {"label": "yx",
             "points": [point1],
             "shape_type": "point",
             "flags": {}
             },
            {"label": "yx",
             "points": [point2],
             "shape_type": "point",
             "flags": {}
             }
            ],
            "imagePath": image_path,
            "imageHeight": image_height,
            "imageWidth": image_width
            }
    if json_file is not None:
        with open(json_path, 'w') as f:
            json.dump(json_file, f,indent=2)
