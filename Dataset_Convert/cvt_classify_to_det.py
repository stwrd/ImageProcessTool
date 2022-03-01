import pickle
import os
import numpy as np
import json

#将分类图像转为bbox类型
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
    out_file = open(out_name, 'w')
    bb = [0.5,0.5,1,1]
    out_file.write(str(0) + " " + " ".join([str(a) for a in bb]) + '\n')
    out_file.close()

if __name__ == '__main__':
    img_path = r'/media/hzh/docker_disk/dataset/call_data_near/call1'
    xml_path = r'/media/hzh/docker_disk/dataset/call_data_near/call1'
    suffix = '.jpg'

    img_file_list = os.listdir(img_path)
    xml_file_list = os.listdir(xml_path)
    img_file_list = [os.path.join(img_path,filename) for filename in img_file_list if filename.endswith('.jpg') or filename.endswith('.jpeg')]
    xml_file_list = [os.path.join(xml_path,filename) for filename in xml_file_list if filename.endswith('.json')]

    idx = 1
    for img_filename in img_file_list:
        print('process ', img_filename)
        basename = os.path.split(img_filename)[1]
        xml_filename = os.path.join(xml_path, basename.replace('.jpg', '.json')).replace('.jpeg','.json')
        res = convert_annotation(img_filename,xml_filename)
        if res == -1:
            print(img_filename)