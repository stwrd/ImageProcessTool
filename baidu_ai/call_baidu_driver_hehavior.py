# encoding:utf-8

import requests
import base64
import cv2
import numpy as np
from pathlib import Path

def base64_cv2(base64_str):
    imgString = base64.b64decode(base64_str)
    nparr = np.fromstring(imgString,np.uint8)
    image = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    return image
'''
驾驶行为分析
'''
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ifP9I5XrzYQY6ce3pERFgisz&client_secret=wKP2ODvYwqZCK2nFnjdsYTEtDqDmpOr7'
access_response = requests.get(host)
if access_response:
    print(access_response.json())
access_token = access_response.json()['access_token']
request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/driver_behavior"
# 二进制方式打开图片文件

filenames = Path('/media/hzh/ssd_disk/spd_data/Sbelt_phone20200615done').rglob('*.jpg')
cv2.namedWindow('tt',flags=0)
for filename in filenames:
    f = open(filename.as_posix(), 'rb')
    img = base64.b64encode(f.read())
    cv_img = base64_cv2(img)

    params = {"image":img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        print (response.json())
        result_json = response.json()
        for person_info in result_json["person_info"]:
            location = person_info["location"]
            width = location["width"]
            top = location["top"]
            left = location["left"]
            height = location["height"]
            call_score = person_info["attributes"]["cellphone"]["score"]
            smoke_socre = person_info["attributes"]["smoke"]["score"]
            if call_score > 0.5:
                cv2.putText(cv_img,'call',(left,top),cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 2)
                cv2.rectangle(cv_img,(left,top),(left+width,top+height),(255,0,0),thickness=3)
                cv2.imshow('tt',cv_img)
                cv2.waitKey(0)
            if smoke_socre > 0.5:
                cv2.putText(cv_img, 'smoke', (left, top), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 2)
                cv2.rectangle(cv_img,(left,top),(left+width,top+height),(0,0,255),thickness=3)
                cv2.imshow('tt',cv_img)
                cv2.waitKey(0)
