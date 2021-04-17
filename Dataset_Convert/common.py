import os
import os
import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET
import sys
import json

def search_all_folder(input_path):
    totalfolders = []
    for root,dirs,files in os.walk(input_path):
        totalfolders.append(root)
    return totalfolders

def check_voc_label(xml_path):
    labels = {}
    if os.path.exists(xml_path):
        in_file = open(xml_path,encoding='utf-8')
        parser = ET.XMLParser(encoding='utf-8')
        tree=ET.parse(in_file,parser=parser)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            if ET.iselement(obj.find('bndbox')):
                cls = obj.find('name').text
                if cls in labels.keys():
                    labels[cls] += 1
                else:
                    labels[cls] = 1
                # if cls not in labels:
                #     labels.append(cls)
    return labels

#检测文件夹下的所有xml标注文件中的标签
def check_labels_in_folder(input_path):
    total_labels = {}
    for xml_path in Path(input_path).rglob('*.xml'):
        labels = check_voc_label(xml_path)
        for key in labels:
            if key in total_labels.keys():
                total_labels[key] += labels[key]
            else:
                total_labels[key] = labels[key]
    return total_labels

def convert(str,rows):
    num = len(str)
    cols = (num//(2*rows-2))*(rows-1)+(rows-1)
    str_arr = np.zeros([rows,cols],dtype=np.str)
    flag = rows-1
    r_mode = True
    i,j = 0,0
    for s in str:
        flag -= 1
        str_arr[i, j] = s
        if r_mode:
            i += 1
        else:
            i -= 1
            j += 1
        if flag == 0:
            r_mode = not r_mode
            flag = rows-1
    str_resort = ''
    for i in range(rows):
        for j in range(cols):
            if str_arr[i,j] != '':
                str_resort += str_arr[i,j]
    return str_resort


if __name__ == '__main__':
    str = '12345678'
    convert(str,3)

    input_path = '/media/hzh/docker_disk/dataset/深铁/车载巡检/CZXJonline20200413_done'
    labels = check_labels_in_folder(input_path)

    # folders = search_all_folder(input_path)
    # total_labels = {}
    # for folder in folders:
    #     labels = check_labels_in_folder(folder)
    #     for key in labels:
    #         if key in total_labels.keys():
    #             total_labels[key] += labels[key]
    #         else:
    #             total_labels[key] = labels[key]
    print(labels)
    with open('labels.json', 'w') as json_file:
        json.dump(labels, json_file)
