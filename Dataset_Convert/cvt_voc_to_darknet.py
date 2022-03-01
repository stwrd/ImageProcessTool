import xml.etree.ElementTree as ET
import pickle
import os
import numpy as np
from pathlib import Path
import sys
#{'people': 152710, 's_smoke': 488, 's_phone': 427, 'smoke': 916, 'phone': 6619, 'smoke_phone': 150}
# classes = ["clothes","hat","mound","bulldozer","drill","excavator","roadblock","fence"] #穿反光衣 clothes,带安全帽 hat,土堆 mound,小型推土机 bulldozer,小型钻机 drill,挖掘机 excavator,雪糕筒 roadblock,围栏 fence
# classes = ["people","s_smoke","s_phone","smoke","smoke_phone","phone","person","somke_phone","smoke_s_phone","s_smoke_s_phone","phone_s_smoke"]

# classes = ["excavator","crane","rig","driver"] #挖掘机，起重机，钻机，打桩机
# classes = ['zebra crossing','left turn', 'right turn','straight','straight&left','straight&right','u-turn']
# classes = ["vehicle","belt","phone","people"]  #开车不系安全带和打手机
classes = ["car",
"truck",
"bus",
"non_motor",
"people",
"motor",
"plate",
"straight",
"straight_r",
"straight_l",
"right",
"left",
"stop_line",
"zebra",
"road_block"]

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

def convert_annotation(img_filename,xml_file_name):

    out_name = img_filename.replace(os.path.splitext(img_filename)[1], '.txt')

    if os.path.exists(xml_file_name):
        in_file = open(xml_file_name,encoding='utf-8')
        parser = ET.XMLParser(encoding='utf-8')
        tree=ET.parse(in_file,parser=parser)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        out_file = open(out_name, 'w')
        if w == 0 or h == 0:
            out_file.close()
            return -1
        else:
            for obj in root.iter('object'):
                if ET.iselement(obj.find('bndbox')):
                    cls = obj.find('name').text
                    if cls not in classes:
                        print('invalid label:',cls)
                        raise('invalid label')
                        continue
                    cls_id = classes.index(cls)

                    xmlbox = obj.find('bndbox')
                    b = np.array([float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)])
                    x1 = b[0]
                    y1 = b[2]
                    x2 = b[1]
                    y2 = b[3]
                    if x1 >= w or y1 >= h:
                        print('label {} {} {} {} truncated'.format(x1, y1, x2, y2))
                        continue
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(w, x2), min(h, y2)
                    bb = convert((w,h), (x1,x2,y1,y2))
                    out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                    # out_file.write(str(0) + " " + " ".join([str(a) for a in bb]) + '\n')
                    # if cls_id > 0:
                    #     out_file.write(str(0) + " " + " ".join([str(a) for a in bb]) + '\n')
                    # else:
                    #     out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            out_file.close()
            # tree.write(xml_file_name)
    else:
        print('xml file not exist:{}'.format(xml_file_name))
        out_file = open(out_name, 'w')
        out_file.close()

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
    img_path = '/media/hzh/docker_disk/dataset/traffic/交通违法第一次通用标注/Annotations'#这里填目标图片路径
    pattern_list = ['*.jpg', '*.png']
    with open('/media/hzh/docker_disk/dataset/traffic/error_list.txt','w') as f:
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