import os
import numpy as np
import shutil
import sys

#重命名数字序号
start_idx = 0

def add_prefix_to_files_by_move(target_folder, suffix):
    filelist = os.listdir(target_folder)
    img_filelist = [os.path.join(target_folder,filename) for filename in filelist if filename.endswith(suffix)]
    json_filelist = [os.path.join(target_folder,filename.replace(suffix,'.json')) for filename in img_filelist]
    xml_filelist = [os.path.join(target_folder, filename.replace(suffix, '.xml')) for filename in img_filelist]
    txt_filelist = [os.path.join(target_folder, filename.replace(suffix, '.txt')) for filename in img_filelist]
    for i,(img_filename,json_filename,xml_filename,txt_filename) in enumerate(zip(img_filelist,json_filelist,xml_filelist,txt_filelist)):
        # print('process ',img_filename)
        shutil.move(img_filename,os.path.join(target_folder,'{:0=6}{}'.format(i+1+start_idx, suffix)))
        if os.path.exists(json_filename):
            shutil.move(json_filename,os.path.join(target_folder,'{:0=6}.json'.format(i+1+start_idx)))
        if os.path.exists(xml_filename):
            shutil.move(xml_filename, os.path.join(target_folder, '{:0=6}.xml'.format(i+1+start_idx)))
        if os.path.exists(txt_filename):
            shutil.move(txt_filename, os.path.join(target_folder, '{:0=6}.txt'.format(i+1+start_idx)))

def add_prefix_to_files_by_copy(target_folder, dst_folder, suffix):
    global start_idx
    os.makedirs(dst_folder,exist_ok=True)
    filelist = os.listdir(target_folder)
    img_filelist = [os.path.join(target_folder,filename) for filename in filelist if filename.endswith(suffix)]
    json_filelist = [os.path.join(target_folder,filename.replace(suffix,'.json')) for filename in img_filelist]
    xml_filelist = [os.path.join(target_folder, filename.replace(suffix, '.xml')) for filename in img_filelist]
    txt_filelist = [os.path.join(target_folder, filename.replace(suffix, '.txt')) for filename in img_filelist]
    for i,(img_filename,json_filename,xml_filename,txt_filename) in enumerate(zip(img_filelist,json_filelist,xml_filelist,txt_filelist)):
        print('Number:',1+start_idx,' process ',img_filename)
        shutil.copy(img_filename,os.path.join(dst_folder,'{:0=6}{}'.format(1+start_idx, suffix)))
        if os.path.exists(json_filename):
            shutil.copy(json_filename,os.path.join(dst_folder,'{:0=6}.json'.format(1+start_idx)))
        # if os.path.exists(xml_filename):
        #     shutil.copy(xml_filename, os.path.join(dst_folder, '{:0=6}.xml'.format(1+start_idx)))
        if os.path.exists(txt_filename):
            shutil.copy(txt_filename, os.path.join(dst_folder, '{:0=6}.txt'.format(1+start_idx)))
        start_idx+=1

def show_something():
    print('123455=============')
if __name__ == '__main__':
    target_folder = sys.argv[1]
    target_prefix = sys.argv[2]
    add_prefix_to_files_by_move(target_folder, suffix=target_prefix)