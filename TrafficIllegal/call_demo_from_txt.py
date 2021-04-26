import sys
import base64
import os
import re
import requests
import json
import time
import cv2
import numpy as np
from pathlib import Path

pattern1 = re.compile("^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4,5}[A-Z0-9挂学警港澳]{1}$")
pattern2 = re.compile("^[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$")


def call(image_name, hphm, wfxw, zpms_detail):
    print('call', image_name)
    url = 'http://127.0.0.1:80/api/analysisImage'
    body = {"wfxw": "1"}
    headers = {"Content-Type": "application/json;charset=utf-8"}
    for i in range(len(image_name)):
        f = open(image_name[i], 'rb')
        image = f.read()
        f.close()
        imgdata = base64.encodebytes(image).decode()
        body["zpstr" + str(i + 1)] = imgdata
        body["zpms" + str(i + 1)] = zpms_detail

    body["xh"] = "1"
    body["hphm"] = hphm
    body["wfxw"] = wfxw
    body["hpzl"] = "02"
    body["zpms"] = "1"
    body["zpsl"] = str(len(image_name))
    body["clfl"] = "1"
    body["yxj"] = "1"
    body["sbms"] = "3"
    body["file_name"] = image_name[0]
    response = requests.post(url, data=json.dumps(body), headers=headers)
    return response.text

# def find_group_image(pre_name, images):
#     res = []
#     for image in images:
#         if image.startswith(pre_name):
#             res.append(image)
#     return res

def find_group_image(image_file_path):
    cur_folder_path = image_file_path.parent
    image_name_without_suffix = image_file_path.stem
    return sorted(cur_folder_path.glob(image_name_without_suffix[:-1]+'*.jpg'))

def draw_image(detected_images,result):
    for i in range(min(3, len(detected_images))):
        key_name = "tpbz{}".format(i + 1)
        if key_name in result:
            tpbz = result["tpbz{}".format(i + 1)]
            draw_img = cv2.imread(detected_images[i])
            print('tpbz{}'.format(i + 1))
            if tpbz['bznr'] is None:
                continue
            for bznr in tpbz['bznr']:
                bjd = bznr["bjd"]
                w, h = tpbz['tpkd'], tpbz['tpgd']
                pt1 = (int(bjd[0]['x'] * w), int(bjd[0]['y'] * h))
                pt2 = (int(bjd[1]['x'] * w), int(bjd[1]['y'] * h))
                cv2.rectangle(draw_img, pt1, pt2, (0, 0, 255), 2)
                print('w:', w, 'h:', h)
                print('src:', bjd, 'dst:', pt1, pt2)
        cv2.imwrite(filename=(detected_images[i].replace(in_folder, 'out/')), img=draw_img)

def test_from_image_list(image_file_list,wfxw,out_file,zpms_detail):
    with open(out_file, 'a') as result_file:
        for filename in image_file_list:
            image_file_path = Path(filename.strip())  # 全路径
            detected_images = find_group_image(image_file_path)
            res1 = re.search('[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4,5}[A-Z0-9挂学警港澳]{1}',
                             detected_images[0].as_posix())
            do_algo = False
            if res1:
                do_algo = True
                hphm = res1.group()
            else:
                res2 = re.search('[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}', detected_images[0].as_posix())
                if res2:
                    do_algo = True
                    hphm = res2.group()
                else:
                    print('can not match hphm!!!!!!!!!!!')
            if do_algo:
                print('hphm:', hphm)
                detected_images = [filename.as_posix() for filename in detected_images]
                print('process images:', detected_images)
                ret = call(detected_images, hphm, wfxw, zpms_detail)
                ret = json.loads(ret)
                result = ret["result"]
                # print(result)
                # #print(image_names)
                if result["sbjg"] == '1':  # 删除
                    for image in detected_images:
                        result_file.write(image + '#1#' + result['pdyj'] + '\n')
                        print("result:",删除)
                        break
                elif result["zhjg"] == '1':  # 找回
                    for image in detected_images:
                        result_file.write(image + '#2#' + result['zhyj'] + '\n')
                        print("result:",找回)
                        break
                else:
                    for image in detected_images:  # 未知
                        result_file.write(image + '#0#0\n')
                        print("result:", 争议)
                        break
                # 绘图
                if False:
                    draw_image(detected_images=detected_images, result=result)

def test_from_txt(in_file,wfxw,out_file,zpms_detail):
    with open(in_file,'r') as image_file_list:
        test_from_image_list(image_file_list,wfxw,out_file,zpms_detail)

def test_multi_image(in_folder, wfxw, save_file, zpms_detail):
    in_folder = Path(in_folder)
    image_file_list = sorted(in_folder.glob('*.jpg'))
    filter_list = []
    for image_file in image_file_list:
        if len(filter_list) == 0:
            filter_list.append(image_file.as_posix())
            image_name_without_suffix_base = image_file.stem
        else:
            image_name_without_suffix1 = image_file.stem
            if image_name_without_suffix1[:-1] != image_name_without_suffix_base[:-1]:
                filter_list.append(image_file.as_posix())
                image_name_without_suffix_base = image_file.stem
    test_from_image_list(filter_list,wfxw,save_file,zpms_detail)


if __name__ == '__main__':
    in_folder = sys.argv[1]
    wfxw = sys.argv[2]
    save_file = sys.argv[3]
    zpms_detail = sys.argv[4]  # "2*2"
    # test_single_image(in_folder, wfxw, save_file, zpms_detail)
    test_from_txt(in_folder, wfxw, save_file, zpms_detail)
    print('----------------------------------------------------')
    test_multi_image(Path('/media/hzh/work/data/stardard_test_data/1208/yisi'), wfxw, save_file, zpms_detail)
