import cv2
import numpy as np

# im = cv2.imread(r'C:\Users\stwrd\Desktop\hard\result_left_half_8.jpg',cv2.IMREAD_UNCHANGED)
# plande = np.zeros([im.shape[0],im.shape[1],3],dtype='uint8')
# lines = cv2.HoughLinesP(im,1,np.pi/180,threshold=20,minLineLength=10,maxLineGap=3)
# for x1, y1, x2, y2 in lines.reshape(-1, 4):
#     # cv2.line(half_im, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     if x1 == x2:
#         k = 0
#     else:
#         k = (y2 - y1) / (x2 - x1)
#     if np.abs(k) > 1:
#         cv2.line(plande, (x1, y1), (x2, y2), (255, 255, 255), 2)
#
# cv2.imshow('plande',plande)
# cv2.imshow('im',im)
# cv2.waitKey(0)

im1 = cv2.imread('/media/hzh/work/workspace/mmdetection/data/coco_split1/2_3.jpg')
im2 = cv2.imread('/media/hzh/work/workspace/mmdetection/data/coco_split1/4_3.jpg')
gray1 = cv2.cvtColor(im1,cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(im2,cv2.COLOR_BGR2GRAY)
dif = np.abs(gray1.astype('int')-gray2.astype('int')).astype('uint8')
_,bw = cv2.threshold(dif,50, 255, cv2.THRESH_BINARY)
cv2.imshow('diff',bw)
cv2.waitKey(0)
cv2.destroyAllWindows()