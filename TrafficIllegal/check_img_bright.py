from pathlib import Path
import numpy as np
import cv2
import sys
import shutil

def check_img_bright(img):
    resize_img = cv2.resize(img,(128,128))
    roi1 = resize_img[:64,:64,:]
    roi2 = resize_img[64:,:64,:]
    roi3 = resize_img[:64,64:,:]
    roi4 = resize_img[64:,64:,:]
    pixels_avg1 = np.sum(roi1)/(64*64*3)
    pixels_avg2 = np.sum(roi2)/(64*64*3)
    pixels_avg3 = np.sum(roi3)/(64*64*3)
    pixels_avg4 = np.sum(roi4)/(64*64*3)
    pixels = [pixels_avg1,pixels_avg2,pixels_avg3,pixels_avg4]
    print('avg:{} {} {} {}'.format(pixels_avg1,pixels_avg2,pixels_avg3,pixels_avg4))
    cnt = 0
    for val in pixels:
        if val < 70:
            cnt+=1
    if cnt > 2:
        return True
    else:
        return False

def check_img_bright1(img):
    resize_img = cv2.resize(img,(128,128))
    hist1 = cv2.calcHist([resize_img],[0],None,[256],[0,256])
    hist2 = cv2.calcHist([resize_img],[1],None,[256],[0,256])
    hist3 = cv2.calcHist([resize_img],[2],None,[256],[0,256])
    hist = hist1.reshape(-1)+hist2.reshape(-1)+hist3.reshape(-1)
    start = 128*128*3*0.2
    end = 128*128*3*0.8
    pre_out = 0
    cnt_s = 0
    for i,s in enumerate(hist):
        pre_out += s
        if pre_out > end:
            cnt_s += i*(end - (pre_out-s))
            break
        if pre_out > start:
            cnt_s += i*(pre_out-start)
            start = pre_out
    avg = cnt_s/(128*128*3*0.6)
    print('avg:',avg)
    if avg < 60:
        return True
    else:
        return False

if __name__ == '__main__':
    input_path = sys.argv[1]
    #input_path = '/media/hzh/work/data/百色/百色原图拷贝-0420/1208充分删除/图片模糊'
    h_path = Path(input_path)
    filelist = h_path.rglob('*.jpg')
    target_path = '/media/hzh/work/out_dark'
    for filename in filelist:
        img = cv2.imread(filename.as_posix())
        # print(filename.as_posix())
        if check_img_bright1(img):
            cur_folder_path = filename.parent
            new_filename = filename.as_posix().replace(cur_folder_path.as_posix(),target_path)
            print(new_filename)
            shutil.copy(filename,new_filename)