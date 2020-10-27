#获取标注的roi图像
import xml.etree.ElementTree as ET
import os
import glob
import cv2
import numpy as np
import sys
from pathlib import Path

# classes = ["smoke","people","head","person","phone","smoke_phone"]
classes = ["people","s_smoke","s_phone","smoke","smoke_phone","somke_phone","phone"]
# classes = ["car","truck","spercial"]
# classes = ["right turn","left turn","straight","straight&left","straight&right","left&right","u-turn"]
# classes = ["vehicle","belt","phone","people"]

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
        for obj in root.iter('object'):
            if ET.iselement(obj.find('bndbox')):
                cls = obj.find('name').text
                if cls not in classes:
                    continue
                xmlbox = obj.find('bndbox')
                b = np.array([float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)]).astype('int')
                x1,y1,x2,y2 = b[0],b[2],b[1],b[3]
                center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                box_w = (x2 - x1)
                box_h = (y2 - y1)
                if box_w >= 64 and box_h >= 64:
                    l = max(60, max(box_w, box_h))
                    x1, y1, x2, y2 = max(int(center_x - np.floor(l * 3 / 4)), 0), max(int(center_y - np.floor(l / 2)),0), \
                                     min(int(center_x + np.ceil(l * 3 / 4)), img.shape[1]), min(int(center_y + np.ceil(l)),img.shape[0])
                    # l = max(60, max(box_w, box_h))
                    # x1, y1, x2, y2 = max(int(center_x - np.floor(l * 3 / 4)), 0), max(int(center_y - np.floor(l / 2)),
                    #                                                                   0), min(
                    #     int(center_x + np.ceil(l * 3 / 4)), img.shape[1]), min(int(center_y + l),
                    #                                                            img.shape[0])
                    # x1, y1, x2, y2 = max(int(center_x - l), 0), max(int(center_y - l), 0), min(int(center_x + l),img.shape[1]), min(int(center_y + l), img.shape[0])
                    roi_img = img[y1:y2,x1:x2]
                    full_name = os.path.join(dst_path,cls,basename + '_%02d' %img_idx + '.jpg')
                    img_idx += 1
                    if roi_img.shape[0] > 0 and roi_img.shape[1] > 0:
                        cv2.imwrite(full_name,roi_img)

                # #交通违法识别中，需要筛选出地面区域
                # if b[3] > rows//2:
                #     roi_img = img[b[2]:b[3],b[0]:b[1]]
                #     full_name = os.path.join(dst_path,cls,basename + '_%02d' %img_idx + '.jpg')
                #     cv2.imwrite(full_name,roi_img)

                    # h = (b[3] - b[2]) // 5
                    # r = 1
                    # bb1 = b[0], b[1], max(b[2] - r * h, 0), min(b[3]+r*h,cols-1)
                    # roi_img = img[bb1[2]:bb1[3],bb1[0]:bb1[1]]
                    # full_name = os.path.join(dst_path,cls,basename + '_%02d' %img_idx + '.jpg')
                    # cv2.imwrite(full_name,roi_img)

                    # h = (b[3]-b[2])//5
                    # r = 1
                    # bb1 = b[0],b[1],max(b[2]-r*h,0),b[2]+h
                    # bb2 = b[0],b[1],b[3]-h,min(b[3]+r*h,cols-1)
                    # roi_img1 = img[bb1[2]:bb1[3], bb1[0]:bb1[1]]
                    # full_name1 = os.path.join(dst_path, cls, basename + '_%02d_t' % img_idx + '.jpg')
                    # roi_img2 = img[bb2[2]:bb2[3], bb2[0]:bb2[1]]
                    # full_name2 = os.path.join(dst_path, cls, basename + '_%02d_b' % img_idx + '.jpg')
                    # cv2.imwrite(full_name1, roi_img1)
                    # cv2.imwrite(full_name2, roi_img2)

if __name__ == '__main__':
    img_path = '/media/hzh/ssd_disk/smoke_and_call/标注数据-人头检测/KSTsp20200909_done'
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