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
    filelist = os.listdir(target_folder)
    for filename in filelist:
        dst_filename = os.path.join(dst_folder,filename)
        if os.path.exists(dst_filename):
            print(dst_filename)
            os.remove(dst_filename)

if __name__ == '__main__':
    remove_filelist_for_target_folder('/media/hzh/work/workspace/data/data_smoke/output/smoke','/media/hzh/ssd_disk/smoke_and_call/标注数据-吸烟打手机分类/people')
    # target_folder = sys.argv[1]
    # src_folder = sys.argv[2]
    # dst_folder = sys.argv[3]
    # move_filelist_to_another_folder(target_folder,src_folder,dst_folder)