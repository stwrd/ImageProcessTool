import os
import numpy as np
import shutil
import sys

#为文件夹内的文件添加指定前缀
def add_prefix_to_files(target_folder,prefix=''):
    filelist = os.listdir(target_folder)
    new_filelist = ['{}_{}'.format(prefix,filename) for filename in filelist]
    full_filelist = [os.path.join(target_folder,filename) for filename in filelist]
    full_new_filelist = [os.path.join(target_folder,filename) for filename in new_filelist]
    for old_filename,new_filename in zip(full_filelist,full_new_filelist):
        shutil.move(old_filename,new_filename)
        print('rename {} to {}'.format(old_filename,new_filename))


if __name__ == '__main__':
    target_folder = sys.argv[1]
    target_prefix = sys.argv[2]
    add_prefix_to_files(target_folder,prefix=target_prefix)