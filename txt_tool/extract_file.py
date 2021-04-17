import txt_tool.common as common
import os
#提取文件中的目标行，并保存到另一文件中

if __name__ == '__main__':
    src_path = '/media/hzh/work/data/stardard_test_data/1208'
    src_file = os.path.join(src_path,'1208_keep_result_last.txt')
    dst_file = os.path.join(src_path,'error.txt')
    dst_str = common.searchTxtFile(src_file,'#1#E')
    with open(dst_file,'wt') as f:
        f.writelines(dst_str)