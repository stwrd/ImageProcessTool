#将n个子图像拼接成n宫格图像
import numpy as np
import cv2
from pathlib import Path
import os

def load_image(img_path,long_side):
    img = cv2.imread(img_path)  # BGR
    assert img is not None, 'Image Not Found ' + img_path
    r = long_side / max(img.shape)  # size ratio
    h, w, _ = img.shape
    img = cv2.resize(img, (int(w * r), int(h * r)), interpolation=cv2.INTER_LINEAR)  # _LINEAR fastest
    return img

def create_grid_img(img_list,img_size,n):
    img16 = np.zeros((img_size, img_size, 3), dtype=np.uint8) + 128
    for i,img_path in enumerate(img_list):
        # Load image
        ceil = img_size//n
        #father_folder = '/media/hzh/work/git_code/yolov3-channel-and-layer-pruning'
        img = load_image(img_path,long_side=ceil)
        h, w, _ = img.shape
        x1a,y1a,x2a,y2a = (i%n)*ceil,int(i/n)*ceil,(i%n)*ceil+w,int(i/n)*ceil+h#large pic
        x1b,y1b,x2b,y2b = 0,0,w,h
        # place img in img16
        img16[y1a:y2a, x1a:x2a] = img[y1b:y2b, x1b:x2b]  # img4[ymin:ymax, xmin:xmax]
    return img16

def genetate_dataset(img_list,n,output_folder):
    num = len(img_list)
    for i in range(0,num,n*n):
        if i + n*n <= num:
            sub_list = img_list[i:i+n*n]
        else:
            sub_list = img_list[i:]
        stitching_img = create_grid_img(sub_list,480,n)
        p = Path(output_folder)
        p.mkdir(exist_ok=True)
        file_name = p.joinpath(output_folder,'{:0=4d}.jpg'.format(i//(n*n)+1))
        cv2.imwrite(file_name.as_posix(),stitching_img)

def do_from_folder(path):
    p = Path(path)
    imglist = p.rglob('*.jpg')
    img_list = [img_path.as_posix() for img_path in imglist]
    genetate_dataset(img_list,3,'/media/hzh/docker_disk/dataset/smoke_data/test')

def do_from_txt(path):
    with open(path, 'r') as f:
        imglist = [filename.strip() for filename in f]
        genetate_dataset(imglist,3,'/media/hzh/docker_disk/dataset/smoke_data/test')
if __name__ == '__main__':
    do_from_folder('/media/hzh/ssd_disk/smoke_and_call/原始标注数据-吸烟打手机分类/smoke_and_call_auto_detect_619/smoke_and_call_auto_detect_619_4/疑似')
    # do_from_txt('/media/hzh/docker_disk/dataset/smoke_data/step2/test.txt')