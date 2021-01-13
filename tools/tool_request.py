# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 19:09
# @Author  : czc
# @FileName: tool_request.py
# @Software: PyCharm

# coding:utf-8
# ==============================
#         请求的封装
# ==============================
import requests
from config.config import env, URL
from tools.tool_log import logger

log = logger()


class Requests:
    def send_get(self, url, params=None, headers=None):
        if headers == None:
            res = requests.get(url=url, params=params,verify=False)
        else:
            res = requests.get(url=url, params=params, headers=headers,verify=False)
        return res

    def send_post(self, url, data, headers=None):
        if headers == None:
            res = requests.post(url=url, json=data,verify=False)
        else:
            res = requests.post(url=url, json=data, headers=headers,verify=False)
        return res

    def send_put(self, url, data, headers=None):
        if headers == None:
            res = requests.put(url=url, data=data)
        else:
            res = requests.put(url=url, data=data, headers=headers)
        return res

    def send_delete(self, url, data, headers=None):
        if headers == None:
            res = requests.delete(url=url, data=data)
        else:
            res = requests.delete(url=url, data=data, headers=headers)
        return res

    def send_request(self, method, url, data, headers=None):
        log.info(f"method:{method}")
        log.info(f"url:{url}")
        log.info(f"data:{data}")
        res = None
        # 适应多环境
        if URL in url:
            url = url.replace(URL, env[URL][env["default"]])
            if headers != None:
                headers["Host"] = URL
        if method == 'get':
            res = self.send_get(url=url, params=data, headers=headers)
        elif method == 'post':
            res = self.send_post(url=url, data=data, headers=headers)
        elif method == 'put':
            res = self.send_put(url=url, data=data, headers=headers)
        elif method == 'delete':
            res = self.send_delete(url=url, data=data, headers=headers)
        return res


if __name__ == '__main__':
    req = Requests()
    res = req.send_request(
        method='POST',
        url="https://192.168.1.205/api/cmdb/user/login",
        data={
            'account': 'Ediwin',
            'password': '5184715875cdb3c620966d184e2f84d111b17e6327308d351f2cb187bb2d91c4',
            'type': 0
        },
        headers=None
    )
    # print(res)

