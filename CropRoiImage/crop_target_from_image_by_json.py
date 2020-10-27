#获取标注的roi图像
import xml.etree.ElementTree as ET
import os
import glob
import cv2
import numpy as np
import sys
from pathlib import Path
import json
# classes = ["smoke","people","head","person","phone","smoke_phone"]
classes = ["people","s_smoke","s_phone","smoke","smoke_phone","somke_phone","phone"]
# classes = ["car","truck","spercial"]
# classes = ["right turn","left turn","straight","straight&left","straight&right","left&right","u-turn"]
# classes = ["vehicle","belt","phone","people"]

def convert_annotation(img_filename,xml_file_name,dst_path):
    if os.path.exists(xml_file_name):
        with open(xml_file_name) as f:
            data = json.load(f)
            w = int(data['imageWidth'])
            h = int(data['imageHeight'])
            if w == 0 or h == 0:
                print('invalid json file')
                return -1
            img_idx = 1
            img = cv2.imread(img_filename)
            if img is None:
                return
            rows, cols = img.shape[0], img.shape[1]
            for shape in data['shapes']:
                if shape['shape_type'] != 'rectangle':
                    print('Skipping shape: label={label}, shape_type={shape_type}'.format(**shape))
                    continue
                class_name = shape['label']
                if class_name not in classes:
                    continue
                pt1, pt2 = shape['points']
                pt1 = np.array(pt1).astype('int')
                pt2 = np.array(pt2).astype('int')

                # 调换位置(左上，右下）
                if pt1[0] > pt2[0]:
                    pt1[0], pt2[0] = pt2[0], pt1[0]
                if pt1[1] > pt2[1]:
                    pt1[1], pt2[1] = pt2[1], pt1[1]

                b = np.array([float(pt1[0]), float(pt2[0]), float(pt1[1]), float(pt2[1])]).astype('int')
                x1, y1, x2, y2 = b[0], b[2], b[1], b[3]
                box_w = (x2 - x1)
                box_h = (y2 - y1)
                if box_w >= 32 and box_h >= 32:
                    roi_img = img[y1:y2, x1:x2]
                    full_name = os.path.join(dst_path, class_name, basename + '_%02d' % img_idx + '.jpg')
                    img_idx += 1
                    if roi_img.shape[0] > 0 and roi_img.shape[1] > 0:
                        cv2.imwrite(full_name, roi_img)

if __name__ == '__main__':
    img_path = '/media/hzh/ssd_disk/smoke_and_call/标注数据-人头检测/SHJGsmoke20200819done'
    dst_path = '/media/hzh/ssd_disk/smoke_and_call/tmp'
    for c in classes:
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