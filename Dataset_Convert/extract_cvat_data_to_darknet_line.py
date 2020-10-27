#提取cvat数据
import cv2
from xml.etree.cElementTree import parse
import json
import os
import numpy as np


classname_2_idx = {'lane_line':0,'stop_line':1,'zebra':2,'channelization_line':3,'center_barrier':4}
class LaneLine:
    def __init__(self):
        self.class_id = classname_2_idx['lane_line']
        #实线(solid)、虚线(broken)、双黄线(double_yellow)、左虚右实(broken_solid_line)、左实右虚(solid_broken_line)
        self.typename2id = {'solid':0, 'broken':1, 'double_yellow':2, 'broken_solid_line':3, 'solid_broken_line':4}
        #清晰(high)、一般(middle)、不清晰(low)
        self.sharpness2id = {'high':0,'middle':1,'low':2}
class StopLine:
    def __init__(self):
        self.class_id = classname_2_idx['stop_line']
        self.sharpness2id = {'high':0,'middle':1,'low':2}
class Zebra:
    def __init__(self):
        self.class_id = classname_2_idx['zebra']
        #上边界(upper_boundary)、下边界(lower_boundary)、左边界(left_boundary)、右边界(right_boundary)
        self.typename2id = {'upper_boundary':0, 'lower_boundary':1, 'left_boundary':2, 'right_boundary':3}
        self.sharpness2id = {'high': 0, 'middle': 1, 'low': 2}
        #横向(horizontal)、纵向(vertical)
        self.aspect2id = {'horizontal':0,'vertical':1}
class ChannelizationLine:
    def __init__(self):
        self.class_id = classname_2_idx['channelization_line']
        #上边界(upper_boundary)、下边界(lower_boundary)、左边界(left_boundary)、右边界(right_boundary)
        self.typename2id = {'upper_boundary':0, 'lower_boundary':1, 'left_boundary':2, 'right_boundary':3}
        self.sharpness2id = {'high': 0, 'middle': 1, 'low': 2}
class CenterBarrier:
    def __init__(self):
        self.class_id = classname_2_idx['center_barrier']
        #横向(horizontal)、纵向(vertical)
        self.aspect2id = {'horizontal':0,'vertical':1}

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x1 = box[0]*dw
    x2 = box[1]*dw
    y1 = box[2]*dh
    y2 = box[3]*dh
    return (x1,y1,x2,y2)

if __name__ == '__main__':
    # class, x, y, theta, length, attrib,sharpness,aspect
    xml_file_path = '/media/hzh/ssd_disk/Traffic/Dataset/trafficdata_multiple_attr/JTWFnewdata20200721p1.xml'
    darknet_label_path = '/media/hzh/ssd_disk/Traffic/Dataset/trafficdata_multiple_attr/darknetlabel/data'
    doc = parse(xml_file_path)
    public_folder = os.path.split(xml_file_path)[0]

    root = doc.getroot()
    label_file = {}
    target_list = []
    max_limit = 1000
    save_num = 1
    start_order = 33
    lane_line_attrib_id = {}
    for image_item in root.iterfind('image'):
        image_path = image_item.attrib['name']
        print('process ',image_path)
        image = cv2.imread(os.path.join(public_folder,image_path))
        if image is None:
            continue

        out_name = image_path.replace(os.path.splitext(image_path)[1], '.txt')
        out_name = os.path.join(darknet_label_path,out_name)
        os.makedirs(os.path.split(out_name)[0],exist_ok=True)
        out_file = open(out_name, 'w')
        for box_item in image_item.iterfind('polyline'):
            # print(box_item.attrib)
            label = box_item.attrib['label']
            attrib = 0
            sharpness = 0
            aspect = 0

            points = box_item.attrib['points']
            part_pts = points.split(';')
            if len(part_pts) < 2:
                continue
            pt1, pt2 = part_pts[0],part_pts[1]
            x1, y1 = pt1.split(',')
            x2, y2 = pt2.split(',')
            x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
            # 调换位置(左，右）
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            x1, y1, x2, y2 = x1/image.shape[1],y1/image.shape[0],x2/image.shape[1],y2/image.shape[0]
            x1 = max(min(1,x1),0)
            x2 = max(min(1,x2), 0)
            y1 = max(min(1,y1),0)
            y2 = max(min(1,y2), 0)
            # class, x1, y1, x2, y2, attrib,sharpness,aspect
            if label == 'lane_line':
                for attrib_item in box_item.iterfind('attribute'):
                    attrib_name = attrib_item.attrib['name']
                    attrib_label = attrib_item.text
                    if attrib_name == 'type':
                        attrib = LaneLine().typename2id[attrib_label]
                    if attrib_name == 'sharpness' or attrib_name == 'shapness':
                        sharpness = LaneLine().sharpness2id[attrib_label]
                class_id = LaneLine().class_id
                out_file.write(str(class_id) + " " + " ".join([str(x1),str(y1),str(x2),str(y2),str(attrib),str(sharpness),str(aspect)]) + '\n')

            if label == 'stop_line':
                for attrib_item in box_item.iterfind('attribute'):
                    attrib_name = attrib_item.attrib['name']
                    attrib_label = attrib_item.text
                    if attrib_name == 'sharpness' or attrib_name == 'shapness':
                        sharpness = StopLine().sharpness2id[attrib_label]
                class_id = StopLine().class_id
                out_file.write(str(class_id) + " " + " ".join([str(x1),str(y1),str(x2),str(y2),str(attrib),str(sharpness),str(aspect)]) + '\n')

            if label == 'zebra':
                for attrib_item in box_item.iterfind('attribute'):
                    attrib_name = attrib_item.attrib['name']
                    attrib_label = attrib_item.text
                    if attrib_name == 'type':
                        attrib = Zebra().typename2id[attrib_label]
                    if attrib_name == 'sharpness' or attrib_name == 'shapness':
                        sharpness = Zebra().sharpness2id[attrib_label]
                    if attrib_name == 'aspect':
                        aspect = Zebra().aspect2id[attrib_label]
                        # print(aspect)
                class_id = Zebra().class_id
                out_file.write(str(class_id) + " " + " ".join([str(x1),str(y1),str(x2),str(y2),str(attrib),str(sharpness),str(aspect)]) + '\n')

            # if label == 'center_barrier':
            #     for attrib_item in box_item.iterfind('attribute'):
            #         attrib_name = attrib_item.attrib['name']
            #         attrib_label = attrib_item.text
            #         if attrib_name == 'aspect':
            #             aspect = CenterBarrier().aspect2id[attrib_label]
            #     class_id = CenterBarrier().class_id
            #     out_file.write(str(class_id) + " " + " ".join([str(x1),str(y1),str(x2),str(y2),str(attrib),str(sharpness),str(aspect)]) + '\n')

            if label == 'channelization_line':
                for attrib_item in box_item.iterfind('attribute'):
                    attrib_name = attrib_item.attrib['name']
                    attrib_label = attrib_item.text
                    if attrib_name == 'type':
                        attrib = ChannelizationLine().typename2id[attrib_label]
                    if attrib_name == 'sharpness' or attrib_name == 'shapness':
                        sharpness = ChannelizationLine().sharpness2id[attrib_label]
                class_id = ChannelizationLine().class_id
                out_file.write(str(class_id) + " " + " ".join([str(x1),str(y1),str(x2),str(y2),str(attrib),str(sharpness),str(aspect)]) + '\n')
        out_file.close()
