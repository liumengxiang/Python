# -*- coding:utf-8 -*-# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse
import http.cookiejar
import json
import time
import requests
import hashlib
import os
import re
from bs4 import BeautifulSoup

# 获取验证码并保存
def get_verify(mobile):
    # 普通请求头
    verify_headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
        'Host': 'sports.lifesense.com',
        'Connection': 'Keep-Alive',
    }

    # 拼接url
    verify_url = 'https://sports.lifesense.com/sms_service/verify/getValidateCode?requestId=1000&sessionId=nosession&mobile=' + mobile

    # 构建循环刷新验证码, 降低打码难度
    for i in range(1, 4):
        # 请求与响应
        verify_request = urllib.request.Request(url=verify_url, headers=verify_headers)
        verify_response = opener.open(verify_request)

    # 保存至文件
    with open('shuabu/verify.jpg', 'wb') as fp:
        fp.write(verify_response.read())


# 斐斐打码
def predict_verify():
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
    with open("shuabu/verify.jpg", "rb") as fp:
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

    # 获取打码结果
    verify = json.loads(json.loads(rsp_data.text)["RspData"])["result"]

    return verify


# 获取短信验证码
def get_code(verify, mobile):
    # 声明媒体类型‘application/json’的请求头, 否则报错
    auth_code_headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
        'Host': 'sports.lifesense.com',
        'Connection': 'Keep-Alive',
    }

    # 获取短信验证码的url
    auth_code_url = 'https://sports.lifesense.com/sms_service/verify/sendCodeWithOptionalValidate?sessionId=nosession&requestId=1000'

    # 传递图片验证码识别结果和登录的手机号码
    auth_code_data = {
        "code": verify,
        "mobile": mobile,
    }

    # 请求与响应
    auth_code_request = urllib.request.Request(url=auth_code_url, headers=auth_code_headers)
    auth_code_response = opener.open(auth_code_request, data=json.dumps(auth_code_data).encode())

    # 解析返回的数据
    auth_code_js_info = json.loads(auth_code_response.read().decode())

    # 获取发送状态码, 判断短信验证码是否成功发出
    # code = 200  成功发送
    # code = 412  验证码错误
    # code = 415  获取验证码已达上限
    # code = 500  服务器异常
    send_code = auth_code_js_info['code']

    return send_code


# 登录
def login(mobile):
    # 输入短信验证码
    authCode = input('请输入短信验证码:')
    print('\n正在尝试登录, 请稍后......')

    # 带有验证参数的url, 参数与登录设备有关, 此处为模拟器的参数
    login_url = 'https://sports.lifesense.com/sessions_service/loginByAuth?city=%E4%B8%8A%E6%B5%B7&province=%E4%B8%8A%E6%B5%B7%E5%B8%82&devicemodel=Magic2&areaCode=310109&osversion=5.1.1&screenHeight=1280&provinceCode=310000&version=4.5&channel=huawei&systemType=2&promotion_channel=huawei&screenWidth=720&requestId=d6e3e55379914cbd86ebbe975b19a877&longitude=121.492479&screenheight=1280&os_country=CN&timezone=Asia%2FShanghai&cityCode=310100&os_langs=zh&platform=android&clientId=8e844e28db7245eb81823132464835eb&openudid=&countryCode=&country=%E4%B8%AD%E5%9B%BD&screenwidth=720&network_type=wifi&appType=6&area=CN&latitude=31.247221&language=zh'

    # 带有媒体类型'application/json'的请求头
    login_headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
        'Host': 'sports.lifesense.com',
        'Connection': 'Keep-Alive',
    }

    # 登录信息, 其中'clientId'是以短信验证码方式登录的id信息
    login_data = {
        "clientId": "3627c6dc922e4fc7998af1f3f8867042",
        "authCode": authCode,
        "appType": "6",
        "loginName": mobile,
    }

    # 请求与响应
    login_request = urllib.request.Request(url=login_url, headers=login_headers)
    login_response = opener.open(login_request, data=json.dumps(login_data).encode())

    # 解析返回的数据
    login_js_info = json.loads(login_response.read().decode())

    # 获取登录状态码
    login_code = login_js_info['code']

    # 如果登录成功, 则返回用户id和cookie
    # userId用以后续提交数据
    # cookie用以记录登录状态
    if login_code == 200:
        # 提示
        print('\n登录成功!\n')
        # 获取userId
        userId = login_js_info['data'].get('userId')

        # 获取cookie
        cookie = ''
        for item in cj:
            cj_part = '{}={};'.format(item.name, item.value)
            cookie += cj_part

        # 要记录的数据
        record_data = '<account>{},{},{}</account>\n'.format(mobile, userId, cookie)
        # 判断路径是否已存在, 存在则读取
        if os.path.exists('shuabu/record_data.txt'):
            # 先读取原有数据
            with open('shuabu/record_data.txt', 'r+', encoding='utf-8') as fp:
                # 已存在数据
                user_data = fp.read()
            # 将重叠的数据删除
            with open('shuabu/record_data.txt', 'w+', encoding='utf-8') as fp:
                # 重叠格式
                pattern = re.compile('<account>{},{},(.*?)</account>\s'.format(mobile, userId))
                # 寻找重叠cookie
                overlap_cookie = pattern.findall(user_data)
                # 替换为空白字符串
                for co in overlap_cookie:
                    data = '<account>{},{},{}</account>\n'.format(mobile, userId, co)
                    user_data = user_data.replace(data, '')
                # 消除空白字符
                user_data = user_data.replace(' ', '')
                # 重新拼接record_data
                record_data = user_data + record_data
                # 写入
                fp.write(record_data)
        # 不存在则直接创建
        else:
            with open('shuabu/record_data.txt', 'w+', encoding='utf-8') as fp:
                fp.write(record_data)

        # 返回
        return userId

    # 登录不成功
    else:
        # 询问是否重新输入
        print('\n登录失败!\n')
        ask = input('请检查验证码是否输入有误, 直接回车重新输入, 输入’0‘退出:')
        # 直接退出
        if ask == '0':
            return '404'
        # 重新输入验证码
        else:
            login(mobile)


