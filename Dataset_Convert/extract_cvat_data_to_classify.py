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
    max_limit = 1000
    start_order = 0
    # class, x, y, theta, length, attrib,sharpness,aspect
    level = ['high','middle','low']
    save_num = {'high':0,
                'middle':0,
                'low':0}#分别记录每一类的保存数量

    xml_file_path = '/media/hzh/ssd_disk/Traffic/Dataset/trafficdata_multiple_attr'
    classify_data_path = '/media/hzh/ssd_disk/Traffic/Dataset/trafficdata_multiple_attr/line_classify/data1'
    for l in level:
        os.makedirs(os.path.join(classify_data_path,l),exist_ok=True)

    filelist = os.listdir(xml_file_path)
    xml_filelist = [os.path.join(xml_file_path,filename) for filename in filelist if filename.endswith('.xml')]
    public_folder = xml_file_path

    for xml_file in xml_filelist:
        doc = parse(xml_file)
        root = doc.getroot()
        for image_item in root.iterfind('image'):
            image_path = image_item.attrib['name']
            print('process ',image_path)
            image = cv2.imread(os.path.join(public_folder,image_path))
            if image is None:
                continue
            image_folder, image_name = os.path.split(image_path)
            image_basename = os.path.splitext(image_name)[0]
            sub_idx = 0
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
                # 转换为左上右下表达形式
                if x1 > x2:
                    x1, x2 = x2, x1
                if y1 > y2:
                    y1, y2 = y2, y1
                if x2-x1 < 1:
                    x1 -= 2
                    x2 += 2
                if y2 - y1 < 1:
                    y1-=2
                    y2+=2
                x1 = max(min(image.shape[1],x1),0)
                x2 = max(min(image.shape[1],x2), 0)
                y1 = max(min(image.shape[0],y1),0)
                y2 = max(min(image.shape[0],y2), 0)

                # class, x1, y1, x2, y2, attrib,sharpness,aspect
                if label == 'lane_line':
                    sharpness_label = ''
                    type_label = ''
                    for attrib_item in box_item.iterfind('attribute'):
                        attrib_name = attrib_item.attrib['name']
                        attrib_label = attrib_item.text
                        if attrib_name == 'type':
                            type_label = attrib_label
                        if attrib_name == 'sharpness' or attrib_name == 'shapness':
                            sharpness_label = attrib_label
                    if type_label in ['solid','double_yellow','broken_solid_line','solid_broken_line']:
                        save_num[sharpness_label] += 1
                        sub_idx += 1
                        target_img = image[int(y1):int(y2),int(x1):int(x2),:]
                        label_path = os.path.join(classify_data_path,sharpness_label)
                        order_folder = int(np.ceil(save_num[sharpness_label] / max_limit)) + start_order
                        image_save_path_1 = os.path.join(label_path, '{:0>4}'.format(order_folder))
                        os.makedirs(image_save_path_1, exist_ok=True)
                        sub_img_path = os.path.join(image_save_path_1, image_basename + '_{:0>3}.jpg'.format(sub_idx))
                        if target_img.shape[0] > 224 or target_img.shape[1] > 224:
                            long_resize_ratio = 224./max(target_img.shape[0],target_img.shape[1])
                            new_w = int(np.ceil(long_resize_ratio*target_img.shape[1]))
                            new_h = int(np.ceil(long_resize_ratio*target_img.shape[0]))
                            if target_img.shape[0] > 4 and target_img.shape[1] > 4:
                                target_img = cv2.resize(target_img,(new_w,new_h))
                        if (target_img.shape[0] > 100 or target_img.shape[1] > 100) and (target_img.shape[0] > 4 and target_img.shape[1] > 4):
                            cv2.imwrite(sub_img_path,target_img)
                if label == 'channelization_line':
                    for attrib_item in box_item.iterfind('attribute'):
                        attrib_name = attrib_item.attrib['name']
                        attrib_label = attrib_item.text
                        if attrib_name == 'sharpness' or attrib_name == 'shapness':
                            save_num[attrib_label] += 1
                            sub_idx += 1
                            target_img = image[int(y1):int(y2),int(x1):int(x2),:]
                            label_path = os.path.join(classify_data_path,attrib_label)
                            order_folder = int(np.ceil(save_num[attrib_label] / max_limit)) + start_order
                            image_save_path_1 = os.path.join(label_path, '{:0>4}'.format(order_folder))
                            os.makedirs(image_save_path_1, exist_ok=True)
                            sub_img_path = os.path.join(image_save_path_1, image_basename + '_{:0>3}.jpg'.format(sub_idx))
                            if target_img.shape[0] > 224 or target_img.shape[1] > 224:
                                long_resize_ratio = 224. / max(target_img.shape[0], target_img.shape[1])
                                new_w = int(np.ceil(long_resize_ratio * target_img.shape[1]))
                                new_h = int(np.ceil(long_resize_ratio * target_img.shape[0]))
                                target_img = cv2.resize(target_img, (new_w, new_h))
                                if target_img.shape[0] > 4 and target_img.shape[1] > 4:
                                    target_img = cv2.resize(target_img, (new_w, new_h))
                            if (target_img.shape[0] > 100 or target_img.shape[1] > 100) and (
                                    target_img.shape[0] > 4 and target_img.shape[1] > 4):
                                cv2.imwrite(sub_img_path, target_img)
