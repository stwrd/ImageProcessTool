import cv2
import numpy
from pathlib import Path
import shutil
import os
import datetime
import time

Name_by_Time = False #是否以时间戳重命名
Copy_Mode = False  #是否为复制模式，当为False时剪切
target_folder = '/media/hzh/work/dxx_out'
dst_folder = '/media/hzh/ssd_disk/Traffic/Dataset/predict/left'
classify_names = ['left','straight','right','none']
for name in classify_names:
    os.makedirs(os.path.join(dst_folder,name),exist_ok=True)

def process(filename):
    img = cv2.imread(filename)
    now = datetime.datetime.now()
    timestr = now.strftime('%Y_%m_%d_%H_%M_%S')
    timestr = '{}_{}'.format(timestr, now.microsecond // 1000)
    revert_src = ''
    revert_dst = ''
    while True:
        cv2.imshow('window', img)
        k = cv2.waitKey(0)
        if (k == ord('1')):
            dst_path = os.path.join(dst_folder, 'zx', timestr + '.jpg')
            shutil.move(filename, dst_path)
            revert_src = filename
            revert_dst = dst_path
            break
        elif (k == ord('2')):
            dst_path = os.path.join(dst_folder, 'fx', timestr + '.jpg')
            shutil.move(filename, dst_path)
            revert_src = filename
            revert_dst = dst_path
            break
        elif (k == ord('3')):
            dst_path = os.path.join(dst_folder, 'other', timestr + '.jpg')
            shutil.move(filename, dst_path)
            revert_src = filename
            revert_dst = dst_path
            break
        else:
            print('invalid key')
    return revert_src,revert_dst

if __name__ == '__main__':
    start_time = time.time()
    cv2.namedWindow('window',0)
    img_num = 0

    while True:
        pattern_str = '*.jpg'
        file_list = Path(target_folder).rglob(pattern_str)
        revert_src = []
        revert_dst = []
        is_relist = False
        is_empty = True
        # if not any(file_list):
        #     break
        for filename in file_list:
            is_empty = False
            print('read next image')
            img = cv2.imread(filename.as_posix())
            print('read Done')
            if Name_by_Time:
                now = datetime.datetime.now()
                timestr = now.strftime('%Y_%m_%d_%H_%M_%S')
                timestr = '{}_{}'.format(timestr,now.microsecond//1000)
            else:
                timestr = os.path.splitext(os.path.split(filename.as_posix())[1])[0]

            while True:
                print('show next image')
                cv2.imshow('window',img)
                k = cv2.waitKey(0)
                do_flag = False
                for i,name in enumerate(classify_names):
                    if(k == ord(str(i+1))):
                        dst_path = os.path.join(dst_folder,name,timestr+'.jpg')
                        if Copy_Mode:
                            shutil.copy(filename.as_posix(),dst_path)
                        else:
                            shutil.move(filename.as_posix(),dst_path)
                        revert_src.append(filename.as_posix())
                        revert_dst.append(dst_path)
                        do_flag = True
                        break
                if do_flag:
                    break
                else:
                    print('invalid key')

            # if is_relist:
            #     break
            img_num+=1
            cur_time = time.time()
            avg_time = (cur_time - start_time)/img_num
            print('do annotation {} , average cost time {} minute/10000张'.format(img_num,avg_time*10000//60))
        if is_empty:
            break
    cv2.destroyAllWindows()