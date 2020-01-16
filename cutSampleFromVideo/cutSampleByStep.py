import cv2
import os

#按照固定时间间隔从视频中截取图片
def cutImageFromFolder(videofolder,savefolder,step=25):
    os.makedirs(savefolder,exist_ok=True)
    videolist = os.listdir(videofolder)
    videolist = [os.path.join(videofolder,videoname) for videoname in videolist if videoname.endswith('.mp4') or videoname.endswith('.avi') or videoname.endswith('.MOV')]
    for videoname in videolist:
        print('process {}'.format(videoname))
        cap = cv2.VideoCapture(videoname)
        if cap.isOpened():
            frame_idx = 1
            while True:
                ret, frame = cap.read()
                if ret:
                    if frame_idx%step == 0:
                        basename = os.path.split(videoname)[1]
                        basename_nosuffix = os.path.splitext(basename)[0]
                        # output_folder = os.path.join(savefolder,basename_nosuffix)#为每一个视频单独生成文件夹
                        output_folder = savefolder
                        os.makedirs(output_folder,exist_ok=True)
                        output_path = os.path.join(output_folder,'{}_{:0>4}.jpg'.format(basename_nosuffix,frame_idx))
                        # output_path = os.path.join(output_folder, '{:0>4}.jpg'.format(frame_idx))
                        cv2.imwrite(output_path,frame)
                        print('save {} done'.format(output_path))
                    frame_idx+=1
                else:
                    break

if __name__ == '__main__':
    targetfolder = r'/media/hzh/ssd_disk/打架标注数据/fight-detection-surv-dataset-master/noFight'
    savefoler = r'/media/hzh/ssd_disk/打架标注数据/fight-detection-surv-dataset-master/dj'
    cutImageFromFolder(targetfolder,savefoler,5)
