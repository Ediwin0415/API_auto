# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 13:53
# @Author  : czc
# @FileName: config.py
# @Software: PyCharm

import os
import datetime

# -------------项目根目录------------------
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------数据文件-------------------
DATA_PATH = os.path.join(BASE_PATH, "data")
COOKIE_FILE = os.path.join(DATA_PATH, "cookie.json")

# -------------环境配置--------------------
URL = "192.168.1.205"
# env = {
#     URL: {
#         "dev": "192.168.1.205",  # 线上环境
#         "test": "192.168.1.205"  # 生产环境
#     },
#     "default": "test"
# }

# -------------bat文件相关------------------
BAT_FILE = os.path.join(BASE_PATH, "bat", "generate_report.bat")
RUN_SERVER_FILR = os.path.join(BASE_PATH, "bat", "run_allure_server.bat")

# -------------测试报告----------------------
REPORT_PATH = os.path.join(BASE_PATH, "report")
REPORT_RESULT_PATH = os.path.join(REPORT_PATH, "allure_result")
REPORT_END_PATH = os.path.join(REPORT_PATH, "allure_report")
REPORT_HISTORY_PATH = os.path.join(REPORT_PATH, "allure_report", "history")

# -------------EXCEL相关----------------------
EXCEL_FILE=os.path.join(BASE_PATH,"excel","接口文档.xls")

# -------------日志相关------------------------
# 日志级别
LOG_LEVEL='debug'
LOG_STREAM_LEVEL='debug' # 屏幕输出流
LOG_FILE_LEVEL='info' # 文件输出流
# 日志命名
LOG_FOLDER=os.path.join(BASE_PATH,'logs')
LOG_FILE_NAME=os.path.join(LOG_FOLDER, datetime.datetime.now().strftime('%Y-%m-%d')+'.log')

# --------------邮件相关------------------------
# 邮件文件列表
FILE_LIST=[
    os.path.join(BASE_PATH,"report","zip","report.zip")
]

# -------------压缩文件相关------------------------
# 要压缩文件夹的根路径
REPORT_DIR=os.path.join(BASE_PATH,"report","allure_report")

# -------------Email相关--------------------------
EMAIL_FROMADDR='xxxxx@xxx.com' # 发送人邮箱
EMAIL_PASSWORD='xxxxxx' # 发件人授权码
EMAIL_TOADDR = [        # 收件人地址列表
    'xxxxxxxx@xx.com'
]

if __name__=="__main__":
    print(env[URL][env["default"]])






