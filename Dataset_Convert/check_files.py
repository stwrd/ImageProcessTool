#检测是否有冗余文件


import xml.etree.ElementTree as ET
import pickle
import os
import numpy as np

classes = ["smoke","people","head","person"]

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
    for xml_filename in xml_file_list:
        basename = os.path.split(xml_filename)[1]
        img_filename = os.path.join(img_path,basename.replace('.xml',suffix))
        if os.path.exists(xml_filename) and (not os.path.exists(img_filename)):#异常处理，一个大坑！！！会导致生成的标注文件错位，一直无法收敛
            # os.remove(xml_filename)
            print('remove ',xml_filename)