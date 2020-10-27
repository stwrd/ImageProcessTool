#由于部分图片过大，等比例缩小图片分辨率
import os
import shutil
import random
import cv2
tar_path = '/media/hzh/work/out'#图片源文件夹
dst_path = '/media/hzh/work/out1'#目标文件夹
short_side = 720#最短边长

resize_cnt = 0
copy_cnt = 0
bad_image = 0
def resize_image(input_img,short_side = 720):
    h,w,c = input_img.shape
    ratio = short_side / min(h,w)
    if ratio < 1:
        new_shape = [round(h * ratio), round(w * ratio)]
        out_img = cv2.resize(input_img, (new_shape[1], new_shape[0]), interpolation=cv2.INTER_AREA)  # resized, no border
    else:
        out_img = input_img
    return out_img,ratio
def save_images_to_target_folder(images, input_path, output_path):
    global copy_cnt
    global resize_cnt
    global bad_image
    images1 = images.copy()
    for input_image in images1:
        output_image = input_image.replace(input_path,output_path)
        os.makedirs(os.path.split(output_image)[0],exist_ok=True)

        img = cv2.imread(input_image)
        if img is None:
            bad_image += 1
            continue

        s_img,ratio = resize_image(img,short_side=short_side)
        if ratio >= 1:
            # shutil.copy(input_image,output_image)
            print('copy {} to {}'.format(input_image,output_image))
            copy_cnt += 1
        else:
            # cv2.imwrite(output_image,s_img)
            print('resize image ({},{})-->({},{}) ,save to {}'.format(img.shape[1],img.shape[0],s_img.shape[1],s_img.shape[0],output_image))
            resize_cnt += 1

def search_all_images(input_path, output_path):
    subpaths = [ os.path.join(input_path,subpath) for subpath in os.listdir(input_path)]#全路径
    images = []
    for subpath in subpaths:
        if os.path.isdir(subpath):
            sub_output = os.path.join(output_path, os.path.split(subpath)[1])
            sub_images = search_all_images(subpath, sub_output)
            images = images + sub_images
        else:
            if subpath.endswith('.jpg') or subpath.endswith('.png'):
                images.append(subpath)
            else:
                print('invalid image format')
        if len(images) > 1024:
            save_images_to_target_folder(images,input_path,output_path)
            images.clear()

    if len(images) != 0:
        save_images_to_target_folder(images, input_path, output_path)
        images.clear()
    return images


if __name__ == '__main__':
    search_all_images(tar_path,dst_path)
    print('total copy:',copy_cnt)
    print('total resize:', resize_cnt)
    print('total bad image:', bad_image)