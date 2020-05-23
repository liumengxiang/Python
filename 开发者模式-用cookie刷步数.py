# -*- coding:utf-8 -*-# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import http.cookiejar
import json
import time


cj = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(handler)

step_url = 'https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?country=%E4%B8%AD%E5%9B%BD&city=%E8%8C%82%E5%90%8D&cityCode=440900&timezone=Asia%2FShanghai&latitude=21.896515&os_country=CN&channel=huawei&language=zh&openudid=&platform=android&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&appType=6&requestId=3419c7c789b04bbf8038dc1f0b34975b&countryCode=&systemType=2&longitude=111.090323&devicemodel=TNY-AL00&area=CN&screenwidth=1080&os_langs=zh&provinceCode=440000&promotion_channel=huawei&rnd=01bac08f&version=4.6&areaCode=440981&requestToken=b52865104761842bfcc7ffdc01d1466c&network_type=wifi&osversion=10&screenheight=2340'

step_headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MIX Build/LMY48Z)',
    'Host': 'sports.lifesense.com',
    'Connection': 'Keep-Alive',
}

cookie = input('请输入cookie:')
step_headers['Cookie'] = cookie
id = input('请输入id:')
step = int(input('您要修改步数为:'))
distance = step / 3
calories = int(step / 4000)


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
            "userId": id,
            "DataSource": 2,
            "exerciseTime": 0
        }
    ]
}

step_request = urllib.request.Request(url=step_url, headers=step_headers)
step_response = opener.open(step_request, data=json.dumps(step_data).encode())

step_js_info = json.loads(step_response.read().decode())

print(step_js_info)
