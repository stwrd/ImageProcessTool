import os
import sys
import cv2
import shutil

result_file=r'H:\Traffic\测试数据\result_1301.txt'
ceshi_folder=r'H:\Traffic\测试数据\1301\1301'
wrong_delete=r'H:\Traffic\测试数据\平安1301\不该删却删'
fail_delete=r'H:\Traffic\测试数据\平安1301\该删除但没删'

delete_folder=r'H:\Traffic\测试数据\平安1301\应该删除'
keep_folder=r'H:\Traffic\测试数据\平安1301\应该保留'
os.makedirs(delete_folder,exist_ok=True)
os.makedirs(keep_folder,exist_ok=True)

f=open(result_file,encoding='UTF-8')
results=f.readlines()
f.close()

deleted=[]
for result in results:
    print(result)
    if result.split('#')[1]=='1':
        deleted.append(result.split('#')[0]+'.jpg')

print('deleted: ',len(deleted))

deleted=set(deleted)

wrong_deleteds=os.listdir(wrong_delete)
wrong_deleteds=[ wrong_deleted for wrong_deleted in wrong_deleteds]
print('wrong_deleted:',len(wrong_deleteds))

wrong_deleteds=set(wrong_deleteds)


fail_deleteds=os.listdir(fail_delete)
fail_deleteds=[ fail_deleted for fail_deleted in fail_deleteds]
print('fail_deleteds:',len(fail_deleteds))

fail_deleteds=set(fail_deleteds)



true_deletes=deleted.union(fail_deleteds).difference(wrong_deleteds)
print('true_deletes:',len(true_deletes))

all_imgs=os.listdir(ceshi_folder)

'''
for true_delete in true_deletes:
    if not true_delete in all_imgs:
        print(true_delete)
'''
for img_name in all_imgs:
    # print(os.path.join(ceshi_folder,img_name))
    src_path = os.path.join(ceshi_folder,img_name)
    if img_name in true_deletes:
        dst_path = os.path.join(delete_folder,img_name)
        shutil.copy(src_path,dst_path)
    else:
        dst_path = os.path.join(keep_folder,img_name)
        shutil.copy(src_path,dst_path)






