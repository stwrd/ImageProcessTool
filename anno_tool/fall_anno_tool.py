import os
import cv2
import shutil
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX
PREDEFINE_LEN = 6
STRIDE = 6

class boxing:
    def __init__(self, path, label_path):
        self.Path = path  #####视频路径
        self.draw = False  #####画框的标志
        self.pt0 = None  #####矩形框左上角坐标
        self.pt1 = None  #####矩形框右下角坐标
        self._boxes = np.zeros([0,4],dtype='int')  #####用来存储每一个框的坐标信息
        self._all_boxes = np.zeros([0,5],dtype='int')
        self._all_cls = np.zeros([0],dtype='int')
        self.base_name = os.path.basename(self.Path)
        self.base_name = os.path.splitext(self.base_name)[0]
        self.label_path = os.path.join(label_path, self.base_name + '.txt')#bbox 文件
        self.cur_idx = 0
        self.cur_len = 0
        self.ratio = 1
        if os.path.exists(self.label_path):
            self._all_boxes = np.loadtxt(self.label_path,dtype='float32')
            self._all_boxes = self._all_boxes.reshape([-1,5])

    def _on_mouse(self, event, x, y, flags, para):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.draw = True
            self.pt0 = np.array([x,y])
        elif event == cv2.EVENT_LBUTTONUP:
            self.draw = False
            self.pt1 = np.array([x,y])
            xx = np.concatenate((self.pt0,self.pt1),0).reshape([1,4]).astype('float')
            xx[:,[0,2]] = xx[:,[0,2]] / self.show_width
            xx[:,[1,3]] = xx[:,[1,3]] / self.show_height
            # self._boxes.append(np.concatenate((self.pt0,self.pt1),0))
            self._boxes = np.concatenate((self._boxes,xx))
        elif event == cv2.EVENT_MOUSEMOVE:  #########鼠标移动的时候把画框轨迹显示出来
            self.pt1 = np.array([x,y])

    def _drawing_box(self, img):
        canvas = cv2.copyMakeBorder(img, 0, 16, 0, 0, cv2.BORDER_CONSTANT, value=(192, 192, 192))
        anno_progress = str(self.cur_idx) + '/' + str(self.cur_len - PREDEFINE_LEN)
        cv2.putText(canvas,anno_progress,(0,50),font,2,(0,255,0),2)

        if len(self._boxes) == 0:
            cv2.putText(canvas,'NEG',(img.shape[1]//2,img.shape[0]//2),font,2,(0,255,0),2)
        else:
            cv2.putText(canvas,'POS',(img.shape[1]//2,img.shape[0]//2),font,2,(0,0,255),2)

        for box in self._boxes:
            bpt0 = (int(box[0]*img.shape[1]),int(box[1]*img.shape[0]))
            bpt1 = (int(box[2]*img.shape[1]),int(box[3]*img.shape[0]))
            cv2.rectangle(canvas, bpt0, bpt1, (255, 0, 0), 2)

        ###画每一个框显示轨迹
        if self.draw:
            cv2.rectangle(canvas, tuple(self.pt0), tuple(self.pt1), (255, 0, 0), thickness=2)
        return canvas

    def start(self):
        #加载所有的视频
        video_cap = cv2.VideoCapture(self.Path)
        frame_list = []
        ratio = 1
        standard_height = 0
        standard_width = 1
        while True:
            is_read,img = video_cap.read()
            if is_read:
                ratio = 600.0 / max(img.shape[1], img.shape[0])
                standard_height = img.shape[0]
                standard_width = img.shape[1]
                img = cv2.resize(img, (int(float(img.shape[1]) * ratio), int(float(img.shape[0]) * ratio)))
                self.show_width,self.show_height = img.shape[1],img.shape[0]
                frame_list.append(img)
            else:
                break
        self.ratio = ratio
        self.cur_len = len(frame_list)
        continue_anno = True
        win_name = "action_window"
        cv2.namedWindow(win_name)
        cv2.setMouseCallback(win_name, self._on_mouse)
        while continue_anno:
            img_stack = []
            for i in range(PREDEFINE_LEN):
                img_stack.append(frame_list[self.cur_idx+i])

            loop = True

            ##重新读入label
            self._boxes = self._all_boxes[self._all_boxes[:, 0] == self.cur_idx][:, 1:]

            while loop:
                for s_img in img_stack:
                    cp_img = s_img.copy()
                    cp_img = self._drawing_box(cp_img)
                    cv2.imshow(win_name, cp_img)
                    k = cv2.waitKey(200)
                    if k == ord('s'):
                        t_boxes = np.array(self._boxes)
                        t_boxes[t_boxes<0] = 0
                        tmp_boxes_w = t_boxes[:,[0,2]]
                        tmp_boxes_h = t_boxes[:,[1,3]]
                        # 调换位置
                        for child_box in tmp_boxes_w:
                            if child_box[0] > child_box[1]:
                                child_box[0], child_box[1] = child_box[1], child_box[0]
                        for child_box in tmp_boxes_h:
                            if child_box[0] > child_box[1]:
                                child_box[0], child_box[1] = child_box[1], child_box[0]
                        tmp_boxes_w[tmp_boxes_w>=standard_width] = standard_width-1
                        tmp_boxes_h[tmp_boxes_h>=standard_height] = standard_height-1
                        t_boxes[:,[0,2]] = tmp_boxes_w
                        t_boxes[:,[1,3]] = tmp_boxes_h
                        add_idx = np.ones([t_boxes.shape[0],1],dtype='int')*self.cur_idx
                        t_boxes = np.concatenate((add_idx,t_boxes),1)
                        self._all_boxes = self._all_boxes[~(self._all_boxes[:, 0] == self.cur_idx)]
                        if t_boxes.shape[0] != 0:
                            self._all_boxes = np.concatenate((self._all_boxes,t_boxes),0)
                        print(self._all_boxes)
                        with open(self.label_path,mode='w') as f:
                            for sbox in self._all_boxes:
                                f.write(str(int(sbox[0])) + " " +" ".join(['{:.3f}'.format(a) for a in sbox[1:]]) + '\n')
                        loop = False
                        break
                    if k == ord('c'):
                        self._boxes = np.zeros([0, 4], dtype='int')
                        break

                    if k == ord('a'):
                        self.cur_idx -= STRIDE
                        self.cur_idx = max(0,self.cur_idx)
                        loop = False
                        break
                    if k == ord('d'):
                        self.cur_idx += STRIDE
                        if self.cur_idx + PREDEFINE_LEN > len(frame_list):
                            self.cur_idx -= STRIDE
                        loop = False
                        break
                    if k == ord('q'):
                        loop = False
                        continue_anno = False
                        break
            # cv2.destroyAllWindows()


if __name__ == '__main__':
    tar_path = r'/media/hzh/NO.1/fall/fall20200617/fall20200617'
    label_path = tar_path+'_label'

    os.makedirs(label_path,exist_ok=True)
    sub_video_list = os.listdir(tar_path)
    suffix = '.mp4'
    for i, sub_video in enumerate(sub_video_list):
        if sub_video.endswith(suffix):
            print(i + 1, "--->%d" % len(sub_video_list))
            full_sub_video = os.path.join(tar_path, sub_video)
            instance_ = boxing(full_sub_video,label_path)
            instance_.start()
