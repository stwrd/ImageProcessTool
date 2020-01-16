import cv2
import os


#颠倒图像并保存
src_path = r'H:\Traffic\Dataset\lanemark_data\neg'
dst_path = r'H:\Traffic\Dataset\lanemark_data\pos_test'
os.makedirs(dst_path,exist_ok=True)

filename_list = [filename for filename in os.listdir(src_path) if filename.endswith('.jpg')]
full_filename_list = [os.path.join(src_path,filename) for filename in filename_list]

for i,full_filename in enumerate(full_filename_list):
    im = cv2.imread(full_filename)
    r_im = im[::-1,...]
    dst_filename = os.path.join(dst_path,filename_list[i]).replace('.jpg','_r.jpg')
    cv2.imwrite(dst_filename,r_im)
    print(dst_filename)
