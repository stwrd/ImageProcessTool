import os
import file_and_folder_ops
from pathlib import Path
import shutil

if __name__ == '__main__':
    target_folder = '/media/hzh/ssd_disk/Traffic/Dataset/keypoint_yx_targets/zhaohui'
    for filename in Path(target_folder).rglob('*.jpg'):
        image_folder, image_name = os.path.split(filename)
        new_image_name = file_and_folder_ops.strip_chinese_character(image_name)
        new_filename = os.path.join(image_folder,new_image_name)
        shutil.move(filename,new_filename)
