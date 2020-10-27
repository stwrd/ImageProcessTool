import os
from pathlib import Path
def search_all_folder(input_path):
    totalfolders = []
    for root,dirs,files in os.walk(input_path):
        totalfolders.append(root)
    return totalfolders


if __name__ == '__main__':
    target_path = '/media/hzh/ssd_disk/BaiduNetdiskDownload'
    subfolders = search_all_folder(target_path)
    print(subfolders)