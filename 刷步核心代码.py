# -*- coding:utf-8 -*-# -*- coding:utf-8 -*-
import json
import time
import requests
import hashlib



##################################################################

r = requests.Session()

mobile = input('请输入手机号码:')


def verify(mobile):
    verify_headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
        'Host': 'sports.lifesense.com',
        'Connection': 'Keep-Alive',
    }

    verify_url = 'https://sports.lifesense.com/sms_service/verify/getValidateCode?requestId=1000&sessionId=nosession&mobile=' + mobile

    verify_content = r.get(url=verify_url, headers=verify_headers).content

    return verify_content


for i in range(1, 4):
    verify_content = verify(mobile)

with open('verify.jpg', 'wb') as fp:
    fp.write(verify_content)


def Predict():
    # 账户
    pd_id = "122456"
    pd_key = "XMs+NAqARNG+L1Jlx3zREgZ8S6ZKkKgZ"

    # 打码接口
    url = "http://pred.fateadm.com/api/capreg"

    # 验证码类型
    pred_type = "10500"

    # 哈希算法加密验证
    tm = str(int(time.time()))
    # 第一次加密
    md5 = hashlib.md5()
    md5.update((tm + pd_key).encode())
    csign = md5.hexdigest()
    # 第二次加密
    md5 = hashlib.md5()
    md5.update((pd_id + tm + csign).encode())
    csign = md5.hexdigest()

    # 表单数据
    param = {
        "user_id": pd_id,
        "timestamp": tm,
        "sign": csign,
        "predict_type": pred_type,
        "up_type": "mt"
    }

    # 验证码图片数据
    with open("verify.jpg", "rb") as fp:
        files = fp.read()
    # 转化为post数据
    files_data = {
        'img_data': ('img_data', files)
    }
    # 请求头
    header = {
        'User-Agent': 'Mozilla/5.0',
    }
    # 响应数据
    rsp_data = requests.post(url, param, files=files_data, headers=header)

    # 得到打码结果
    value = json.loads(json.loads(rsp_data.text)["RspData"])["result"]

    return value


value = Predict()

#####################################################################

code_url = 'https://sports.lifesense.com/sms_service/verify/sendCodeWithOptionalValidate?sessionId=nosession&requestId=1000'

code_headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
    'Host': 'sports.lifesense.com',
    'Connection': 'Keep-Alive',
}

code_data = {
    "code": value,
    "mobile": mobile,
}

code_resp = r.post(url=code_url, headers=code_headers, json=code_data)

print(code_resp.text)

print('#########################################################################')

#####################################################################

authCode = input('请输入验证码:')

login_url = 'https://sports.lifesense.com/sessions_service/loginByAuth?city=%E4%B8%8A%E6%B5%B7&province=%E4%B8%8A%E6%B5%B7%E5%B8%82&devicemodel=Magic2&areaCode=310109&osversion=5.1.1&screenHeight=1280&provinceCode=310000&version=4.5&channel=huawei&systemType=2&promotion_channel=huawei&screenWidth=720&requestId=d6e3e55379914cbd86ebbe975b19a877&longitude=121.492479&screenheight=1280&os_country=CN&timezone=Asia%2FShanghai&cityCode=310100&os_langs=zh&platform=android&clientId=8e844e28db7245eb81823132464835eb&openudid=&countryCode=&country=%E4%B8%AD%E5%9B%BD&screenwidth=720&network_type=wifi&appType=6&area=CN&latitude=31.247221&language=zh'

login_headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
    'Host': 'sports.lifesense.com',
    'Connection': 'Keep-Alive',
}

login_data = {
    "clientId": "3627c6dc922e4fc7998af1f3f8867042",
    "authCode": authCode,
    "appType": "6",
    "loginName": mobile,
}

login_text = json.loads(r.post(url=login_url, headers=login_headers, json=login_data).text)

userId = login_text['data'].get('userId')

print(login_text)

print('#########################################################################')

######################################################################

step_url = 'https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?city=%E4%B8%8A%E6%B5%B7&province=%E4%B8%8A%E6%B5%B7%E5%B8%82&devicemodel=Magic2&areaCode=310109&osversion=5.1.1&screenHeight=1280&provinceCode=310000&version=4.5&channel=huawei&systemType=2&promotion_channel=huawei&screenWidth=720&requestId=d6e3e55379914cbd86ebbe975b19a877&longitude=121.492479&screenheight=1280&os_country=CN&timezone=Asia%2FShanghai&cityCode=310100&os_langs=zh&platform=android&clientId=8e844e28db7245eb81823132464835eb&openudid=&countryCode=&country=%E4%B8%AD%E5%9B%BD&screenwidth=720&network_type=wifi&appType=6&area=CN&latitude=31.247221&language=zh'

step_headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
    'Host': 'sports.lifesense.com',
    'Connection': 'Keep-Alive',
}

step = int(input('您要修改步数为:'))
distance = step / 3
calories = step / 4

step_data = {
    "list": [
        {
            "active": 1,
            "calories": calories,
            "dataSource": 2,
            "deviceId": "M_NULL",
            "distance": distance,
            "isUpload": 0,
            "measurementTime": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            "priority": 0,
            "step": step,
            "type": 2,
            "updated": int((str(int(time.time()) * 1000).split('.'))[0]),
            "userId": userId,
            "DataSource": 2,
            "exerciseTime": 0
        }
    ]
}

step_text = json.loads(r.post(url=step_url, headers=step_headers, json=step_data).text)

print(step_text)
