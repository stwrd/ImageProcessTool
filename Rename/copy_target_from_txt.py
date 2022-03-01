#从文件中读取文件列表，复制到另一个文件夹中
import os
import shutil
def copy_from_txt(filename,src_folder,target_folder):
    with open(filename,'r') as f:
        for line in f:
            line = line.strip('\n')
            _,target_filename = os.path.split(line)
            os.makedirs(target_folder,exist_ok=True)
            shutil.copy(os.path.join(src_folder,line),os.path.join(target_folder,target_filename))

if __name__ == '__main__':
    copy_from_txt('data/test.txt',
                  '',
                  'samples')