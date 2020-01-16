import os
import cv2
import numpy as np

start_idx = 1
PREDEFINE_LEN = 9

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
        B = (img_list[0]+img_list[1])/2
        G = (img_list[2] + img_list[3]) / 2
        R = (img_list[4] + img_list[5]) / 2

        standard_with = B.shape[1]
        standard_height = B.shape[0]

        bgr_img = np.array([B,G,R],np.uint8).transpose((1,2,0)).copy()
        dst_path = os.path.join(dst_dir,'data','%05d.png' %start_idx)
        if not os.path.exists(os.path.join(dst_dir,'data')):
            os.makedirs(os.path.join(dst_dir,'data'))

        #for label in labels:
        #    cv2.rectangle(bgr_img,(label[0],label[1]),(label[2],label[3]),(255,0,0),2)
        cv2.imwrite(dst_path,bgr_img)

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
        dst_label_path = dst_path.replace('.png','.txt')
        np.savetxt(dst_label_path,labels,fmt='%0.5f')

    def start(self):
        if os.path.exists(self.label_path) or os.path.exists(self.label_path_cls):
            video_cap = cv2.VideoCapture(self.Path)
            frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = video_cap.get(cv2.CAP_PROP_FPS)
            fps = np.ceil(fps)

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            vw = cv2.VideoWriter(os.path.join(self.dst_dir,'throw_detect_demo.mp4'), fourcc, fps,(frame_width, frame_height))

            frame_list = []
            frame_cp_list = []
            global start_idx
            cur_idx = 0
            while True:
                is_read,img = video_cap.read()
                if is_read:
                    frame_list.append(img)
                    if len(frame_list) == PREDEFINE_LEN:
                        labels = self._all_boxes[self._all_boxes[:, 0] == cur_idx][:, 1:]
                        labels = labels.astype('int')
                        if labels.shape[0] != 0:
                            frame_cp_list.clear()
                            for frame in frame_list:
                                frame_cp = frame.copy()
                                for label in labels:
                                    cv2.putText(frame_cp,'throw',(label[0], label[1]-10),0,2,[0,0,255],2)
                                    cv2.rectangle(frame_cp, (label[0], label[1]), (label[2], label[3]), (0, 0, 255), 2)
                                frame_cp_list.append(frame_cp)

                        if len(frame_cp_list) != 0:
                            for frame in frame_cp_list[:1]:
                                vw.write(frame)
                                frame_cp_list = frame_cp_list[1:]
                        else:
                            for frame in frame_list[:1]:
                                vw.write(frame)
                        frame_list = frame_list[1:]
                        cur_idx += 1
                else:
                    vw.release()
                    break

if __name__ == '__main__':
    tar_path = r'/media/hzh/work/workspace/data/data_throw/make_demo/throw'
    label_path = r'/media/hzh/work/workspace/data/data_throw/make_demo/throw_label'
    dst_dir = r'/media/hzh/work/workspace/data/data_throw/make_demo'

    sub_video_list = os.listdir(tar_path)
    suffix = '.mp4'
    for i, sub_video in enumerate(sub_video_list):
        if sub_video.endswith(suffix):
            print("process " + sub_video + "..")
            full_sub_video = os.path.join(tar_path, sub_video)
            instance_ = generating(full_sub_video,label_path,dst_dir)
            instance_.start()