import cv2
import os
import numpy as np
path1 = '/media/hzh/ssd_disk/Traffic/traffic_split_data_1208_1301_1345_by1213/1208X/340221000000050001_3402210100046899_1208X_02_null_B69BA1_20191025114954_0_1_a.jpg'
path2 = '/media/hzh/ssd_disk/Traffic/traffic_split_data_1208_1301_1345_by1213/1208X/340221000000050001_3402210100046899_1208X_02_null_B69BA1_20191025114954_0_1_c.jpg'

img1 = cv2.imread(path1)
img1 = cv2.resize(img1, None,None,0.25,0.25)
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

edge1 = cv2.Sobel(gray1,-1,0,1)
_,edge1 = cv2.threshold(edge1,100,255,cv2.THRESH_BINARY)
cv2.imshow('edge1',edge1)
cv2.waitKey(0)
img2 = cv2.imread(path2)
img2 = cv2.resize(img2, None,None,0.25,0.25)
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)


sub_img = gray2.astype(np.float) - gray1.astype(np.float)
sub_img = np.abs(sub_img)
sub_img = sub_img.astype(np.uint8)
_,sub_img = cv2.threshold(sub_img,30,255,cv2.THRESH_OTSU)
cv2.imshow('gray1',gray1)
cv2.imshow('gray2',gray2)
cv2.imshow('tt',sub_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
