import os
import cv2
import numpy as np
import numba
start_idx = 1
PREDEFINE_LEN = 12

class generating:
    def __init__(self, path, label_path, dst_dir):
        self.Path = path  #####视频路径
        self.base_name = os.path.basename(self.Path)
        self.base_name = os.path.splitext(self.base_name)[0]
        self.label_path = os.path.join(label_path, self.base_name + '.txt')#bbox 文件
        self.label_path_cls = os.path.join(label_path, self.base_name + '_cls' + '.txt')#分类文件
        self.dst_dir = dst_dir
        os.makedirs(self.dst_dir,exist_ok=True)

        if os.path.exists(self.label_path):
            self._all_boxes = np.loadtxt(self.label_path,dtype='int')
            self._all_boxes = self._all_boxes.reshape([-1,5])
        else:
            print('this video has none box annotation')
        if os.path.exists(self.label_path_cls):
            self._all_cls = np.loadtxt(self.label_path_cls,dtype='int')
            self._all_cls = self._all_cls.reshape([-1,1])
        else:
            print('this video has none cls annotation')
    def generate_single_sample(self,img_list,labels):

        B = np.zeros_like(img_list[0])
        G = np.zeros_like(img_list[0])
        R = np.zeros_like(img_list[0])
        for i in range(4):
            B += img_list[i]
            G += img_list[i+PREDEFINE_LEN//3]
            R += img_list[i+PREDEFINE_LEN*2//3]
        B = B/4.0
        G = G/4.0
        R = R/4.0

        standard_with = B.shape[1]
        standard_height = B.shape[0]

        bgr_img = np.array([B,G,R],np.uint8).transpose((1,2,0)).copy()
        dst_path = os.path.join(dst_dir,'data','%05d.jpg' %start_idx)
        if not os.path.exists(os.path.join(dst_dir,'data')):
            os.makedirs(os.path.join(dst_dir,'data'))

        #for label in labels:
        #    cv2.rectangle(bgr_img,(label[0],label[1]),(label[2],label[3]),(255,0,0),2)
        cv2.imwrite(dst_path,bgr_img)

        if labels is not None:
            middle_x = (labels[:,0] + labels[:,2])/2
            middle_y = (labels[:,1] + labels[:,3])/2
            labels[:,2] = labels[:,2] - labels[:,0]
            labels[:,3] = labels[:,3] - labels[:,1]
            labels[:,0] = middle_x
            labels[:,1] = middle_y
            labels[:,[0,2]] /= standard_with
            labels[:,[1,3]] /= standard_height

            add_cls = np.zeros([labels.shape[0],1],np.int32)
            labels = np.concatenate((add_cls,labels),axis=1)
            dst_label_path = dst_path.replace('.jpg','.txt')
            with open(dst_label_path,'w') as outfile:
                for label in labels:
                    outfile.write('{} {:.4} {:.4} {:.4} {:.4}\n'.format(int(label[0]),label[1],label[2],label[3],label[4]))
        else:
            dst_label_path = dst_path.replace('.jpg', '.txt')
            out_file = open(dst_label_path, 'w')
            out_file.close()

    def start(self):
        global start_idx
        if os.path.exists(self.label_path) or os.path.exists(self.label_path_cls):
            video_cap = cv2.VideoCapture(self.Path)
            frame_list = []
            cur_idx = 0
            while True:
                is_read,img = video_cap.read()
                if is_read:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    gray = gray.astype(np.float32)
                    frame_list.append(gray)
                    if len(frame_list) == PREDEFINE_LEN:
                        if self._all_cls[cur_idx] != -1:
                            labels = self._all_boxes[self._all_boxes[:, 0] == cur_idx][:, 1:]
                            labels = labels.astype('float32')
                            self.generate_single_sample(frame_list,labels)
                            start_idx = start_idx + 1

                        frame_list = frame_list[1:]
                        cur_idx += 1
                else:
                    break
        else:
            video_cap = cv2.VideoCapture(self.Path)
            frame_list = []
            cur_idx = 0
            while True:
                is_read,img = video_cap.read()
                if is_read:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    gray = gray.astype(np.float32)
                    frame_list.append(gray)
                    if len(frame_list) == PREDEFINE_LEN:
                        labels = None
                        self.generate_single_sample(frame_list,labels)
                        start_idx = start_idx + 1
                        frame_list = frame_list[12:]
                        cur_idx += 12
                else:
                    break

if __name__ == '__main__':
    tar_path = r'/media/hzh/docker_disk/dataset/data_throw/throw_neg/video/1'
    label_path = r'/media/hzh/docker_disk/dataset/data_throw/throw_neg/video_label'
    dst_dir = r'/media/hzh/docker_disk/dataset/data_throw/throw_neg'

    sub_video_list = os.listdir(tar_path)
    suffix = '.mp4'
    for i, sub_video in enumerate(sub_video_list):
        if sub_video.endswith(suffix) or sub_video.endswith('.flv'):
            print("process " + sub_video + "..")
            full_sub_video = os.path.join(tar_path, sub_video)
            instance_ = generating(full_sub_video,label_path,dst_dir)
            instance_.start()