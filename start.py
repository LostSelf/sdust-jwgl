# -*- coding:utf-8 -*-
import os
import requests
import base64
import urllib
import sys

reload(sys)

sys.setdefaultencoding('utf8')
from PIL import ImageFilter
from PIL import Image as image
import ocr
import time
#------------------------------------------------------------------#
URL_GET_GETCODE = 'http://jwgl.sdust.edu.cn/jsxsd/verifycode.servlet'
URL_POST_LOGIN = 'http://jwgl.sdust.edu.cn/jsxsd/xk/LoginToXk'
#------------------------------------------------------------------#
user = '账号'
password = '密码'


def verlify_code(content):

    f = open('verify.jpg', 'wb+')
    f.write(content)
    f.close()

    img = image.open('verify.jpg')
    img = ocr.covergrey(img)
    img = ocr.clearline(img)
    #img = ocr.clearedge(img)
    img = ocr.clearline(img)
    #img = img.filter(ImageFilter.EDGE_ENHANCE)
    img = ocr.identificationCodeHandle(img)
    # img.show()
    verlifyCode = ocr.identify(img)

    os.rename('verify.jpg', verlifyCode + '.jpg')
    return verlifyCode


for i in range(3):
    cookie = ''
    mysession = requests.session()
    code = mysession.get(URL_GET_GETCODE)
    cookie = code.headers['Set-Cookie'].split(';')[0]
    identification_code = verlify_code(code.content)
    print(identification_code)

    logindata = {}
    logindata['encoded'] = str(base64.b64encode(user.encode(
        'utf-8')))+'%%%'+str(base64.b64encode(password.encode('utf-8')))
    logindata['RANDOMCODE'] = identification_code
    logindata = urllib.urlencode(logindata)
    heard = {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie}
    login = mysession.post(URL_POST_LOGIN, logindata, headers=heard)
    login.encoding = 'utf-8'

    if '学生个人中心' in login.text:
        print('登陆成功！')
        sum = sum+1
    else:
        login.encoding = 'GB2312'
        if '验证码错误!!' in login.text:
            print('验证码错误！')
            f = open(str(sum)+'_'+identification_code+'.jpg', 'wb+')
            f.write(code.content)
            f.close()
        else:
            print('密码错误！')