# 修改步数
def modify_step(userId, cookie='', mode='active'):
    # 提交步数的url
    step_url = 'https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?city=%E4%B8%8A%E6%B5%B7&province=%E4%B8%8A%E6%B5%B7%E5%B8%82&devicemodel=Magic2&areaCode=310109&osversion=5.1.1&screenHeight=1280&provinceCode=310000&version=4.5&channel=huawei&systemType=2&promotion_channel=huawei&screenWidth=720&requestId=d6e3e55379914cbd86ebbe975b19a877&longitude=121.492479&screenheight=1280&os_country=CN&timezone=Asia%2FShanghai&cityCode=310100&os_langs=zh&platform=android&clientId=8e844e28db7245eb81823132464835eb&openudid=&countryCode=&country=%E4%B8%AD%E5%9B%BD&screenwidth=720&network_type=wifi&appType=6&area=CN&latitude=31.247221&language=zh'

    # 修改步数的请求头, 与以上两者相同, 不赘述
    step_headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
        'Host': 'sports.lifesense.com',
        'Connection': 'Keep-Alive',
    }

    # 如果传入cookie, 则将cookie传入请求头尝试直接登录
    if cookie != '':
        # 这里有一个不知名bug, 只能强硬转换
        step_headers['Cookie'] = str(cookie).replace('b', '').replace('\n', '').replace(' ', '')

    # 输入步数
    step = int(input('您要修改步数为:'))

    # 运动距离与消耗的卡路里验证参数, 必须传入
    distance = step / 3
    calories = int(step / 4000)

    # 修改步数需要的参数
    step_data = {
        "list": [
            {
                "active": 1,
                "calories": calories,
                "dataSource": 2,
                "deviceId": "M_NULL",
                "distance": distance,
                "isUpload": 0,
                # 这里要传入上传数据时的时间戳
                "measurementTime": str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                "priority": 0,
                "step": step,
                "type": 2,
                # 这里要传入纪年时间值
                "updated": int((str(int(time.time()) * 1000).split('.'))[0]),
                "userId": userId,
                "DataSource": 2,
                "exerciseTime": 0
            }
        ]
    }

    # 请求与响应
    step_request = urllib.request.Request(url=step_url, headers=step_headers)
    step_response = opener.open(step_request, data=json.dumps(step_data).encode())

    # 解析返回的数据
    step_js_info = json.loads(step_response.read().decode())

    # 获取上传数据的状态码
    # code = 200  成功
    # 其他则修改失败
    step_code = step_js_info['code']

    # 根据登录模式不同选择不同执行方式
    if mode == 'active':
        # 判断是否修改成功
        # 修改成功
        if step_code == 200:
            print('\n数据上传成功!如存在步数并没有成功修改的情况, 请联系管理员!\n')
            # 询问是否继续修改
            ask = input('直接回车退出程序, 输入‘0’继续修改:')
            print()
            # 继续修改
            if ask == '0':
                modify_step(userId)
            # 退出程序
            else:
                print('程序已退出!\n')
                time.sleep(2)
                return 1
        # 修改失败
        else:
            print('\n修改失败!请重试!多次修改失败请联系管理员!\n')
            print('程序已退出!\n')
            time.sleep(2)
            return -1
    else:
        return step_code


