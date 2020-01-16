import os
import csv
import shutil
import codecs

result_file=r'/home/hzh/超速.csv'
f = codecs.open(result_file,'r',encoding='GBK')
# f = open(result_file,'r')
lines = csv.reader(f)
target_path = r''

for l in lines:
    hphm = l[3]
    cu_filename = l[4]
    base_filename = os.path.split(cu_filename)[1]
    base_name,suffix = os.path.splitext(base_filename)
    res = l[6]
    new_filename = '{}_{}_{}{}'.format(base_name,hphm,res,suffix)
    new_filename.encode('utf-8').decode('utf-8')
    new_filename.replace('已上传','keep')
    new_filename.replace('已删除','delete')

    full_old_file = os.path.join(target_path,base_filename)
    full_new_file = os.path.join(target_path,new_filename)
    print(full_new_file)

    # shutil.move(full_old_file,full_new_file)
    # print('copy {} to {}'.format(full_old_file,full_new_file))




