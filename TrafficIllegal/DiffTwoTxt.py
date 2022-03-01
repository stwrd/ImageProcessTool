import os
import shutil
from pathlib import Path
#比较两个文件，将输出不同的找出来，并进行输出
def diff_two_file(file1,file2):
    diff_list = []
    f1 = open(file1,'r')
    f2 = open(file2,'r')
    while True:
        l1 = f1.readline()
        l2 = f2.readline()
        if l1 == '' or l2 == '':
            break
        else:
            if l1 != l2:
                position = l1.find('#')
                diff_list.append(l1[:position])
    f1.close()
    f2.close()
    return diff_list

#输出包含特定字符串的文本
def search_target_string(input_filename,target_str):
    str_list = []
    with open(input_filename,'r') as f:
        for line in f:
            position = line.find(target_str)
            if position != -1:
                str_list.append(line[:position].strip())
    return str_list

def find_group_image(image_file_path):
    cur_folder_path = image_file_path.parent
    image_name_without_suffix = image_file_path.stem
    return sorted(cur_folder_path.glob(image_name_without_suffix[:-1]+'*.jpg'))

import cv2
if __name__ == '__main__':
    file_name1 = '/media/hzh/work/workspace/cambricon/ev_sdk_traffic_violations/1352_result_shanchu.txt'
    # file_name2 = '/media/hzh/work/workspace/cambricon/ev_sdk_traffic_violations/ceshi/zhaohui.txt'
    # diff_list =diff_two_file(file_name1,file_name2)
    # print(diff_list)

    out_path = '/media/hzh/work/data/stardard_test_data/1352/zhaohui_error'
    os.makedirs(out_path,exist_ok=True)
    str_list = search_target_string(file_name1,'#2#')
    print(str_list)
    out_error_file = file_name1.replace('.txt','_error.txt')
    with open(out_error_file,'w') as f:
        for line in str_list:
            image_group = find_group_image(Path(line))
            for img_path in image_group:
                shutil.copy(img_path.as_posix(),os.path.join(out_path,os.path.split(img_path.as_posix())[1]))
            f.write(line+'\n')

