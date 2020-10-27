import os
import cv2
import numpy as np

start_idx = 1
PREDEFINE_LEN = 6
anno_num = 0
total_anno = 0

class generating:
    def __init__(self, path, label_path, dst_dir):
        self.Path = path  #####视频路径
        self.base_name = os.path.basename(self.Path)
        self.base_name = os.path.splitext(self.base_name)[0]
        self.label_path = os.path.join(label_path, self.base_name + '.txt')#bbox 文件
        self.dst_dir = dst_dir
        self.target_actions = []
        os.makedirs(self.dst_dir,exist_ok=True)
        global anno_num

        if os.path.exists(self.label_path):
            self._all_boxes = np.loadtxt(self.label_path,dtype='float32')
            self._all_boxes = self._all_boxes.reshape([-1,5])
            self._all_boxes = self._all_boxes[np.argsort(self._all_boxes[:, 0])]
            self.target_actions = self.extract_whole_action(self._all_boxes)
            with open(os.path.join(self.dst_dir,self.base_name + '.txt'),'w') as outfile:
                for action in self.target_actions:
                    anno_num += 1
                    outfile.write('{} {}'.format(int(action[0]),int(action[1])) + " " + " ".join([str(a) for a in action[2:]]) + '\n')
        else:
            print('this video has none box annotation')

    def bbox_iou(self,box1, box2, x1y1x2y2=True, GIoU=False):
        # Returns the IoU of box1 to box2. box1 is 4, box2 is nx4

        # Get the coordinates of bounding boxes
        if x1y1x2y2:
            # x1, y1, x2, y2 = box1
            b1_x1, b1_y1, b1_x2, b1_y2 = box1[0], box1[1], box1[2], box1[3]
            b2_x1, b2_y1, b2_x2, b2_y2 = box2[0], box2[1], box2[2], box2[3]
        else:
            # x, y, w, h = box1
            b1_x1, b1_x2 = box1[0] - box1[2] / 2, box1[0] + box1[2] / 2
            b1_y1, b1_y2 = box1[1] - box1[3] / 2, box1[1] + box1[3] / 2
            b2_x1, b2_x2 = box2[0] - box2[2] / 2, box2[0] + box2[2] / 2
            b2_y1, b2_y2 = box2[1] - box2[3] / 2, box2[1] + box2[3] / 2

        # Intersection area
        inter_area = (min(b1_x2, b2_x2) - max(b1_x1, b2_x1)) * (min(b1_y2, b2_y2) - max(b1_y1, b2_y1))

        # Union Area
        union_area = ((b1_x2 - b1_x1) * (b1_y2 - b1_y1) + 1e-16) + \
                     (b2_x2 - b2_x1) * (b2_y2 - b2_y1) - inter_area

        iou = inter_area / union_area  # iou
        return iou

    def extract_whole_action(self,anno_boxes):
        sorted_anno = anno_boxes[np.argsort(anno_boxes[:, 0])]
        target_actions = np.ones([0,6],'float32')
        global total_anno
        for anno in sorted_anno:
            total_anno += 1
            loc = np.where(target_actions[:,0] == anno[0])#起始帧数值一样
            loc2 = np.where(target_actions[:,1] == anno[0])#结束帧数值相同
            if loc[0].shape[0] == 0:
                if loc2[0].shape[0] == 0:
                    target_action = np.ones([1,6],'float32')
                    target_action[0,0] = anno[0]
                    target_action[0,1] = anno[0]+PREDEFINE_LEN
                    target_action[0,2:6] = anno[1:]
                    target_actions = np.concatenate((target_actions,target_action),axis=0)
                else:
                    cur_actions = target_actions[loc2]
                    is_exist = False#是否为同一个action
                    for cur_action in cur_actions:
                        iou = self.bbox_iou(anno[1:], cur_action[2:])
                        if (iou > 0.1):
                            cur_action[1] = anno[0] + PREDEFINE_LEN
                            cur_action[2], cur_action[3] = min(anno[1], cur_action[2]), min(anno[2], cur_action[3])
                            cur_action[4], cur_action[5] = max(anno[3], cur_action[4]), max(anno[4], cur_action[5])
                            is_exist = True
                    if not is_exist:
                        target_action = np.ones([1,6], 'float32')
                        target_action[0, 0] = anno[0]
                        target_action[0, 1] = anno[0] + PREDEFINE_LEN
                        target_action[0, 2:6] = anno[1:]
                        target_actions = np.concatenate((target_actions, target_action), axis=0)
                    else:
                        target_actions[loc2] = cur_actions
            else:
                target_action = np.ones([1,6], 'float32')
                target_action[0, 0] = anno[0]
                target_action[0, 1] = anno[0] + PREDEFINE_LEN
                target_action[0, 2:6] = anno[1:]
                target_actions = np.concatenate((target_actions, target_action), axis=0)
        return target_actions
    def generate_single_sample(self,img_list,labels):
        standard_with = img_list[0].shape[1]
        standard_height = img_list[0].shape[0]

        global start_idx
        if(len(labels) != 0):
            for label in labels:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                pos_path = os.path.join(dst_dir, 'pos','%05d.mp4' % start_idx)
                os.makedirs(os.path.join(dst_dir, 'pos'),exist_ok=True)
                print(pos_path)
                vw = cv2.VideoWriter(pos_path, fourcc, 6,(standard_with, standard_height))
                for image in img_list:
                    vw.write(image)
                vw.release()
                start_idx += 1

    def start(self):
        if os.path.exists(self.label_path) and len(self.target_actions) != 0:
            video_cap = cv2.VideoCapture(self.Path)
            frame_list = []
            frame_idx = 0
            global start_idx

            action_id = 0
            self.target_actions = self.target_actions[np.argsort(self.target_actions[:, 0])]
            cur_action = self.target_actions[action_id]
            while True:
                is_read,img = video_cap.read()
                if is_read:
                    if frame_idx >= cur_action[0] and frame_idx < cur_action[1]:
                        frame_list.append(img)
                    if len(frame_list) == (cur_action[1]-cur_action[0]) and frame_idx == cur_action[1]:
                        self.generate_single_sample(frame_list,cur_action)
                        frame_list = []
                        action_id += 1
                        cur_action = self.target_actions[action_id]
                    frame_idx += 1
                else:
                    break

