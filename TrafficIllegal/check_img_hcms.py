#判定图像的合成模式
import cv2
import numpy as np
import sys
from skimage import feature
from pathlib import Path

def search_hcms(img):
    ratio_x = 300/img.shape[1]
    img = cv2.resize(img,dsize=(0,0),dst=None,fx=ratio_x,fy=ratio_x)
    img = cv2.GaussianBlur(img,(3,3),0.3)
    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # corners = cv2.goodFeaturesToTrack(gray,50,0.01,10,corners=None,mask=None)
    # for corner_pt in corners.reshape(-1,2):
    #     cv2.circle(img,tuple(corner_pt),3,(255,0,0))
    # print(img.shape)
    base_boxes = [np.array([int(img.shape[1]*0.05),int(img.shape[0]*0.05)]),
                  np.array([int(img.shape[1]*0.1),int(img.shape[0]*0.1)])]#w,h
    stride = np.array([5,5])
    match_thresh = 0.05
    for base_box in base_boxes:
        for x in range(0,img.shape[1]-base_box[0],300):
            for y in range(0,img.shape[0]-base_box[1],stride[1]):
                # print('x:',x,' y:',y)
                bbox = (x,y,base_box[0],base_box[1])
                # bbox = (5, 96, 34, 39)
                template_img = img[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2],:]
                resort_template = np.sort(template_img.reshape(-1))
                avg = np.mean(resort_template[::-1][:int(resort_template.shape[0]/10)])
                # print('avg:',avg)
                if avg < 50:
                    continue
                # print(template_img.shape)
                tmp = img.copy()
                tmp[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2],:] = 0
                result = cv2.matchTemplate(tmp,template_img,cv2.TM_SQDIFF_NORMED)
                resort_res = np.sort(result.reshape(-1))
                print('fifth value:',resort_res[1])
                if resort_res[1] < match_thresh:
                    loc = np.where(result <= resort_res[1])
                    valid_pts = [(x,y)]
                    for pt in zip(*loc[::-1]):
                        is_find = False
                        for pt1 in valid_pts:
                            if (abs(pt[0] - pt1[0]) < ((img.shape[1]/3)*0.9)) and (abs(pt[1] - pt1[1]) < ((img.shape[0]/3)*0.9)):
                                is_find = True
                                break
                        if not is_find:
                            valid_pts.append(pt)
                    if len(valid_pts) > 2:
                        for pt in valid_pts:
                            print('val:', result[pt[::-1]])
                            right_bottom = (pt[0] + base_box[0], pt[1] + base_box[1])
                            cv2.rectangle(img, pt, right_bottom, (0, 255, 0))
                        return template_img,img

        for x in range(0,img.shape[1]-base_box[0],stride[0]):
            for y in range(0,img.shape[0]-base_box[1],300):
                # print('x:',x,' y:',y)
                bbox = (x,y,base_box[0],base_box[1])
                # bbox = (5, 96, 34, 39)
                template_img = img[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2],:]
                resort_template = np.sort(template_img.reshape(-1))
                avg = np.mean(resort_template[::-1][:int(resort_template.shape[0]/10)])
                # print('avg:',avg)
                if avg < 50:
                    continue
                # print(template_img.shape)
                tmp = img.copy()
                tmp[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2],:] = 0
                result = cv2.matchTemplate(tmp,template_img,cv2.TM_SQDIFF_NORMED)
                resort_res = np.sort(result.reshape(-1))
                print('fifth value:',resort_res[1])
                if resort_res[1] < match_thresh:
                    loc = np.where(result <= resort_res[1])
                    valid_pts = [(x,y)]
                    for pt in zip(*loc[::-1]):
                        is_find = False
                        for pt1 in valid_pts:
                            if (abs(pt[0] - pt1[0]) < ((img.shape[1]/3)*0.9)) and (abs(pt[1] - pt1[1]) < ((img.shape[0]/3)*0.9)):
                                is_find = True
                                break
                        if not is_find:
                            valid_pts.append(pt)
                    if len(valid_pts) > 2:
                        for pt in valid_pts:
                            print('val:', result[pt[::-1]])
                            right_bottom = (pt[0] + base_box[0], pt[1] + base_box[1])
                            cv2.rectangle(img, pt, right_bottom, (0, 255, 0))
                        return template_img,img
    return template_img,img




if __name__ == '__main__':
    # target_dir = sys.argv[1]
    target_dir = '/media/hzh/work/data/格林/backErr/1208'
    p = Path(target_dir)
    filelist = p.glob('*.jpg')
    for filename in filelist:
        img = cv2.imread(filename.as_posix())
        # img = cv2.imread('/media/hzh/work/data/格林/backErr/1208/12080_02_湘ATZ411_20191003031945_0_1_R0202.jpg')
        t1 = cv2.getTickCount()
        template_img,img = search_hcms(img)
        cost_time = (cv2.getTickCount()-t1)*1000/cv2.getTickFrequency()
        print('cost time:',cost_time)
        cv2.imshow('pre', img)
        cv2.waitKey(0)

    # post_img = cv2.imread('/media/hzh/work/data/南宁/12080/12080/12.jpg')
    # resize_img = cv2.resize(img,(600,600))
    # post_img = cv2.resize(post_img,(300,300))
    # # bbox = (5, 96, 34, 39)
    # bbox = cv2.selectROI(resize_img,False)
    # print(bbox)
    # template_img = resize_img[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2],:]
    # tmp = resize_img.copy()
    # tmp[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2],:] = 0
    # res = cv2.matchTemplate(tmp,template_img,cv2.TM_SQDIFF_NORMED)
    # new_res = np.sort(res.reshape(-1))
    # print('first 10:',new_res[6])
    # loc = np.where(res <new_res[6])
    # min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(res)
    # # resize_img = cv2.cvtColor(resize_img,cv2.COLOR_BGR2GRAY)
    # print(loc)
    #
    #
    # print(bbox)
    # for pt in zip(*loc[::-1]):
    #     print('val:',res[pt[::-1]])
    #     right_bottom = (pt[0]+bbox[2],pt[1]+bbox[3])
    #     cv2.rectangle(resize_img,pt,right_bottom,(0,255,0))
    #     cv2.imshow('pre', resize_img)
    #     cv2.waitKey(0)
    # cv2.imshow('template_img', template_img)
    # # cv2.imshow('post', post_img)
    # cv2.imshow('pre',img)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()