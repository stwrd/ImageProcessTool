import json
import sys
import cv2
import numpy as np
import os
font = cv2.FONT_HERSHEY_SIMPLEX

class boxing:
    def __init__(self, path, label_path):
        self.Path = path  #####图片文件夹路径
        self.draw = False  #####画框的标志
        self.pt0 = None  #####矩形框左上角坐标
        self.pt1 = None  #####矩形框右下角坐标
        self._boxes = np.zeros([0,4],dtype='float')  #####用来存储每一个框的坐标信息
        self.base_name = os.path.basename(self.Path)
        self.base_name = os.path.splitext(self.base_name)[0]
        self.label_path = os.path.join(label_path, self.base_name + '.json')#bbox 文件

        self.img = cv2.imread(self.Path)
        self.height,self.width,_ = self.img.shape
        if os.path.exists(self.label_path):
            with open(self.label_path) as f:
                label_json = json.load(f)
                normalize_boxes = label_json["roi_detail"]
                for box in normalize_boxes:
                    box = np.array(box)
                    box[[0,2]] = box[[0,2]]*self.width
                    box[[1,3]] = box[[1,3]]*self.height
                    self._boxes = np.concatenate((self._boxes,box.reshape(1,4)))
                print('label:',self._boxes)
    def _on_mouse(self, event, x, y, flags, para):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.draw = True
            self.pt0 = np.array([max(x,0),max(0,y)])
        elif event == cv2.EVENT_LBUTTONUP:
            self.draw = False
            self.pt1 = np.array([min(self.width,x),min(self.height,y)])
            xx = np.concatenate((self.pt0,self.pt1),0).reshape([1,4])
            # self._boxes.append(np.concatenate((self.pt0,self.pt1),0))
            self._boxes = np.concatenate((self._boxes,xx))

        elif event == cv2.EVENT_MOUSEMOVE:  #########鼠标移动的时候把画框轨迹显示出来
            self.pt1 = np.array([x,y])

    def _drawing_box(self, img):
        canvas = cv2.copyMakeBorder(img, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=(192, 192, 192))
        for box in self._boxes:
            bpt0 = (int(box[0]),int(box[1]))
            bpt1 = (int(box[2]),int(box[3]))
            cv2.rectangle(canvas, bpt0, bpt1, (255, 0, 0), 4)

        ###画每一个框显示轨迹
        if self.draw:
            cv2.rectangle(canvas, tuple(self.pt0), tuple(self.pt1), (255, 0, 0), thickness=4)
        return canvas

    def start(self):
        continue_anno = True
        win_name = "action_window"
        cv2.namedWindow(win_name,0)
        cv2.setMouseCallback(win_name, self._on_mouse)
        while continue_anno:
            cp_img = self.img.copy()
            cp_img = self._drawing_box(cp_img)
            cv2.imshow(win_name, cp_img)
            k = cv2.waitKey(200)
            if k == ord('s'):
                t_boxes = np.array(self._boxes)
                tmp_boxes_w = t_boxes[:,[0,2]]
                tmp_boxes_h = t_boxes[:,[1,3]]
                # 调换位置
                for child_box in tmp_boxes_w:
                    if child_box[0] > child_box[1]:
                        child_box[0], child_box[1] = child_box[1], child_box[0]
                for child_box in tmp_boxes_h:
                    if child_box[0] > child_box[1]:
                        child_box[0], child_box[1] = child_box[1], child_box[0]
                t_boxes[:,[0,2]] = tmp_boxes_w
                t_boxes[:,[1,3]] = tmp_boxes_h

                if t_boxes.shape[0] != 0:
                    with open(self.label_path, 'w') as f:
                        normalize_boxes = np.zeros_like(t_boxes,'float32')
                        normalize_boxes[:,[0,2]] = t_boxes[:, [0, 2]] / float(self.width)
                        normalize_boxes[:,[1,3]] = t_boxes[:, [1, 3]] / float(self.height)
                        labels = {"roi_detail":normalize_boxes.tolist()}
                        # json.dump(labels, f, indent=4, separators=(',', ':'))
                        json.dump(labels, f)
                        continue_anno = False

            if k == ord('c'):
                self._boxes = np.zeros([0, 4], dtype='int')
            if k == ord('q'):
                continue_anno = False
                return -1
            # cv2.destroyAllWindows()
if __name__ == '__main__':
    img_folder = sys.argv[1]
    img_paths = os.listdir(img_folder)
    img_paths = [os.path.join(img_folder,img_path) for img_path in img_paths if img_path.endswith('.jpg')]
    for img_path in img_paths:
        instance_ = boxing(img_path,img_folder)
        res = instance_.start()
        if res == -1:
            break