import os
from pathlib import Path
def search_all_folder(input_path):
    totalfolders = []
    for root,dirs,files in os.walk(input_path):
        totalfolders.append(root)
    return totalfolders

def isvalid_symbol(code):
    if ord(code) >=32 and ord(code) <=122:
        return True
    else:
        return False

def strip_chinese_character(base_name):
    new_basename = ''
    for c in base_name:
        if isvalid_symbol(c):
            new_basename += c
    return new_basename

if __name__ == '__main__':
    target_path = '/media/hzh/ssd_disk/BaiduNetdiskDownload'
    subfolders = search_all_folder(target_path)
    print(subfolders)