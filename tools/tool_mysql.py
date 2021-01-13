# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 15:43
# @Author  : czc
# @FileName: tool_mysql.py
# @Software: PyCharm

import pymysql


class mysqlPack:
    def __init__(self, conn=None):
        if conn == None:
            self.conn = pymysql.connect(
                host='192.168.1.205',
                port=20000,
                user='gsuser',
                password='Gs@db?>>',
                db='ops_center',
                charset='utf8'
            )
        else:
            self.conn = conn
        print(111)
        self.c = self.conn.cursor()
        print(222)

    # 发送mysql命令
    def send_mysql_command(self, str):
        print(333)
        self.c.execute(str)
        print(444)

    # 读取一行
    def read_mysql_oneLine(self):
        print(555)
        return self.c.fetchone()
        print(666)

    # 读取全部行
    def read_mysql_allLine(self):
        return self.c.fetchall()

    # 输出列表
    def get_mysql_list(self):
        for i in range(self.c.rowcount):
            print(self.c.fetchone())


if __name__ == "__main__":
    c=mysqlPack()
    c.send_mysql_command("select * from sys_user where account='Ediwin'")
    print(c.read_mysql_oneLine())
