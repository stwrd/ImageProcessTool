import os
import numpy as np
import warnings
from pathlib import Path
import cv2
import shutil
#检测目录下的图片标注是否合法，不合法则移至垃圾箱
warnings.filterwarnings('ignore')

tar_path = '/media/hzh/docker_disk/dataset/traffic/data2'
trash_path = '/media/hzh/docker_disk/dataset/traffic/trash'
os.makedirs(trash_path,exist_ok=True)
pattern_list = ['*.txt']
cnt = 0
for pattern_str in pattern_list:
    filenames = Path(tar_path).rglob(pattern_str)
    with open(os.path.join('/media/hzh/ssd_disk','trash_remove_list.txt'),'w') as f:
        for filename in filenames:
            labels = np.loadtxt(str(filename), dtype=np.float32).reshape(-1, 5)
            for label in labels:
                x1 = label[1] - label[3]/2
                y1 = label[2] - label[4]/2
                x2 = label[1] + label[3]/2
                y2 = label[2] + label[4]/2
                if x1 < 0 or y1 < 0 or  x2 >= 1 or y2 >=1:
                    print(filename)
                    #shutil.move(filename, os.path.join(trash_path, filename.name))
                    f.write(str(filename) + '\n')
