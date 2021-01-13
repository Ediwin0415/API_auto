# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 20:25
# @Author  : czc
# @FileName: run.py
# @Software: PyCharm

import pytest
from tools.tool_manager import TestManager

if __name__=="__main__":
    mytest=TestManager()
    mytest.del_old_result() # 删除旧的测试结果数据
    pytest.main()
    mytest.generate_report()  # 生成测试报告

