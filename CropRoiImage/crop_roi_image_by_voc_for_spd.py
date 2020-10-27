#获取标注的roi图像
import xml.etree.ElementTree as ET
import os
import glob
import cv2
import numpy as np
import sys
from pathlib import Path

# classes = ["smoke","people","head","person","phone","smoke_phone"]
# classes = ["people","s_smoke","s_phone","smoke","smoke_phone","somke_phone","phone"]
# classes = ["car","truck","spercial"]
# classes = ["right turn","left turn","straight","straight&left","straight&right","left&right","u-turn"]
classes = ["vehicle","belt","phone","people"]

def bbox_iou(box1, box2):
    b1_x1, b1_y1, b1_x2, b1_y2 = box1[0], box1[1], box1[2], box1[3]
    b2_x1, b2_y1, b2_x2, b2_y2 = box2[0], box2[1], box2[2], box2[3]

    # Intersection area
    inter_area = (min(b1_x2, b2_x2) - max(b1_x1, b2_x1)) * (min(b1_y2, b2_y2) - max(b1_y1, b2_y1))

    iou = inter_area / ((b2_x2-b2_x1)*(b2_y2-b2_y1))  # iou

    return iou

def convert_annotation(img_filename,xml_file_name,dst_path,limit_size=(32,32)):
    if os.path.exists(xml_filename):
        in_file = open(xml_file_name, encoding='utf-8')
        basename = os.path.splitext(os.path.split(xml_file_name)[1])[0]

        parser = ET.XMLParser(encoding='utf-8')
        tree=ET.parse(in_file,parser=parser)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w == 0 or h == 0:
            return -1

        img_idx = 1
        img = cv2.imread(img_filename)
        if img is None:
            return
        rows,cols = img.shape[0],img.shape[1]
        targets = {classes[0]:[],
                   classes[1]:[],
                   classes[2]:[],
                   classes[3]:[]}
        for obj in root.iter('object'):
            if ET.iselement(obj.find('bndbox')):
                cls = obj.find('name').text
                if cls not in classes:
                    continue
                xmlbox = obj.find('bndbox')
                b = np.array([float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)]).astype('int')
                x1,y1,x2,y2 = b[0],b[2],b[1],b[3]
                targets[cls].append([x1,y1,x2,y2])
        for people_box in targets["people"]:
            box_w,box_h = people_box[2] - people_box[0],people_box[3] - people_box[1]
            if box_w >= 150 and box_h >= 150:
                center_x, center_y = (people_box[0] + people_box[2]) // 2, (people_box[1] + people_box[3]) // 2
                l = max(box_w, box_h)
                x1, y1, x2, y2 = max(int(center_x - np.floor(l * 1 / 2)), 0), max(int(center_y - np.floor(l / 2)), 0), min(
                    int(center_x + np.ceil(l * 1 / 2)), img.shape[1]), min(int(center_y + np.ceil(l * 1 / 2)), img.shape[0])
                roi_img = img[y1:y2, x1:x2]
                label_name = {'not_seatbelt':0,'phone':1,}
                label = np.array([0,0],'int')
                for phone_box in targets["phone"]:
                    ratio = bbox_iou(people_box,phone_box)
                    if ratio > 0.7:
                        label[label_name['phone']] = 1
                not_found_seatbelt = True
                for belt_box in targets["belt"]:
                    ratio = bbox_iou(people_box,belt_box)
                    if ratio > 0.7:
                        not_found_seatbelt = False
                        break
                if not_found_seatbelt:
                    label[label_name['not_seatbelt']] = 1

                if label[label_name['not_seatbelt']] == 1 and label[label_name['phone']] == 1:
                    full_name = os.path.join(dst_path, "both", basename + '_%02d' % img_idx + '.jpg')
                    img_idx += 1
                    if roi_img.shape[0] > 0 and roi_img.shape[1] > 0:
                        cv2.imwrite(full_name, roi_img)
                elif label[label_name['not_seatbelt']] == 1 and label[label_name['phone']] == 0:
                    full_name = os.path.join(dst_path, "not_seatbelt", basename + '_%02d' % img_idx + '.jpg')
                    img_idx += 1
                    if roi_img.shape[0] > 0 and roi_img.shape[1] > 0:
                        cv2.imwrite(full_name, roi_img)
                elif label[label_name['not_seatbelt']] == 0 and label[label_name['phone']] == 1:
                    full_name = os.path.join(dst_path, "phone", basename + '_%02d' % img_idx + '.jpg')
                    img_idx += 1
                    if roi_img.shape[0] > 0 and roi_img.shape[1] > 0:
                        cv2.imwrite(full_name, roi_img)
                else:
                    full_name = os.path.join(dst_path, "normal", basename + '_%02d' % img_idx + '.jpg')
                    img_idx += 1
                    if roi_img.shape[0] > 0 and roi_img.shape[1] > 0:
                        cv2.imwrite(full_name, roi_img)
if __name__ == '__main__':
    img_path = '/media/hzh/ssd_disk/spd_data/Sbelt_phone20200615done'
    dst_path = '/media/hzh/ssd_disk/spd_data/step2'
    target_cls = ['normal','not_seatbelt','phone','both']
    for c in target_cls:
        sub_dir = os.path.join(dst_path,c)
        os.makedirs(sub_dir,exist_ok=True)
    pattern_list = ['*.jpg', '*.png']
    with open('/media/hzh/ssd_disk/process_list.txt','w') as f:
        for pattern_str in pattern_list:
            filenames = Path(img_path).rglob(pattern_str)
            for img_filename in filenames:
                print('process ', img_filename)
                basename = img_filename.name
                xml_filename = basename.replace(pattern_str[1:],'.xml')
                xml_filename = img_filename.parent.joinpath(xml_filename)
                res = convert_annotation(img_filename.as_posix(),xml_filename.as_posix(),dst_path)
                f.writelines(img_filename.as_posix()+'\n')