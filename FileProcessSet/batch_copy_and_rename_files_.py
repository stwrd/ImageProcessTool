#批量复制某个文件为序号i-i+n的文件名

import shutil
import os

def batch_rename_file_to_range(filename,start_idx,end_idx):
    target_str = filename[-10:-4]
    old_filename = filename
    for i in range(start_idx,end_idx+1):
        rename_str = '{:0=6}'.format(i)
        new_filename = filename.replace(target_str,rename_str)
        shutil.copy(old_filename,new_filename)