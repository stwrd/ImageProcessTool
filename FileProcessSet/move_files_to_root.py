#移动目标文件夹下的所有文件至根目录

import shutil
import os
from pathlib import Path

pattern_str = '*.jpg'
target_path = '/media/hzh/docker_disk/dataset/traffic/交通违法第一次通用标注/src'
dst_folder = '/media/hzh/docker_disk/dataset/traffic/交通违法第一次通用标注/Annotations'
filenames = Path(target_path).rglob(pattern_str)

for filename in filenames:
    base_name = os.path.split(filename.as_posix())[1]
    dst_path = os.path.join(dst_folder,base_name)
    shutil.copy(filename.as_posix(),dst_path)
    print('copy {} to {}'.format(filename,dst_path))