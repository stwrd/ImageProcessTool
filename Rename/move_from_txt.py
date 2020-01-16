import os
import shutil
if __name__ == '__main__':
    tar_path = r'/media/hzh/ssd_disk/BaiduNetdiskDownload/Hollywood2-actions/Hollywood2'
    filename = os.path.join(tar_path,'ClipSets','AnswerPhone_autotrain.txt')
    with open(filename, 'r') as f:
        for line in f:
            video_name,v = line.split()
            if v == '1':
                input_video = os.path.join(tar_path,'AVIClips','{}.avi'.format(video_name))
                os.makedirs(os.path.join(tar_path,'call'),exist_ok=True)
                print(input_video)
                output_video = os.path.join(tar_path, 'call', '{}.mp4'.format(video_name))
                cmd = 'ffmpeg -y -i {}  -r 6 {}'.format(input_video, output_video)
                os.system(cmd)
