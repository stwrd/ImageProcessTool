# coding=utf-8
# 请你补全代码，将源文件夹中的数据集进行左右镜像和上下颠倒，并对其标注进行同等变换，转换为darknet风格，保存于输出文件夹中
# 源文件夹路径 src=/tmp/interview/input_data
# 输出文件夹  dst=/tmp/interview/output_data
# 源文件夹中的图片和对应的标注文件同名

'''
原始标注文件为图片同名的json文件，结构如下(x1,y1),(x2,y2)
  {
    "shapes": [
    {
      "label": "truck",
      "points": [
        [500,500],
        [800,800]
      ],
      "shape_type": "rectangle",
    },
    {
      "label": "car",
      "points": [
        [500,500],
        [800,800]
      ],
      "shape_type": "rectangle",
    }
  ],
  "imageHeight": 1000,
  "imageWidth": 1000
}

转换后保存为和图片同名的txt文件，文件内容为（label,x,y,w,h），示例如下：
1 0.5 0.5 0.3 0.3
0 0.5 0.5 0.3 0.3
'''

import os
import shutil
import numpy as np
import json
import cv2
classes = ["car","truck","motobike"]

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

def convert_annotation(img_filename,xml_file_name,darknet_file_name):
    out_name = darknet_file_name
    if os.path.exists(xml_file_name):
        with open(xml_file_name) as f:
            data = json.load(f)
            w = int(data['imageWidth'])
            h = int(data['imageHeight'])
            out_file = open(out_name, 'w')
            if w == 0 or h == 0:
                out_file.close()
                print('invalid json file')
                return -1
            img = cv2.imread(img_filename)
            img = img[::-1,...]
            img = img[:,::-1,...]
            cv2.imwrite(darknet_file_name.replace('.txt','.jpg'),img)
            for shape in data['shapes']:
                if shape['shape_type'] != 'rectangle':
                    print('Skipping shape: label={label}, shape_type={shape_type}'.format(**shape))
                    continue
                class_name = shape['label']
                class_id = classes.index(class_name)
                pt1, pt2 = shape['points']
                pt1 = np.array(pt1).astype('int')
                pt2 = np.array(pt2).astype('int')

                # 调换位置(左上，右下）
                if pt1[0] > pt2[0]:
                    pt1[0], pt2[0] = pt2[0], pt1[0]
                if pt1[1] > pt2[1]:
                    pt1[1], pt2[1] = pt2[1], pt1[1]
                if np.sum(np.array([class_id, pt1[0], pt1[1], pt2[0] - pt1[0], pt2[1] - pt1[1]]) < 0) > 0:
                    print(np.array([class_id, pt1[0], pt1[1], pt2[0] - pt1[0], pt2[1] - pt1[1]]))
                pt1[0],pt1[1] = w - pt1[0], h - pt1[1]
                pt2[0],pt2[1] = w - pt2[0], h - pt2[1]
                bbox = np.array([float(pt1[0])/w,float(pt1[1])/h, float(pt2[0])/w, float(pt2[1])/h])
                bb = [bbox[0],bbox[1],bbox[2]-bbox[0],bbox[3]-bbox[1]]
                out_file.write(str(class_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            out_file.close()
    else:
        out_file = open(out_name, 'w')
        out_file.close()

def transform_dataset(src, dst):
    #在这里补全相关代码
    file_list = os.listdir(src)
    img_list = [os.path.join(src,f) for f in file_list if f.endswith('.jpg')]
    os.makedirs(dst,exist_ok=True)
    for img_file in img_list:
        json_file = img_file.replace('.jpg','.json')
        darknet_file = img_file.replace('.jpg','.txt')
        darknet_file = darknet_file.replace(src,dst)
        convert_annotation(img_file,json_file,darknet_file)
    return


if __name__ == "__main__":
    src = '/tmp/interview/input_data'
    dst = '/tmp/interview/output_data'
    if os.path.exists(dst):
        shutil.rmtree(dst)
    transform_dataset(src,dst)