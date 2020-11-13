#复制目标文件夹下的训练数据到另一个文件夹中，并进行重命名
import os
import numpy as np
import shutil
import sys
import batch_rename_to_int
import file_and_folder_ops
if __name__ == '__main__':
    folder_list = ['/media/hzh/docker_disk/dataset/traffic/src']
    dst_folder = '/media/hzh/docker_disk/dataset/traffic/images'
    total_folders = []
    for folder in folder_list:
        total_folders = total_folders + file_and_folder_ops.search_all_folder(folder)
    for folder in total_folders:
        print(batch_rename_to_int.start_idx)
        batch_rename_to_int.add_prefix_to_files_by_copy(folder,dst_folder,'.jpg')