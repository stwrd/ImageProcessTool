import xml.etree.ElementTree as ET
import pickle
import os
import numpy as np

classes = ["smoke","people","head","person","phone","smoke_phone"]
# classes = ['zebra crossing','left turn', 'right turn','straight','straight&left','straight&right','u-turn']
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
                if ET.iselement(obj.find('difficult')) and ET.iselement(obj.find('bndbox')):
                    difficult = obj.find('difficult').text
                    cls = obj.find('name').text
                    if cls not in classes or int(difficult)==1:
                        continue
                    cls_id = classes.index(cls)
                    xmlbox = obj.find('bndbox')
                    b = np.array([float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text)]).astype('int')
                    # if (b[1]-b[0] < 16) or (b[3] - b[2] < 16):#过滤过小的目标
                    #     continue
                    bb = convert((w,h), b)
                    # out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                    if cls_id > 0:
                        out_file.write(str(0) + " " + " ".join([str(a) for a in bb]) + '\n')
                    else:
                        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            out_file.close()
    else:
        out_file = open(out_name, 'w')
        out_file.close()

if __name__ == '__main__':
    img_path = r'/media/hzh/ssd_disk/mclz/0724_kitchen'
    xml_path = r'/media/hzh/ssd_disk/mclz/0724_kitchen'
    suffix = '.jpg'

    img_file_list = os.listdir(img_path)
    xml_file_list = os.listdir(xml_path)
    img_file_list = [os.path.join(img_path,filename) for filename in img_file_list if filename.endswith(suffix)]
    xml_file_list = [os.path.join(xml_path,filename) for filename in xml_file_list if filename.endswith('.xml')]

    # #skip
    # skip = 85873
    # img_file_list = img_file_list[skip:]
    # xml_file_list = xml_file_list[skip:]

    idx = 1
    for img_filename in img_file_list:
        print('process ', img_filename)
        basename = os.path.split(img_filename)[1]
        xml_filename = os.path.join(xml_path, basename.replace('.jpg', '.xml')).replace('.jpeg','.xml')
        # if os.path.exists(xml_filename) and (not os.path.exists(img_filename)):#异常处理，一个大坑！！！会导致生成的标注文件错位，一直无法收敛
        #     os.remove(xml_filename)
        #     print('remove ',xml_filename)
        res = convert_annotation(img_filename,xml_filename)
        if res == -1:
            print(img_filename)
    # for img_filename,xml_filename in zip(img_file_list,xml_file_list):
    #     print('process ',img_filename,xml_filename)
    #     res = convert_annotation(img_filename,xml_filename)
    #     if res == -1:
    #         print(img_filename)