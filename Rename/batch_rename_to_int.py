import os
import numpy as np
import shutil
import sys

#重命名数字序号
start_idx = 10742
def add_prefix_to_files(target_folder, suffix=''):
    filelist = os.listdir(target_folder)
    img_filelist = [os.path.join(target_folder,filename) for filename in filelist if filename.endswith(suffix)]
    json_filelist = [os.path.join(target_folder,filename.replace(suffix,'.json')) for filename in img_filelist]
    xml_filelist = [os.path.join(target_folder, filename.replace(suffix, '.xml')) for filename in img_filelist]
    txt_filelist = [os.path.join(target_folder, filename.replace(suffix, '.txt')) for filename in img_filelist]
    for i,(img_filename,json_filename,xml_filename,txt_filename) in enumerate(zip(img_filelist,json_filelist,xml_filelist,txt_filelist)):
        print('process ',img_filename)
        shutil.move(img_filename,os.path.join(target_folder,'{:0=6}{}'.format(i+1+start_idx, suffix)))
        if os.path.exists(json_filename):
            shutil.move(json_filename,os.path.join(target_folder,'{:0=6}.json'.format(i+1+start_idx)))
        if os.path.exists(xml_filename):
            shutil.move(xml_filename, os.path.join(target_folder, '{:0=6}.xml'.format(i+1+start_idx)))
        if os.path.exists(txt_filename):
            shutil.move(txt_filename, os.path.join(target_folder, '{:0=6}.txt'.format(i+1+start_idx)))

if __name__ == '__main__':
    target_folder = sys.argv[1]
    target_prefix = sys.argv[2]
    add_prefix_to_files(target_folder, suffix=target_prefix)