# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 15:02
# @Author  : czc
# @FileName: tool_global_var.py
# @Software: PyCharm

# ===============================
#       EXCEL列封装
# ===============================
class global_var:
    test_id = 0
    test_module = 1
    test_function = 2
    test_run = 3
    test_url = 4
    test_data = 5
    test_run_way = 6
    test_cookie = 7
    test_case_depend = 8   # case依赖
    test_field_depend = 9  # 数据依赖字段
    test_expect = 10
    test_result = 11
    test_response = 12


def get_id():
    return global_var.test_id


def get_module():
    return global_var.test_module


def get_fuction():
    return global_var.test_function


def get_url():
    return global_var.test_url


def get_run():
    return global_var.test_run


def get_run_way():
    return global_var.test_run_way


def get_cookie():
    return global_var.test_cookie


def get_case_depend():
    return global_var.test_case_depend


def get_filed_depend():
    return global_var.test_field_depend


def get_data():
    return global_var.test_data


def get_expect():
    return global_var.test_expect


def get_result():
    return global_var.test_result


def get_response():
    return global_var.test_response