if __name__ == '__main__':
    total_tatgets = [r'/media/hzh/NO.6/Q3_RIGHT_newest/Q3/fall/fall20200617/fall20200617',
                     r'/media/hzh/NO.6/Q3_RIGHT_newest/Q3/fall/fall20200618/fall20200618',
                     r'/media/hzh/NO.6/Q3_RIGHT_newest/Q3/fall/fall20200619/fall20200619',
                     r'/media/hzh/NO.6/Q3_RIGHT_newest/Q3/fall/fall20200620/fall20200620',
                     r'/media/hzh/NO.6/Q3_RIGHT_newest/Q3/fall/fall20200621/fall20200621',
                     r'/media/hzh/NO.6/Q3_RIGHT_newest/Q3/fall/fall20200622/fall20200622']
    for tar_path in total_tatgets:
        # tar_path = r'/media/hzh/ssd_disk/摔倒标注数据/fall/fall20200622/fall20200622'
        label_path = tar_path+'_label'
        # label_path = r'/media/hzh/ssd_disk/摔倒标注数据/fall/fall20200622/fall20200622_label'
        # new_label_path = tar_path+'_newlabel'
        dst_dir = tar_path+'_newlabel'

        sub_video_list = os.listdir(tar_path)
        suffix = '.mp4'
        for i, sub_video in enumerate(sub_video_list):
            if sub_video.endswith(suffix) or sub_video.endswith('.flv'):
                print("process " + sub_video + "..")
                full_sub_video = os.path.join(tar_path, sub_video)
                instance_ = generating(full_sub_video,label_path,dst_dir)
                # instance_.start()
    print('total fall action:',anno_num)
    print('total src fall action:',total_anno)