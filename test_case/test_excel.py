# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 14:31
# @Author  : czc
# @FileName: test_excel.py
# @Software: PyCharm

import allure
import pytest
import yaml
from config.config import EXCEL_FILE
from tools.tool_excel import excelPack
from tools.tool_request import Requests
from config.config import URL

@allure.title("接口测试")  # 用例标题
class TestExcel:
    runs=Requests()
    excel=excelPack(file_name=EXCEL_FILE,runs=runs)
    excel.clear_cookie()
    results=excel.run_excel_case()
    excel.write_test_summary()

    @allure.severity(allure.severity_level.CRITICAL)  # 发生BUG时的严重程度
    @pytest.mark.parametrize("result", results)
    def test_excel(self, result):
        allure.dynamic.title(str(result['title']))
        allure.dynamic.description(f"{str(result['method'])} {str(result['url'])}")
        with allure.step(f"method:{str(result['method'])}"):
            pass
        with allure.step(f"url:{str(result['url'])}"):
            pass
        with allure.step(f"data:{str(result['data'])}"):
            pass
        with allure.step(f"res:{str(result['res'].json())}"):
            pass
        with allure.step(f"响应时间:{str(result['res'].elapsed.total_seconds())}s"):
            pass
        assert result["result"] == "pass"


if __name__ == '__main__':
    pytest.main()

