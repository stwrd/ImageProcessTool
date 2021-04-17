import os
import numpy as np
import shutil
import sys

#移动指定文件夹中的filelist到另一文件夹
def add_prefix_to_files(target_folder,prefix=''):
    filelist = os.listdir(target_folder)
    prefix_len = len(prefix)+1
    new_filelist = [filename[prefix_len:] for filename in filelist]
    full_filelist = [os.path.join(target_folder,filename) for filename in filelist]
    full_new_filelist = [os.path.join(target_folder,filename) for filename in new_filelist]
    for old_filename,new_filename in zip(full_filelist,full_new_filelist):
        shutil.move(old_filename,new_filename)
        print('rename {} to {}'.format(old_filename,new_filename))

def move_filelist_to_another_folder(target_folder, src_folder, dst_folder):
    filelist = os.listdir(target_folder)
    for filename in filelist:
        older_filename = os.path.join(src_folder,filename)
        new_filename = os.path.join(dst_folder,filename)
        print(older_filename)
        shutil.copy(older_filename,new_filename)

#移除 dst_folder中与target_folder重名的文件
def remove_filelist_for_target_folder(target_folder,dst_folder):
    filelist = [f for f in os.listdir(target_folder) if f.endswith('.jpg')]
    for filename in filelist:
        dst_filename = os.path.join(dst_folder,filename)
        if os.path.exists(dst_filename):
            print(dst_filename)
            with open('remove_filelist.txt','a') as f:
                f.write(dst_filename+'\n')
            os.remove(dst_filename)
    return len(filelist)

# dst_folder 中与target_folder 重名的文件,两个目录结构必须相同
from pathlib import Path
def remove_filelist_for_target_folders(target_father_folder,dst_father_folder):
    src_folders = [f.as_posix() for f in Path(target_father_folder).rglob('') if f.is_dir()]
    src_folders = sorted(src_folders)
    print('target folders:',src_folders)
    dst_folders = [f.as_posix() for f in Path(dst_father_folder).rglob('') if f.is_dir()]
    dst_folders = sorted(dst_folders)
    print('dst_folders:',dst_folders)
    total_num = 0
    for target_folder,dst_folder in zip(src_folders,dst_folders):
        total_num += remove_filelist_for_target_folder(target_folder,dst_folder)
    print('check {} files'.format(total_num))

if __name__ == '__main__':
    remove_filelist_for_target_folders('/media/hzh/docker_disk/dataset/traffic/src','/media/hzh/docker_disk/dataset/traffic/src2')
    #remove_filelist_for_target_folder('/media/hzh/work/workspace/data/data_smoke/output/smoke','/media/hzh/ssd_disk/smoke_and_call/标注数据-吸烟打手机分类/people')
    # target_folder = sys.argv[1]
    # src_folder = sys.argv[2]
    # dst_folder = sys.argv[3]
    # move_filelist_to_another_folder(target_folder,src_folder,dst_folder)