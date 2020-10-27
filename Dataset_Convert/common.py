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

if __name__ == '__main__':
    input_path = '/media/hzh/ssd_disk/深铁/ST/UAV20200917done'
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
