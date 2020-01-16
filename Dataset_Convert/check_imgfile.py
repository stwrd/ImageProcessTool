import os
import cv2

tar_path = '/media/hzh/work/workspace/py_smoke_call_train/roi_data_train_square/call'
filenames = os.listdir(tar_path)
for filename in filenames:
    full_filename = os.path.join(tar_path,filename)
    img = cv2.imread(full_filename, cv2.IMREAD_COLOR)
    if img is None:
        print(full_filename)