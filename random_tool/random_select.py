#由于数据过多随机抽取一部分数据进行标注
import os
import shutil
import random
tar_path = '/media/hzh/ssd_disk/Traffic/traffic_split_data_1208_1301_1345_by1213'
dst_path = '/media/hzh/ssd_disk/Traffic/lane_data_1219'

copy_cnt = 0

def save_images_to_target_folder(images, input_path, output_path):
    images1 = images.copy()
    images1 = random.sample(images1,int(len(images1)*0.4))
    for input_image in images1:
        # folder,filename = os.path.split(input_images)
        output_image = input_image.replace(input_path,output_path)
        os.makedirs(os.path.split(output_image)[0],exist_ok=True)
        shutil.copy(input_image,output_image)
        print('copy {} to {}'.format(input_image,output_image))
        global copy_cnt
        copy_cnt += 1

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
    return images


if __name__ == '__main__':
    search_all_images(tar_path,dst_path)
    print('total copy:',copy_cnt)