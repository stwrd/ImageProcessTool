import os
import numpy as np
import shutil
import sys

#去除前缀
def remove_prefix_to_files(target_folder,prefix=''):
    filelist = os.listdir(target_folder)
    prefix_len = len(prefix)+1# 因为中间还有个分隔符 '_'
    new_filelist = [filename[prefix_len:] for filename in filelist]
    full_filelist = [os.path.join(target_folder,filename) for filename in filelist]
    full_new_filelist = [os.path.join(target_folder,filename) for filename in new_filelist]
    for old_filename,new_filename in zip(full_filelist,full_new_filelist):
        shutil.move(old_filename,new_filename)
        print('rename {} to {}'.format(old_filename,new_filename))

#去除后缀
def remove_postfix_to_files(target_folder,postfix=''):
    print(target_folder)
    print(postfix)
    filelist = os.listdir(target_folder)
    full_filelist = [os.path.join(target_folder,filename) for filename in filelist]
    postfix_len = len(postfix)
    for full_filename in full_filelist:
        print(full_filename)
        filename = os.path.split(full_filename)[1]
        basename,type = os.path.splitext(filename)
        if basename[-postfix_len:] == postfix:
            new_basename = basename[:-postfix_len]
            new_filename = new_basename+type
            new_full_filename = os.path.join(target_folder,new_filename)
            shutil.move(full_filename, new_full_filename)
            print('rename {} to {}'.format(filename, new_filename))

if __name__ == '__main__':
    target_folder = sys.argv[1]
    target_prefix = sys.argv[2]
    remove_postfix_to_files(target_folder,postfix=target_prefix)