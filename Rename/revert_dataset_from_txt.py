import os
import shutil
if __name__ == '__main__':
    inputs = ['/media/hzh/ssd_disk/smoke_and_call/charades_head','/media/hzh/ssd_disk/smoke_and_call/hmdb51_head','/media/hzh/ssd_disk/smoke_and_call/Hollywood2_head',
              '/media/hzh/ssd_disk/smoke_and_call/other_head','/media/hzh/ssd_disk/smoke_and_call/wider_head','/media/hzh/work/workspace/data/roi_data_train_square1/people',
              '/media/hzh/work/workspace/data/roi_data_train_square1/phone','/media/hzh/work/workspace/data/roi_data_train_square1/smoke',
              '/media/hzh/work/workspace/data/roi_data_train_square1/smoke_phone','/media/hzh/ssd_disk/smoke_and_call/film_head',
              '/media/hzh/ssd_disk/smoke_and_call/mask_head']
    file_list = []
    for input in inputs:
        filenames = os.listdir(input)
        # filename_list += filenames
        filenames = [os.path.join(input,filename) for filename in filenames]
        file_list += filenames

    txt_filename = '/home/hzh/tt.txt'
    target_path = '/media/hzh/work/workspace/data/roi_data_train_square2'
    people_path = os.path.join(target_path,'people')
    smoke_path = os.path.join(target_path,'smoke')
    phone_path = os.path.join(target_path,'call')
    both_path = os.path.join(target_path,'both')
    os.makedirs(people_path,exist_ok=True)
    os.makedirs(smoke_path,exist_ok=True)
    os.makedirs(phone_path,exist_ok=True)
    os.makedirs(both_path,exist_ok=True)

    with open(txt_filename, 'r') as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
        lines = set(lines)
        out_f = open('/home/hzh/un_find.txt', 'w')
        for line in lines:
            prefix,basename = os.path.split(line)
            _,cls = os.path.split(prefix)
            is_find = False
            for filename in file_list:
                _,basename1 = os.path.split(filename)
                if basename == basename1:
                    is_find = True
                    if cls == 'people':
                        new_filename = os.path.join(people_path,basename)
                        shutil.copy(filename,new_filename)
                    elif cls == 'smoke':
                        new_filename = os.path.join(smoke_path, basename)
                        shutil.copy(filename,new_filename)
                    elif cls == 'call':
                        new_filename = os.path.join(phone_path, basename)
                        shutil.copy(filename,new_filename)
                    elif cls == 'both':
                        new_filename = os.path.join(both_path, basename)
                        shutil.copy(filename,new_filename)
                    print('copy ',filename)
                    break
            if not is_find:
                out_f.write(line+'\n')
        out_f.close()