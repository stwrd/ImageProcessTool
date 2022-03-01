import cv2
import numpy as np
if __name__ == '__main__':
    imglist = ['/media/hzh/work/out/000011_桂AXZ956_0.jpg','/media/hzh/work/out/000011_桂AXZ956_1.jpg','/media/hzh/work/out/000011_桂AXZ956_2.jpg','/media/hzh/work/out/000011_桂AXZ956_3.jpg']
    big_img = None
    for x in range(2):
        for y in range(2):
            p = imglist[x*2+y]
            img = cv2.imread(p)
            if big_img is None:
                h,w,_ = img.shape
                big_img = np.zeros([h*2,w*2,3],np.uint8)
            big_img[y*h:(y+1)*h,x*w:(x+1)*w,:] = img
    cv2.imshow('tt',big_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('/home/hzh/图片/sample.jpg',big_img)
