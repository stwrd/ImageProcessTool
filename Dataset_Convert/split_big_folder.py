#将一个大文件夹夹中的图片拆分到小的文件夹中，加快文件加载速度
import os
from pathlib import Path
import shutil
import cv2
max_limit = 1000  #一个文件夹下的最大图片数量

def search_all_folder(input_path):
    totalfolders = []
    for root,dirs,files in os.walk(input_path):
        totalfolders.append(root)
    return totalfolders

if __name__ == '__main__':
    target_folder = '/media/hzh/docker_disk/dataset/traffic/交通违法第一次通用标注/Annotations'
    out_folder = '/media/hzh/docker_disk/dataset/traffic/交通违法第一次通用标注/data2'

    total_folders = search_all_folder(target_folder)
    for sub_folder in total_folders:
        total_files = Path(sub_folder).glob('*.[jJ][pP][gG]')
        total_files = [f for f in total_files]

        #替换为out_folder
        image_save_path = sub_folder.replace(target_folder,out_folder)
        Path(image_save_path).mkdir(exist_ok=True)

        order_num = 1
        if len(total_files) != 0:
            image_save_path_order = os.path.join(image_save_path, '{:0>5}'.format(order_num))
            Path(image_save_path_order).mkdir(exist_ok=True)
        cur_num = 0
        for filename in total_files:
            if cur_num >= max_limit:
                order_num += 1
                image_save_path_order = os.path.join(image_save_path, '{:0>5}'.format(order_num))
                Path(image_save_path_order).mkdir(exist_ok=True)
                cur_num = 0
            image = cv2.imread(filename.as_posix())
            if image is None:
                print('read image failed')
                continue
            pre_file_path = filename.as_posix()
            pre_json_path = os.path.splitext(pre_file_path)[0]+'.json'
            pre_txt_path = os.path.splitext(pre_file_path)[0]+'.txt'
            pre_xml_path = os.path.splitext(pre_file_path)[0]+'.xml'
            # if not os.path.exists(pre_json_path):#仅当json和jpg同时存在时才移动
            #     continue
            basename = os.path.split(pre_file_path)[1]
            post_file_path = os.path.join(image_save_path_order,basename.lower())#文件名全转换为小写
            post_json_path = (os.path.splitext(post_file_path)[0]+'.json')
            post_txt_path = (os.path.splitext(post_file_path)[0]+'.txt')
            post_xml_path = (os.path.splitext(post_file_path)[0]+'.xml')

            # if os.path.exists(pre_json_path):
            #     shutil.move(pre_json_path,post_json_path)
            # else:
            #     continue
            shutil.move(pre_file_path, post_file_path)
            if os.path.exists(pre_txt_path):
                shutil.move(pre_txt_path,post_txt_path)
            # cv2.imwrite(post_file_path,image)
            if os.path.exists(pre_xml_path):
                shutil.copy(pre_xml_path,post_xml_path)
                # shutil.move(pre_xml_path,post_xml_path)
            print('cp {} to {}'.format(pre_file_path,post_file_path))
            cur_num += 1