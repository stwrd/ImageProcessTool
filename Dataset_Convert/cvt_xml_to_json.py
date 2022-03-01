import xml.etree.ElementTree as ET
import pickle
import os
import numpy as np
from pathlib import Path
import sys
import json

classes = ['smoke','s_smoke','people','smoke_part']

def convert_annotation(img_filename,xml_file_name):
    out_name = img_filename.replace(os.path.splitext(img_filename)[1], '.json')
    if os.path.exists(xml_file_name):
        in_file = open(xml_file_name,encoding='utf-8')
        parser = ET.XMLParser(encoding='utf-8')
        tree=ET.parse(in_file,parser=parser)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        new_json_data = {"imagePath": img_filename,
                         "imageHeight": h,
                         "imageWidth": w}

        if w != 0 and h != 0:
            shape_data = []
            for obj in root.iter('object'):
                if ET.iselement(obj.find('bndbox')):
                    cls = obj.find('name').text
                    if cls not in classes:
                        print('invalid label')
                        continue
                    xmlbox = obj.find('bndbox')
                    new_shape = {"label":cls,
                                 "shape_type": "rectangle",
                                 "points":[[float(xmlbox.find('xmin').text),float(xmlbox.find('ymin').text)],
                                           [float(xmlbox.find('xmax').text),float(xmlbox.find('ymax').text)]]
                                 }
                    shape_data.append(new_shape)
            if len(shape_data) != 0:
                new_json_data["shapes"] = shape_data
            with open(out_name,'w') as f:
                json.dump(new_json_data,f,indent=4, separators=(',', ':'))

def check_voc_label(xml_path):
    labels = {}
    if os.path.exists(xml_path):
        in_file = open(xml_path,encoding='utf-8')
        parser = ET.XMLParser(encoding='utf-8')
        tree=ET.parse(in_file,parser=parser)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            if ET.iselement(obj.find('bndbox')):
                cls = obj.find('name').text
                if cls in labels.keys():
                    labels[cls] += 1
                else:
                    labels[cls] = 1
                # if cls not in labels:
                #     labels.append(cls)
    return labels

def check_labels_in_folder(input_path):
    total_labels = {}
    for xml_path in Path(input_path).rglob('*.xml'):
        labels = check_voc_label(xml_path)
        for key in labels:
            if key in total_labels.keys():
                total_labels[key] += labels[key]
            else:
                total_labels[key] = labels[key]
    return total_labels

import json
if __name__ == '__main__':
    img_path = '/media/hzh/ssd_disk/smoke_and_call/Annotation'
    pattern_list = ['*.jpg', '*.png']
    with open('/media/hzh/ssd_disk/smoke_and_call/error_list.txt','w') as f:
        for pattern_str in pattern_list:
            filenames = Path(img_path).rglob(pattern_str)
            for img_filename in filenames:
                print('process ', img_filename)
                basename = img_filename.name
                xml_filename = basename.replace(pattern_str[1:],'.xml')
                xml_filename = img_filename.parent.joinpath(xml_filename)
                res = convert_annotation(img_filename.as_posix(),xml_filename.as_posix())
                if res == -1:
                    f.writelines(img_filename.as_posix()+'\n')