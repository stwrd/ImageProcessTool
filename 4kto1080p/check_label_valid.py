import os
import numpy as np
import warnings
warnings.filterwarnings('ignore')
if __name__ == '__main__':
    tar_path = r'H:\mclz\0724_kitchen'
    filelist = os.listdir(tar_path)
    filelist = [os.path.join(tar_path, filename) for filename in filelist if filename.endswith('.txt')]
    for filename in filelist:
        labels = np.loadtxt(filename, dtype=np.float32).reshape(-1, 5)
        for label in labels:
            if np.sum(label[1:] < 0):
                print(filename)
                print(label)