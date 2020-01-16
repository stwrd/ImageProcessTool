#转换视频帧率

import cv2
import os
import sys
import numpy as np
import shutil
if __name__ == '__main__':
    # tar_path = sys.argv[1]
    # dst_path = sys.argv[2]
    tar_path = '/media/hzh/work/workspace/data/fighting_data/dj'
    dst_path = '/media/hzh/work/workspace/data/fighting/Anomaly-Videos-6fps'
    os.makedirs(dst_path,exist_ok=True)
    for sub_folder in os.listdir(tar_path):
        full_sub_floder = os.path.join(tar_path, sub_folder)
        if os.path.isdir(full_sub_floder):
            filename_list = os.listdir(full_sub_floder)
            for filename in filename_list:
                # print('process ',filename)
                if not filename.endswith('.mp4'):
                    continue
                full_path = os.path.join(full_sub_floder,filename)
                basename = os.path.splitext(filename)[0]
                new_full_path = os.path.join(dst_path,basename+'_6fps.mp4')
                cmd = 'ffmpeg -y -i {}  -r 6 {}'.format(full_path, new_full_path)
                print(cmd)
                os.system(cmd)


