import os
import numpy as np
import cv2

def phash(path):
    # 加载并调整图片为32*32的灰度图片
    img = cv2.imread(path)
    img1 = cv2.resize(img, (32, 32))
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    # 创建二维列表
    h, w = img1.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img1
    # vis0 = vis0/255
    # DCT二维变换
    # 离散余弦变换，得到dct系数矩阵
    img_dct = cv2.dct(vis0)
    img_dct = img_dct[0:8,0:8]
    # img_dct = cv2.dct(vis0)
    # img_dct = cv2.resize(img_dct,(8,8))
    # 把list变成一维list
    img_list = img_dct.reshape(-1).tolist()
    # 计算均值
    img_mean = img_dct.mean()
    avg_list = ['0' if i<img_mean else '1' for i in img_list]
    print(avg_list)
    return ''.join(['%x' % int(''.join(avg_list[x:x+4]),2) for x in range(0,64,4)])
def ham_dist(x, y):
    # return bin(x ^ y).count('1')
    assert len(x) == len(y)
    return sum([ch1 != ch2 for ch1, ch2 in zip(x, y)])

if __name__ == '__main__':
    path1 = '/media/hzh/ssd_disk/Traffic/traffic_split_data_1208_1301_1345_by1213/1208X/340221000000050001_3402210100046899_1208X_02_null_B69BA1_20191025114954_0_1_a.jpg'
    path2 = '/media/hzh/ssd_disk/Traffic/traffic_split_data_1208_1301_1345_by1213/1208X/340221000000050001_3402210100046899_1208X_02_null_B69BA1_20191025114954_0_1_b.jpg'
    path3 = '/media/hzh/ssd_disk/Traffic/traffic_split_data_1208_1301_1345_by1213/1208X/340221000000050001_3402210100046899_1208X_02_null_B69BA1_20191025114954_0_1_c.jpg'
    path4 = '/media/hzh/ssd_disk/Traffic/traffic_split_data_1208_1301_1345_by1213/1208X/340221000000050001_3402210100046899_1208X_02_null_B69BA1_20191025114954_0_1_d.jpg'
    feature1 = phash(path1)
    feature2 = phash(path2)
    feature3 = phash(path3)
    feature4 = phash(path4)
    print(ham_dist(feature1,feature2))
    print(ham_dist(feature2, feature3))
    print(ham_dist(feature2, feature4))
    print(phash(path1))
    print(phash(path2))
    print(phash(path3))
    print(phash(path4))