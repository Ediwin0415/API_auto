# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 15:18
# @Author  : czc
# @FileName: tool_headers.py
# @Software: PyCharm

from config.config import COOKIE_FILE

class headersPack:
    def __init__(self, response):
        self.response = response

    # 获取登录的cookie
    def get_login_cookie(self):
        cookie = self.response['Token']
        return cookie

    #生成headers
    def create_headers(self):
        cookie = self.get_login_cookie()
        headers = {"token": str(cookie)}
        fp = open(file=COOKIE_FILE, mode='w+', encoding='utf-8')
        fp.write(str(headers).replace("'", '"'))
        fp.close()