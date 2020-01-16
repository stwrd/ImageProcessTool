import os
import sys
import cv2
import shutil

result_file=r'/media/hzh/work/workspace/data/1301_keep/result.txt'
src_image_folder = r'/media/hzh/work/workspace/data/1301_keep'
target_folder=r'/media/hzh/work/workspace/data/1301_keep_delete'
os.makedirs(target_folder,exist_ok=True)

with open(result_file,encoding='UTF-8') as f:
    results=f.readlines()

for result in results:
    split_result = result.split('#')
    img_name,cls = split_result[0].strip(),split_result[2].strip()
    cls_folder = os.path.join(target_folder,cls)
    os.makedirs(cls_folder,exist_ok=True)
    src_path = os.path.join(src_image_folder,img_name+'.jpg')
    dst_path = os.path.join(cls_folder,img_name+'.jpg')
    print(img_name)
    shutil.copy(src_path,dst_path)