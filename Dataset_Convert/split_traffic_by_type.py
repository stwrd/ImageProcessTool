#按照合成模式分类，相同合成模式的放入同一个文件夹
#分割交通违法数据集
import os
import numpy as np
import shutil
from PIL import Image
from PIL import ImageFile

def isvalid_symbol(code):
    if ord(code) >=32 and ord(code) <=122:
        return True
    else:
        return False
tar_path = '/media/hzh/work/data/wuxi_new_data1'
dst_path = '/media/hzh/work/data/hcms1'


subfolders1 = [ os.path.join(tar_path,subfolder) for subfolder in os.listdir(tar_path) if os.path.isdir(os.path.join(tar_path,subfolder))]
for subfolder1 in subfolders1:
    subfolders2 = [os.path.join(subfolder1,subfolder) for subfolder in os.listdir(subfolder1) if os.path.isdir(os.path.join(subfolder1,subfolder)) and ('1345' in subfolder or '1208' in subfolder or '1301' in subfolder)]#1345
    for subfolder2 in subfolders2:
        print(subfolder2)
        if '1345' in os.path.split(subfolder2)[1]:
            # os.makedirs(os.path.join(dst_path, '1345'),exist_ok=True)
            shutil.copytree(subfolder2, subfolder2.replace(tar_path,dst_path))
        # if '1301' in os.path.split(subfolder2)[1]:
        #     os.makedirs(os.path.join(dst_path, '1301'),exist_ok=True)
        #     shutil.copytree(subfolder2, os.path.join(dst_path, '1301'))
        # if '1208' in os.path.split(subfolder2)[1]:
        #     # os.makedirs(os.path.join(dst_path, '1345'),exist_ok=True)
        #     shutil.copytree(subfolder2, os.path.join(dst_path, '1208'))

