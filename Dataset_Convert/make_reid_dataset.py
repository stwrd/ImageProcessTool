#通过标注的xml文件生成reid数据集

import xml.etree.ElementTree as ET
import pickle
import os
import numpy as np
from pathlib import Path
import cv2
classes = ['car']

def convert_annotation(img_filename,xml_file_name,out_path):
    base_name = os.path.split(img_filename)[1]
    names = base_name.split('_')
    if os.path.exists(xml_file_name):
        src_img = cv2.imread(img_filename)
        if src_img is None:
            return -1
        in_file = open(xml_file_name,encoding='utf-8')
        parser = ET.XMLParser(encoding='utf-8')
        tree=ET.parse(in_file,parser=parser)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w == 0 or h == 0:
            in_file.close()
            return -1
        else:
            num_id = 1
            for obj in root.iter('object'):
                if ET.iselement(obj.find('bndbox')):
                    cls = obj.find('name').text
                    if cls not in classes:
                        print('invalid label')
                        continue
                    xmlbox = obj.find('bndbox')
                    b = np.array([float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)]).astype('int')
                    roi_img = src_img[b[2]:b[3],b[0]:b[1],:]
                    save_name = os.path.join(out_path,'{}_{}_reid{}.jpg'.format(names[1],names[0],num_id))
                    cv2.imwrite(save_name,roi_img)
                    num_id+=1
            if num_id == 1:
                in_file.close()
                return -1
            else:
                in_file.close()
                return 0


if __name__ == '__main__':
    img_path = '/media/hzh/work/workspace/fast-reid/datasets/vehicleid/image/reid_out_done'
    out_path = '/media/hzh/work/workspace/fast-reid/datasets/vehicleid/image/reid_out4'
    os.makedirs(out_path,exist_ok=True)
    pattern_list = ['*.jpg', '*.png']
    with open('/media/hzh/ssd_disk/error_list.txt','w') as f:
        for pattern_str in pattern_list:
            filenames = Path(img_path).rglob(pattern_str)
            for img_filename in filenames:
                print('process ', img_filename)
                basename = img_filename.name
                xml_filename = basename.replace(pattern_str[1:],'.xml')
                xml_filename = img_filename.parent.joinpath(xml_filename)
                res = convert_annotation(img_filename.as_posix(),xml_filename.as_posix(),out_path)
                if res == -1:
                    print('add ',img_filename.as_posix())
                    f.writelines(img_filename.as_posix()+'\n')