# 主动登录
def active_login(mobile):
    # 提示
    print('\n正在获取验证码......')
    # 获取图片验证码并保存
    get_verify(mobile)

    # 尝试斐斐打码
    # 识别成功则返回识别结果
    try:
        print('\n正在尝试识别验证码......')
        verify = predict_verify()
        print('\n识别成功!')
        os.remove('shuabu/verify.jpg')
    # 账户余额不足, 无法识别
    except:
        print('\n可能是打码账户余额不足或者识别过于频繁, 请稍后再试或者联系管理员!\n')
        print('程序已退出!\n')
        time.sleep(2)
        return -1

    # 填写图片验证码, 获取短信验证码
    print('\n正在为您自动填写图片验证码......')
    # 返回状态码
    send_code = get_code(verify, mobile)

    # 成功发送短信验证码
    if send_code == 200:
        print('\n图片验证码正确, 短信验证码已下发!\n')
        # 尝试登录并获取返回的用户ID
        userId = login(mobile)
        # 返回失败状态码
        if userId == '404':
            print('\n程序已退出!\n')
            time.sleep(2)
            return 1
        # 获取用户ID成功, 准备开始修改步数
        else:
            modify_step(userId)

    # 图片验证码识别错误, 即将自动重启
    elif send_code == 412:
        print('\n图片验证码识别错误, 正在自动重新获取并识别, 请稍后......')
        active_login(mobile)

    # 短信验证码已达上限
    elif send_code == 415:
        print('\n今天获取短信验证码次数已达上限!请明天再来或者使用开发者模式!\n')
        print('程序已退出!\n')
        time.sleep(2)
        return 1

    else:
        print('\n服务器异常!请稍后再试!\n')
        print('程序已退出!\n')
        time.sleep(2)
        return -1


# 被动登录
def passive_login(userId, cookie):
    # 尝试直接修改
    step_code = modify_step(userId, cookie, 'passive')

    # 判断是否修改成功
    # 修改成功, 询问是否继续修改
    if step_code == 200:
        print('\n数据上传成功!如存在步数并没有成功修改的情况, 请联系管理员!\n')
        ask = input('直接回车退出程序, 输入’0‘继续修改:')
        print()
        # 继续修改
        if ask == '0':
            passive_login(userId, cookie)
        # 退出程序
        else:
            print('程序已退出!')
            time.sleep(2)
            return 1

    # 修改失败, 询问是否尝试主动登录
    else:
        print('\n修改失败!可能是cookie已过期!\n')
        ask = input('直接回车退出程序, 输入‘1’开始主动登录:')
        # 开始执行主动登录
        if ask == '1':
            # 提示语
            print('\n正在为您执行验证码登陆......\n')
            # 输入手机号
            mobile = input('请输入手机号码:')
            # 限制用户输入
            while (not mobile.isdigit()) or len(mobile) != 11:
                print()
                mobile = input('手机号码格式错误!请重新输入:')
            # 开始执行主动登陆
            active_login(mobile)
        # 退出程序
        else:
            print('\n程序已退出!\n')
            time.sleep(2)
            return 1


# 主程序
def main():
    # 检测是否存在cookie文件, 存在则询问是否直接登录
    # 存在则询问
    if os.path.exists('shuabu/record_data.txt'):
        # 读取数据
        with open('shuabu/record_data.txt', 'r+', encoding='utf-8') as fp:
            info = fp.read()

        # 用户菜单
        print('\n检测到有以下账户的cookie:')
        # 固定格式
        pattern = re.compile('<account>(.*?)</account>\s')
        # 检索用户
        user_ls = pattern.findall(info)
        n = 0
        for user in user_ls:
            n += 1
            print('{}:<{}>'.format(n, (user.split(','))[0]))
        print()

        # 选择登录
        ask = input('输入相应序号可直接尝试登录对应账户, 输入’0‘则以验证码登录:')
        # 限制用户输入
        while (not ask.isdigit()) or (not 0 <= int(ask) <= n):
            print('\n必须输入0到%s的整数!\n' % n)
            ask = input('输入相应序号可直接尝试登录对应账户, 输入’0‘则以验证码登录:')
        # 转为序号
        ask = int(ask) - 1

        # 主动登陆
        if ask == -1:
            # 提示语
            print('\n正在为您执行验证码登陆\n')
            # 输入手机号
            mobile = input('请输入手机号码:')
            # 限制用户输入
            while (not mobile.isdigit()) or len(mobile) != 11:
                print()
                mobile = input('手机号码格式错误!请重新输入:')
            # 开始执行主动登陆
            active_login(mobile)

        # 被动登陆
        else:
            mobile, userId, cookie = (user_ls[ask]).split(',')
            print('\n正在为您登录账户<{}>......\n'.format(mobile))
            # 开始执行被动登陆
            passive_login(userId, cookie)

    # 不存在则执行主动登录
    else:
        # 提示语
        print('\n正在为您执行验证码登陆\n')
        # 输入手机号
        mobile = input('请输入手机号码:')
        # 限制用户输入
        while (not mobile.isdigit()) or len(mobile) != 11:
            print()
            mobile = input('手机号码格式错误!请重新输入:')
        # 开始执行主动登陆
        active_login(mobile)


# 问候语
def hello():
    # 确保程序数据路径存在
    if not os.path.exists('shuabu'):
        os.mkdir('shuabu')
    # 问候语
    print('********************************')
    print("【 Welcome to flyingdream's lab 】")
    print('********************************')


if __name__ == '__main__':
    # 问候
    hello()
    # 创建会话, 保存cookie(在此处创建是为了使opener成为全局变量)
    cj = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(handler)
    # 开始
    main()