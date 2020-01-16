# coding: utf-8
import pickle
import os
import numpy as np
import json
classes = ["line","stopline"]

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x1 = box[0]*dw
    x2 = box[1]*dw
    y1 = box[2]*dh
    y2 = box[3]*dh
    return (x1,y1,x2,y2)

def convert_annotation(img_filename,xml_file_name):

    out_name = img_filename.replace(os.path.splitext(img_filename)[1], '.txt')

    if os.path.exists(xml_file_name):
        with open(xml_file_name,encoding='gbk') as f:
            data = json.load(f)
            w = int(data['imageWidth'])
            h = int(data['imageHeight'])
            out_file = open(out_name, 'w')
            if w == 0 or h == 0:
                out_file.close()
                print('invalid json file')
                return -1
            for shape in data['shapes']:
                if shape['shape_type'] != 'line':
                    print('Skipping shape: label={label}, shape_type={shape_type}'.format(**shape))
                    continue
                class_name = shape['label']
                class_id = classes.index(class_name)
                pt1, pt2 = shape['points']
                pt1 = np.array(pt1).astype('int')
                pt2 = np.array(pt2).astype('int')

                # 调换位置(左，右）
                if pt1[0] > pt2[0]:
                    pt1[0], pt2[0] = pt2[0], pt1[0]
                    pt1[1],pt2[1] = pt2[1],pt1[1]

                b = np.array([float(pt1[0]), float(pt2[0]), float(pt1[1]), float(pt2[1])]).astype('int')
                # if (b[1]-b[0] < 16) or (b[3] - b[2] < 16):#过滤过小的目标
                #     continue
                bb = convert((w,h), b)
                if class_id == 0:
                    out_file.write(str(class_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            out_file.close()
    else:
        out_file = open(out_name, 'w')
        out_file.close()

if __name__ == '__main__':

    img_path = r'/media/hzh/ssd_disk/Traffic/lane_done/lane_data1221done'
    xml_path = r'/media/hzh/ssd_disk/Traffic/lane_done/lane_data1221done'
    suffix = '.jpg'

    img_file_list = os.listdir(img_path)
    xml_file_list = os.listdir(xml_path)
    img_file_list = [os.path.join(img_path,filename) for filename in img_file_list if filename.endswith('.jpg') or filename.endswith('.jpeg')]
    xml_file_list = [os.path.join(xml_path,filename) for filename in xml_file_list if filename.endswith('.json')]

    # #skip
    # skip = 85873
    # img_file_list = img_file_list[skip:]
    # xml_file_list = xml_file_list[skip:]

    idx = 1
    for img_filename in img_file_list:
        print('process ', img_filename,idx)
        idx += 1
        basename = os.path.split(img_filename)[1]
        xml_filename = os.path.join(xml_path, basename.replace('.jpg', '.json')).replace('.jpeg','.json')
        res = convert_annotation(img_filename,xml_filename)
        if res == -1:
            print(img_filename)
