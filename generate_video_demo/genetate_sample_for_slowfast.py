import os
import cv2
import numpy as np

start_idx = 3758
PREDEFINE_LEN = 36

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
    def generate_single_sample(self,img_list,labels,cls):
        standard_with = img_list[0].shape[1]
        standard_height = img_list[0].shape[0]

        middle_x = (labels[:,0] + labels[:,2])/2
        middle_y = (labels[:,1] + labels[:,3])/2
        labels[:,2] = labels[:,2] - labels[:,0]
        labels[:,3] = labels[:,3] - labels[:,1]
        labels[:,0] = middle_x
        labels[:,1] = middle_y
        global start_idx
        if(len(labels) != 0):
            mm = labels[:,2:].max(1)
            labels[:,2] = mm
            labels[:,3] = mm
            for label in labels:
                x1,y1,x2,y2 = (label[0] - label[2]/2),(label[1] - label[3]/2),(label[0] + label[2]/2),(label[1] + label[3]/2)
                x1,y1,x2,y2 = max(0,x1),max(0,y1),min(standard_with,x2),min(standard_height,y2)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                pos_path = os.path.join(dst_dir, 'pos','%05d.mp4' % start_idx)
                os.makedirs(os.path.join(dst_dir, 'pos'),exist_ok=True)
                print(pos_path)
                vw = cv2.VideoWriter(pos_path, fourcc, 6,(int(x2-x1), int(y2-y1)))
                for image in img_list:
                    roi_img = image[int(y1):int(y2),int(x1):int(x2),:]
                    vw.write(roi_img)
                vw.release()
                start_idx += 1
        else:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            neg_path = os.path.join(dst_dir,'neg','%05d.mp4' % start_idx)
            os.makedirs(os.path.join(dst_dir,'neg'),exist_ok=True)
            print(neg_path)
            vw = cv2.VideoWriter(neg_path, fourcc, 6, (standard_with, standard_height))
            for image in img_list:
                vw.write(image)
            vw.release()
            start_idx += 1

    def start(self):
        if os.path.exists(self.label_path) or os.path.exists(self.label_path_cls):
            video_cap = cv2.VideoCapture(self.Path)
            frame_list = []
            global start_idx
            cur_idx = 0
            while True:
                is_read,img = video_cap.read()
                if is_read:
                    frame_list.append(img)
                    if len(frame_list) == PREDEFINE_LEN:
                        if self._all_cls[cur_idx] != -1:
                            labels = self._all_boxes[self._all_boxes[:, 0] == cur_idx][:, 1:]
                            labels = labels.astype('float32')
                            self.generate_single_sample(frame_list,labels,self._all_cls[cur_idx])

                        frame_list = frame_list[1:]
                        cur_idx += 1
                else:
                    break

if __name__ == '__main__':
    tar_path = r'/media/hzh/ssd_disk/打架标注数据/fight/sp'
    label_path = r'/media/hzh/ssd_disk/打架标注数据/fight/sp_label'
    dst_dir = r'/media/hzh/docker_disk/dataset/data_fight/fight_data_step2'

    sub_video_list = os.listdir(tar_path)
    suffix = '.mp4'
    for i, sub_video in enumerate(sub_video_list):
        if sub_video.endswith(suffix) or sub_video.endswith('.flv'):
            print("process " + sub_video + "..")
            full_sub_video = os.path.join(tar_path, sub_video)
            instance_ = generating(full_sub_video,label_path,dst_dir)
            instance_.start()