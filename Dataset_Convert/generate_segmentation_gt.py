#将标签图像转换为语义分割的mask
import cv2
import os

tar_path = r'H:\Traffic\SYNTHIA-SF'

def generate_mask(gtfilenamelist,maskfilenamelist):
    for filename,maskfilename in zip(gtfilenamelist,maskfilenamelist):
        gt = cv2.imread(filename)
        label = gt[:,:,-1]
        label[label != 20] = 0
        label[label==20] = 1
        cv2.imwrite(maskfilename,label)
num = 6
for i in range(num):
    subpath = os.path.join(tar_path,'SEQ{}'.format(i+1))
    thirdpath1 = os.path.join(subpath,'RGBLeft')
    thirdpath2 = os.path.join(subpath,'RGBRight')
    maskpath1 = os.path.join(subpath,'MaskLeft')
    os.makedirs(maskpath1,exist_ok=True)
    maskpath2 = os.path.join(subpath,'MaskRight')
    os.makedirs(maskpath2,exist_ok=True)
    filenamelist1 = [os.path.join(thirdpath1, filename) for filename in os.listdir(thirdpath1) if
                     filename.endswith('.png')]
    gtfilenamelist1 = [filename.replace('RGBLeft','GTLeft') for filename in filenamelist1]
    maskfilenamelist1 = [filename.replace('RGBLeft', 'MaskLeft') for filename in filenamelist1]
    filenamelist2 = [os.path.join(thirdpath2, filename) for filename in os.listdir(thirdpath2) if
                     filename.endswith('.png')]
    gtfilenamelist2 = [filename.replace('RGBRight', 'GTright') for filename in filenamelist2]
    maskfilenamelist2 = [filename.replace('RGBRight', 'MaskRight') for filename in filenamelist2]
    generate_mask(gtfilenamelist1,maskfilenamelist1)
    generate_mask(gtfilenamelist2, maskfilenamelist2)
