#将一个大文件夹夹中的图片拆分到小的文件夹中，加快文件加载速度
import os
from pathlib import Path
import shutil
max_limit = 1000  #一个文件夹下的最大图片数量
if __name__ == '__main__':
    target_folder = '/media/hzh/docker_disk/dataset/交通违法压线分类标注/small_yx/small_yx'
    order_num = 1
    image_save_path = os.path.join(target_folder, '{:0>5}'.format(order_num))
    os.makedirs(image_save_path,exist_ok=True)
    cur_num = 0
    total_files = Path(target_folder).rglob('*.jpg')
    total_files = [f for f in total_files]
    for filename in total_files:
        if cur_num >= max_limit:
            order_num += 1
            image_save_path = os.path.join(target_folder, '{:0>5}'.format(order_num))
            Path(image_save_path).mkdir(exist_ok=True)
            cur_num = 0
        pre_file_path = filename.as_posix()
        pre_json_path = pre_file_path.replace('.jpg', '.json')
        pre_txt_path = pre_file_path.replace('.jpg','.txt')
        pre_xml_path = pre_file_path.replace('.jpg','.xml')
        # if not os.path.exists(pre_json_path):#仅当json和jpg同时存在时才移动
        #     continue
        basename = os.path.split(pre_file_path)[1]
        post_file_path = os.path.join(image_save_path,basename)
        post_json_path = post_file_path.replace('.jpg', '.json')
        post_txt_path = post_file_path.replace('.jpg', '.txt')
        post_xml_path = post_file_path.replace('.jpg', '.xml')
        shutil.move(pre_file_path,post_file_path)
        shutil.move(pre_json_path,post_json_path)
        if os.path.exists(pre_txt_path):
            shutil.move(pre_txt_path,post_txt_path)
        if os.path.exists(pre_xml_path):
            shutil.move(pre_xml_path,post_xml_path)
        print('move {} to {}'.format(pre_file_path,post_file_path))
        cur_num += 1