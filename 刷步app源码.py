# -*- coding:utf-8 -*-# -*- coding:utf-8 -*-
# 引入kivy类
import kivy

kivy.require('1.11.1')
# APP类
from kivy.app import App
# BoxLayout容器
from kivy.uix.boxlayout import BoxLayout
# 输入框
from kivy.uix.textinput import TextInput
# 标签
from kivy.uix.label import Label
# 按钮
from kivy.uix.button import Button
# 引入request
from kivy.network.urlrequest import UrlRequest
# 解析文件用
from urllib3 import encode_multipart_formdata
import json
import hashlib
import time
import os
import re

# 中文支持
ft = kivy.resources.resource_find('DroidSansFallback.ttf')
# 创建数据储存文件夹
if not os.path.exists('/storage/emulated/0/shuabu'):
    os.mkdir('/storage/emulated/0/shuabu')


# 创建自己的APP
class StepsModify(App):
    # 继承
    def build(self):
        # 根容器
        self.box = BoxLayout(orientation='vertical')
        # 主体容器
        self.main_box = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        # 底层容器
        self.bottom_box = BoxLayout(orientation='vertical', size_hint=(1, 0.5), spacing=30)
        # 架构容器
        self.frame_box = BoxLayout(orientation='vertical',
                                   size_hint=(1, None),
                                   spacing=30)
        # 标签1
        self.tip1 = Label(text="",
                          size_hint=(1, None),
                          size=(0, 70),
                          font_size=70,
                          font_name=ft,
                          halign='center')
        # 标签2
        self.tip2 = Label(text="",
                          size_hint=(1, None),
                          size=(0, 70),
                          font_size=70,
                          font_name=ft,
                          halign='center')

        # 输入框
        self.input = TextInput(font_size=50,
                               size_hint=(0.9, None),
                               size=(0, 80),
                               pos_hint={'x': 0.05},
                               halign='center',
                               multiline=False,
                               cursor_color=[0, 0, 1, 1],
                               foreground_color=[0, 0, 1, 1],
                               input_filter='int',
                               font_name=ft)
        # 确定按钮
        self.confirm = Button(text='确定',
                              size_hint=(0.16, None),
                              size=(0, 70),
                              font_size=60,
                              pos_hint={'x': 0.42},
                              font_name=ft)

        # 退出按钮
        self.exit = Button(text='点击退出',
                           size_hint=(1, None),
                           size=(0, 60),
                           font_size=50,
                           font_name=ft)
        # 绑定退出函数
        self.exit.bind(on_press=self.quit)
        # 将exit放入bottom_box
        self.bottom_box.add_widget(self.exit)

        # 将frame_box放入main_box
        self.main_box.add_widget(self.frame_box)
        # 将main_box放入box
        self.box.add_widget(self.main_box)
        # 将bottom_box放入box
        self.box.add_widget(self.bottom_box)

        # 检索登陆数据
        self.read_record()

        return self.box

    #################################################查看数据记录##########################################################
    def read_record(self):
        if os.path.exists('/storage/emulated/0/shuabu/record_data.txt'):
            # 检索tips
            self.root_tips = Label(text="检测到以下账户\n",
                                   size_hint=(1, 0.8),
                                   font_size=60,
                                   font_name=ft,
                                   halign='center')
            # 读取数据
            with open('/storage/emulated/0/shuabu/record_data.txt', 'r+', encoding='utf-8') as fp:
                info = fp.read()
            # 固定格式
            pattern = re.compile('<account>(.*?)</account>\s')
            # 检索用户
            self.user_ls = pattern.findall(info)
            self.n = 0
            for user in self.user_ls:
                self.n += 1
                self.root_tips.text += '{}:<{}>\n'.format(self.n, (user.split(','))[0])
            # 检索提示
            self.tip1.text = '输入相应序号登录对应账户'
            self.tip2.text = '输入0执行主动登录'
            # 检索添加
            self.bottom_box.add_widget(self.root_tips, index=1)
            self.frame_box.add_widget(self.tip1)
            self.frame_box.add_widget(self.tip2)
            self.frame_box.add_widget(self.input)
            self.frame_box.add_widget(self.confirm)
            # 绑定功能
            self.confirm.bind(on_press=self.deal)
        # 不存在则执行主动登录
        else:
            self.input_mobile()

    #################################################处理输入命令##########################################################
    def deal(self, btn):
        if self.input.text == '':
            # tip1提示未输入命令
            # tip2提示输入命令
            self.tip2.text = '请输入命令(0-{})!'.format(self.n)
            self.tip1.text = ''
            # 先解绑
            self.confirm.unbind(on_press=self.deal)
            # 再绑定
            self.confirm.bind(on_press=self.deal)
        elif not 0 <= int(self.input.text) <= self.n:
            # tip1提示命令错误
            # tip2提示重新输入命令
            self.tip1.text = '只能输入0-{}的整数!'.format(self.n)
            self.tip2.text = '请重新输入:'
            # 清除输入数据
            self.input.text = ''
            # 先解绑
            self.confirm.unbind(on_press=self.deal)
            # 再绑定
            self.confirm.bind(on_press=self.deal)
        elif self.input.text == '0':
            # 清除小部件记录
            self.tip1.text = ''
            self.tip2.text = ''
            self.input.text = ''
            self.frame_box.remove_widget(self.tip1)
            self.frame_box.remove_widget(self.tip2)
            self.frame_box.remove_widget(self.input)
            self.frame_box.remove_widget(self.confirm)
            self.confirm.unbind(on_press=self.deal)
            self.bottom_box.remove_widget(self.root_tips)
            # 执行主动登录
            self.input_mobile()
        else:
            self.bottom_box.remove_widget(self.root_tips)
            cmd = int(self.input.text) - 1
            self.mobile, self.userId, self.cookie = (self.user_ls[cmd]).split(',')
            # tip1提示正在登陆
            # tip2提示输入所要修改的步数
            self.tip1.text = "登录账户{}中......".format(self.mobile)
            self.tip2.text = "请输入您要修改的步数:"
            # 清除原输入
            self.input.text = ''
            # 解绑原函数
            self.confirm.unbind(on_press=self.deal)
            # 绑定新函数confirm_steps
            self.confirm.bind(on_press=self.confirm_steps)

    ###############################################requests回调函数#######################################################
    # 退出
    def quit(self, bnt):
        exit()

    # 请求错误回调
    def show_error(self, resp, error):
        self.tip1.text = '发生了一个错误:'
        self.tip2.text = '{}'.format(error)

    # 请求失败回调
    def show_failure(self, resp, result):
        self.tip1.text = "请求失败:"
        self.tip2.text = '{}'.format(result)

    #################################################输入手机号码##########################################################
    # 输入手机号码
    def input_mobile(self):
        # tip2提示输入手机号码
        self.tip2.text = '请输入手机号码:'
        # 将tip1,tip1加入frame_box #---------------------------------- # 将tip1,tip1加入frame_box
        self.frame_box.add_widget(self.tip1)
        self.frame_box.add_widget(self.tip2)
        # <第一次>将input,confirm加入frame_box #-----------------------------------# <第一次>将input,confirm加入frame_box
        self.frame_box.add_widget(self.input)
        self.frame_box.add_widget(self.confirm)
        # <第一次>将confirm绑定confirm_mobile #-----------------------------------# <第一次>将confirm绑定confirm_mobile
        self.confirm.bind(on_press=self.confirm_mobile)

    # 检测是否已输入手机号码
    def confirm_mobile(self, btn):
        if self.input.text == '':
            # tip1提示未输入手机号码
            # tip2提示输入手机号码
            self.tip1.text = '您还没有输入手机号码!'
            self.tip2.text = '请输入手机号码:'
            # 先解绑
            self.confirm.unbind(on_press=self.confirm_mobile)
            # 再绑定
            self.confirm.bind(on_press=self.confirm_mobile)
        elif len(self.input.text) != 11:
            # tip1提示手机号码格式错误
            # tip2提示重新输入手机号码
            self.tip1.text = '手机号码格式错误!'
            self.tip2.text = '请重新输入:'
            # 清除输入数据
            self.input.text = ''
            # 先解绑
            self.confirm.unbind(on_press=self.confirm_mobile)
            # 再绑定
            self.confirm.bind(on_press=self.confirm_mobile)
        else:
            # 执行下一步-->获取图片验证码
            self.get_verification()

    #################################################图片验证码处理########################################################
    # 获取图片验证码
    def get_verification(self):
        # tip1提示正在获取图片验证码
        self.tip1.text = '正在获取图片验证码......'
        self.tip2.text = ''
        # <第一次>移除input,confirm #-----------------------------------# <第一次>移除input,confirm
        self.frame_box.remove_widget(self.input)
        self.frame_box.remove_widget(self.confirm)

        # 获取第一次input值
        self.mobile = self.input.text
        # 请求头
        verification_headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Honor Build/LMY48Z)',
            'Host': 'sports.lifesense.com',
            'Connection': 'Keep-Alive',
        }

        # 拼接url
        verification_url = 'https://sports.lifesense.com/sms_service/verify/getValidateCode?requestId=1000&sessionId=nosession&mobile=' + self.mobile

        # 发送请求
        # 请求错误回调show_error
        # 请求失败回调show_failure
        # 请求成功回调predict_verification
        verification_resquest = UrlRequest(url=verification_url,
                                           on_error=self.show_error,
                                           on_failure=self.show_failure,
                                           on_success=self.predict_verification,
                                           decode=False,
                                           req_headers=verification_headers,
                                           verify=False)

    # 识别图片验证码
    def predict_verification(self, resp, result):
        # tip1,tip2提示正在识别图片验证码
        self.tip1.text = '获取图片验证码成功!'
        self.tip2.text = '正在自动识别......'

        # 打码账户
        pd_id = "122456"
        pd_key = "XMs+NAqARNG+L1Jlx3zREgZ8S6ZKkKgZ"

        # 哈希算法验证
        tm = str(int(time.time()))
        # 第一次加密
        md5 = hashlib.md5()
        md5.update((tm + pd_key).encode())
        csign = md5.hexdigest()
        # 第二次加密
        md5 = hashlib.md5()
        md5.update((pd_id + tm + csign).encode())
        csign = md5.hexdigest()

        # 打码根url
        base_url = "http://pred.fateadm.com/api/capreg?user_id=122456&timestamp={}&sign={}&predict_type=30400&up_type=mt"
        # 打码真实url
        url = base_url.format(tm, csign)

        # 传递图片数据
        files_data = {
            'img_data': ('img_data', result)
        }
        # 格式化数据
        encode_data = encode_multipart_formdata(files_data)
        # 获取转换后的图片数据
        data = encode_data[0]
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0',
            # 声明数据类型
            'Content-Type': encode_data[1],
        }

        # 发送请求
        # 成功则回调get_authCode,其余同上
        predict_request = UrlRequest(url=url,
                                     method='POST',
                                     on_error=self.show_error,
                                     on_failure=self.show_failure,
                                     on_success=self.get_authCode,
                                     req_body=data,
                                     req_headers=headers,
                                     verify=False)

    #################################################获取短信验证码########################################################
    # 获取短信验证码
    def get_authCode(self, resp, result):
        # 防止打码账户不足而出错
        try:
            # 获取图片验证码的值
            value = json.loads(json.loads(result)["RspData"])["result"]

            # 获取短信验证码的url
            get_authCode_url = 'https://sports.lifesense.com/sms_service/verify/sendCodeWithOptionalValidate?sessionId=nosession&requestId=1000'
            # 请求头
            get_authCode_headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
                'Host': 'sports.lifesense.com',
                'Connection': 'Keep-Alive',
            }
            # 所需数据
            get_authCode_data = {
                "code": value,
                "mobile": self.mobile,
            }

            # 发送请求
            # 成功则回调input_authCode,其余同上
            get_authCode_request = UrlRequest(url=get_authCode_url,
                                              on_error=self.show_error,
                                              on_failure=self.show_failure,
                                              on_success=self.input_authCode,
                                              req_body=json.dumps(get_authCode_data),
                                              req_headers=get_authCode_headers,
                                              verify=False)
        except:
            # 提示打码账户不足
            self.tip1.text = '打码账户余额不足!'
            self.tip2.text = '请等待管理员充值!'

    # 输入短信验证码
    def input_authCode(self, resp, result):
        # 获取发送状态码
        send_code = result['code']

        # <第二次>加入input,confirm #-----------------------------------# <第二次>加入input,confirm
        self.frame_box.add_widget(self.input)
        self.frame_box.add_widget(self.confirm)

        # 判断发送状态
        # 发送短信验证码成功:
        if send_code == 200:
            # tip1提示发送成功
            # tip2提示输入短信验证码
            self.tip1.text = "短信验证码发送成功!"
            self.tip2.text = "请输入短信验证码:"
            # 清除原输入
            self.input.text = ''
            # 解绑原函数
            self.confirm.unbind(on_press=self.confirm_mobile)
            # 绑定新函数login #-----------------------------------# <第二次>将confirm绑定login
            self.confirm.bind(on_press=self.login)
        else:
            if send_code == 412:
                # tip1,tip2提示识别验证码错误
                self.tip1.text = "识别错误!"
                self.tip2.text = "请按下确定键重新识别!"
            elif send_code == 500:
                # tip1,tip2提示服务器异常
                self.tip1.text = "服务器异常!"
                self.tip2.text = "可按下确定键重新尝试!"
            elif send_code == 415:
                # tip1提示验证码已达上限
                self.tip1.text = "获取验证码已达上限!"
                # tip2提示输入子账号
                self.tip2.text = "可尝试您的子账号:"
                # 清除原输入
                self.input.text = ''
            else:
                # tip1,tip2提示出现了bug
                self.tip1.text = "出现了一个错误!"
                self.tip2.text = "请先退出!"
                # 清除input,confirm
                self.frame_box.remove_widget(self.input)
                self.frame_box.remove_widget(self.confirm)

    ###################################################执行登录###########################################################
    def login(self, btn):
        # <第二次>移除input,confirm #-----------------------------------# <第二次>移除input,confirm
        self.frame_box.remove_widget(self.input)
        self.frame_box.remove_widget(self.confirm)
        # tip1提示正在登录
        self.tip2.text = ""
        self.tip1.text = "正在尝试登录......"

        # 获取第二次input值
        authCode = self.input.text

        # 登录url
        login_url = 'https://sports.lifesense.com/sessions_service/loginByAuth?city=%E4%B8%8A%E6%B5%B7&province=%E4%B8%8A%E6%B5%B7%E5%B8%82&devicemodel=Magic2&areaCode=310109&osversion=5.1.1&screenHeight=1280&provinceCode=310000&version=4.5&channel=huawei&systemType=2&promotion_channel=huawei&screenWidth=720&requestId=d6e3e55379914cbd86ebbe975b19a877&longitude=121.492479&screenheight=1280&os_country=CN&timezone=Asia%2FShanghai&cityCode=310100&os_langs=zh&platform=android&clientId=8e844e28db7245eb81823132464835eb&openudid=&countryCode=&country=%E4%B8%AD%E5%9B%BD&screenwidth=720&network_type=wifi&appType=6&area=CN&latitude=31.247221&language=zh'
        # 请求头
        login_headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
            'Host': 'sports.lifesense.com',
            'Connection': 'Keep-Alive',
        }
        # 所需数据
        login_data = {
            "clientId": "3627c6dc922e4fc7998af1f3f8867042",
            "authCode": authCode,
            "appType": "6",
            "loginName": self.mobile,
        }

        # 发送请求
        # 成功则回调input_steps,其余同上
        login_request = UrlRequest(url=login_url,
                                   on_error=self.show_error,
                                   on_failure=self.show_failure,
                                   on_success=self.input_steps,
                                   req_body=json.dumps(login_data),
                                   req_headers=login_headers,
                                   verify=False)

    #################################################输入步数并处理########################################################
    # 输入步数
    def input_steps(self, resp, result):
        # 获取登录状态码
        login_code = result['code']

        # <第三次>加入input,confirm #-----------------------------------# <第三次>加入input,confirm
        self.frame_box.add_widget(self.input)
        self.frame_box.add_widget(self.confirm)

        # 判断发送状态
        # 发送短信验证码失败
        if login_code != 200:
            # tip1提示短信验证码错误
            # tip2提示重新输入短信验证码
            self.tip1.text = "登录失败!"
            self.tip2.text = "请检查短信验证码是否有误:"
            # 解绑原函数
            self.confirm.unbind(on_press=self.login)
            # 重新绑定
            self.confirm.bind(on_press=self.login)
        else:
            # tip1提示登录成功
            self.tip1.text = "登录成功!"
            # 从resp中获取cookie
            self.cookie = (resp.resp_headers['Set-Cookie']).replace(',', ':').replace(' ', '')
            # 从result中获取userId
            self.userId = (result['data'])['userId']
            # 记录数据
            self.record()
            # tip2提示输入所要修改的步数
            self.tip2.text = "请输入您要修改的步数:"
            # 清除原输入
            self.input.text = ''
            # 解绑原函数
            self.confirm.unbind(on_press=self.login)
            # 绑定新函数confirm_steps #-----------------------------------# <第三次>将confirm绑定confirm_steps
            self.confirm.bind(on_press=self.confirm_steps)

    # 检测步数是否合法
    def confirm_steps(self, btn):
        if self.input.text == '':
            # tip1提示未输入步数
            # tip2提示输入步数
            self.tip1.text = '您还没有输入步数!'
            self.tip2.text = '请输入您要修改的步数:'
            # 先解绑
            self.confirm.unbind(on_press=self.confirm_steps)
            # 再绑定
            self.confirm.bind(on_press=self.confirm_steps)
        elif int(self.input.text) > 100000:
            # tip1提示步数过多
            # tip2提示重新步数
            self.tip1.text = '步数请不要超过100000!'
            self.tip2.text = '请重新输入步数:'
            # 清除输入数据
            self.input.text = ''
            # 先解绑
            self.confirm.unbind(on_press=self.confirm_steps)
            # 再绑定
            self.confirm.bind(on_press=self.confirm_steps)
        else:
            # 执行下一步-->修改步数
            self.modify()

    ###################################################记录数据###########################################################
    # 记录数据
    def record(self):
        # 要记录的数据
        record_data = '<account>{},{},{}</account>\n'.format(self.mobile, self.userId, self.cookie)
        # 判断路径是否已存在, 存在则读取
        if os.path.exists('/storage/emulated/0/shuabu/record_data.txt'):
            # 先读取原有数据
            with open('/storage/emulated/0/shuabu/record_data.txt', 'r+', encoding='utf-8') as fp:
                # 已存在数据
                user_data = fp.read()
            # 将重叠的数据删除
            with open('/storage/emulated/0/shuabu/record_data.txt', 'w+', encoding='utf-8') as fp:
                # 重叠格式
                pattern = re.compile('<account>{},{},(.*?)</account>\s'.format(self.mobile, self.userId))
                # 寻找重叠cookie
                overlap_cookie = pattern.findall(user_data)
                # 替换为空白字符串
                for co in overlap_cookie:
                    data = '<account>{},{},{}</account>\n'.format(self.mobile, self.userId, co)
                    user_data = user_data.replace(data, '')
                # 消除空白字符
                user_data = user_data.replace(' ', '')
                # 重新拼接record_data
                record_data = user_data + record_data
                # 写入
                fp.write(record_data)
        # 不存在则直接创建
        else:
            with open('/storage/emulated/0/shuabu/record_data.txt', 'w+', encoding='utf-8') as fp:
                fp.write(record_data)

    ####################################################执行修改##########################################################
    # 刷步
    def modify(self):
        # <第三次>移除input,confirm #-----------------------------------# <第三次>移除input,confirm
        self.frame_box.remove_widget(self.input)
        self.frame_box.remove_widget(self.confirm)
        # tip1提示正在尝试修改
        self.tip2.text = ""
        self.tip1.text = "正在尝试修改......"

        # 获取第三次input值并转换为整数类型
        steps = int(self.input.text)
        # 运动距离与消耗的卡路里验证参数, 必须传入
        distance = steps / 3
        calories = int(steps / 4000)

        # 提交步数的url
        modify_url = 'https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?city=%E4%B8%8A%E6%B5%B7&province=%E4%B8%8A%E6%B5%B7%E5%B8%82&devicemodel=Magic2&areaCode=310109&osversion=5.1.1&screenHeight=1280&provinceCode=310000&version=4.5&channel=huawei&systemType=2&promotion_channel=huawei&screenWidth=720&requestId=d6e3e55379914cbd86ebbe975b19a877&longitude=121.492479&screenheight=1280&os_country=CN&timezone=Asia%2FShanghai&cityCode=310100&os_langs=zh&platform=android&clientId=8e844e28db7245eb81823132464835eb&openudid=&countryCode=&country=%E4%B8%AD%E5%9B%BD&screenwidth=720&network_type=wifi&appType=6&area=CN&latitude=31.247221&language=zh'
        # 请求头(已传入cookie)
        modify_headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Magic2 Build/LMY48Z)',
            'Host': 'sports.lifesense.com',
            'Connection': 'Keep-Alive',
            'Cookie': self.cookie,
        }

        # 所需数据
        modify_data = {
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
                    "step": steps,
                    "type": 2,
                    "updated": int((str(int(time.time()) * 1000).split('.'))[0]),
                    "userId": self.userId,
                    "DataSource": 2,
                    "exerciseTime": 0
                }
            ]
        }

        # 发送请求
        # 成功则回调show_result,其余同上
        login_request = UrlRequest(url=modify_url,
                                   on_error=self.show_error,
                                   on_failure=self.show_failure,
                                   on_success=self.show_result,
                                   req_body=json.dumps(modify_data),
                                   req_headers=modify_headers,
                                   verify=False)

    ##################################################返回修改结果#########################################################
    # 返回修改结果
    def show_result(self, resp, result):
        # 获取修改状态码
        modify_code = result['code']

        # <第四次>加入input,confirm #-----------------------------------# <第四次>加入input,confirm
        self.frame_box.add_widget(self.input)
        self.frame_box.add_widget(self.confirm)

        # 判断是否修改成功
        # 修改失败
        if modify_code != 200:
            # tip1提示修改失败
            # tip2提示可重试
            self.tip1.text = '修改失败!'
            self.tip2.text = '请重新登陆再试:'
            # 清除原输入
            self.input.text = ''
            # 解绑原函数
            self.confirm.unbind(on_press=self.confirm_steps)
            # 绑定根函数
            self.confirm.bind(on_press=self.confirm_mobile)
        else:
            # tip1提示修改成功
            # tip2提示可继续修改
            self.tip1.text = "修改成功!"
            self.tip2.text = "您可以继续修改:"
            # 解绑原函数
            self.confirm.unbind(on_press=self.confirm_steps)
            # 重新绑定
            self.confirm.bind(on_press=self.confirm_steps)


if __name__ == '__main__':
    StepsModify().run()
