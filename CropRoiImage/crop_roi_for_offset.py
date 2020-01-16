import os
import cv2
import numpy as np
big_img_name_before = r'/media/hzh/work/workspace/mmdetection/step2/2_960_0.jpg'
big_img_name = r'/media/hzh/work/workspace/mmdetection/step2/4_960_0.jpg'
roi_mask_dir  = r'/media/hzh/work/workspace/mmdetection/step2'
out_dir = r'/media/hzh/work/workspace/mmdetection/step3'
os.makedirs(out_dir,exist_ok=True)

before_big_img = cv2.imread(big_img_name_before)
big_img = cv2.imread(big_img_name)
big_filename = os.path.split(big_img_name)[1]
big_base_filename = os.path.splitext(big_filename)[0]
big_names = big_base_filename.split('_')
base_offset = (int(big_names[1]),int(big_names[2]))#big img相对于全图的基础偏移

roi_filename_list = [ filename for filename in os.listdir(roi_mask_dir) if filename.endswith('.png')]

for roi_filename in roi_filename_list:
    roi_filename_base = os.path.splitext(roi_filename)[0]
    names = roi_filename_base.split('_')
    offset = (int(names[1]),int(names[2]))#小roi相对于全图的基础偏移

    relative_offset = (offset[0]-base_offset[0],offset[1]-base_offset[1])#相对于当前big img的偏移

    roi_mask_img = cv2.imread(os.path.join(roi_mask_dir,roi_filename),cv2.IMREAD_UNCHANGED)
    roi_width,roi_height = roi_mask_img.shape[1],roi_mask_img.shape[0]
    if relative_offset[0] >=0 and relative_offset[1] >= 0 and relative_offset[0]+roi_width <big_img.shape[1] and relative_offset[1] + roi_height < big_img.shape[0]:
        roi_src_img = big_img[relative_offset[1]:relative_offset[1]+roi_height,relative_offset[0]:relative_offset[0]+roi_width,...]
        alarm_img = roi_src_img.copy()
        alarm_img[roi_mask_img == 255] = (0, 0, 255)
        roi_src_img = cv2.addWeighted(roi_src_img,0.5,alarm_img,0.5,0)
        cv2.imwrite(os.path.join(out_dir,roi_filename),roi_src_img)

        before_src_img = before_big_img[relative_offset[1]:relative_offset[1]+roi_height,relative_offset[0]:relative_offset[0]+roi_width,...]
        cv2.imwrite(os.path.join(out_dir, 'base_'+roi_filename), before_src_img)
