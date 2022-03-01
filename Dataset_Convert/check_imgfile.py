import os
import cv2
from pathlib import Path
import shutil
#检测目录下的图片是否损坏，若损坏，则移至垃圾箱
#trash
tar_path = '/media/hzh/docker_disk/dataset/traffic/交通违法2020年12月版通用数据/traffic_common_detect'
trash_path = '/media/hzh/docker_disk/dataset/traffic/交通违法2020年12月版通用数据/trash'
os.makedirs(trash_path,exist_ok=True)
pattern_list = ['*.jpg','*.png']
cnt = 0

for pattern_str in pattern_list:
    filenames = Path(tar_path).rglob(pattern_str)
    with open(os.path.join('/media/hzh/ssd_disk','trash_remove_list.txt'),'a') as f:
        for filename in filenames:
            cnt+=1
            img = cv2.imread(str(filename), cv2.IMREAD_COLOR)
            if img is None:
                print(str(filename))
                shutil.move(filename, os.path.join(trash_path,filename.name) )
                f.write(str(filename)+'\n')
            else:
                print('重新保存图片:',filename.as_posix())
                cv2.imwrite(filename.as_posix(),img)
print('total images num :',cnt)
