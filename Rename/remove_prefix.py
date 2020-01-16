import os
import numpy as np
import shutil
import sys

#去除前缀
def add_prefix_to_files(target_folder,prefix=''):
    filelist = os.listdir(target_folder)
    prefix_len = len(prefix)+1
    new_filelist = [filename[prefix_len:] for filename in filelist]
    full_filelist = [os.path.join(target_folder,filename) for filename in filelist]
    full_new_filelist = [os.path.join(target_folder,filename) for filename in new_filelist]
    for old_filename,new_filename in zip(full_filelist,full_new_filelist):
        shutil.move(old_filename,new_filename)
        print('rename {} to {}'.format(old_filename,new_filename))


if __name__ == '__main__':
    target_folder = sys.argv[1]
    target_prefix = sys.argv[2]
    add_prefix_to_files(target_folder,prefix=target_prefix)