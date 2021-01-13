# coding:utf-8
# ==============================
#         EXCEL处理封装
# ==============================
import xlrd
import xlwt
import json
import re
from xlutils.copy import copy
from tools import tool_global_var
from tools.tool_headers import headersPack
from tools.tool_log import logger
from tools.tool_request import Requests
from config.config import EXCEL_FILE, COOKIE_FILE,URL

log = logger()


class excelPack:
    def __init__(self, file_name=None, sheet_id=None, runs=None):
        if file_name:  # 有文件名用文件名，没有用默认值
            self.file_name = file_name
        else:
            self.file_name = EXCEL_FILE
        if sheet_id:  # 有表id用表id，没有默认为0
            self.sheet_id = sheet_id
        else:
            self.sheet_id = 0
        self.pass_num = 0   # 获取失败条数
        self.fail_num = 0   # 获取成功条数
        self.runs = runs    # Requests
        self.sheet_data = self.get_sheet_data()  # 获取表数据

    # 获取sheet的内容
    def get_sheet_data(self):
        book = xlrd.open_workbook(self.file_name, formatting_info=True)
        sheet = book.sheet_by_index(self.sheet_id)
        return sheet

    # 获取行数
    def get_lines(self):
        return self.sheet_data.nrows

    # 获取某个单元格内容
    def get_cell_data(self, row, col):
        return self.sheet_data.cell(row, col).value

    # 向单元格写内容
    def write_cell_data(self, row, col, value, cell_style=0):
        al = xlwt.Alignment() # 设置对齐方式
        style = xlwt.XFStyle() # 字体样式
        font = xlwt.Font() # 字体设置
        if cell_style == 1:
            al.vert = 0x01  # 设置垂直居中
            # al.wrap = 1  # 自动换行
        elif cell_style == 2:
            al.vert = 0x01  # 设置垂直居中
        elif cell_style == 3:
            al.vert = 0x01  # 设置垂直居中
            font.bold = True  # 设置粗体
            font.colour_index = 3  # 设置绿色
        elif cell_style == 4:
            al.vert = 0x01  # 设置垂直居中
            font.bold = True  # 设置粗体
            font.colour_index = 2  # 设置红色
        style.alignment = al
        style.font = font
        book = xlrd.open_workbook(self.file_name, formatting_info=True)
        book_copy = copy(book)
        sheet = book_copy.get_sheet(self.sheet_id)
        sheet.write(row, col, value, style)
        book_copy.save(self.file_name)

    # 生成依赖列表
    def get_case_list(self, row):
        case_col = tool_global_var.get_case_depend()
        case_depend = self.get_cell_data(row, case_col)
        case_depend_list = []
        if case_depend != "":
            case_depend_list = case_depend.split(";")
        return case_depend_list

    # 获取所依赖的用例响应值
    def get_case_line(self, case_str, row):
        for num in range(1, row):
            if case_str == self.get_cell_data(num, tool_global_var.get_id()):
                response_data = self.get_cell_data(num, tool_global_var.get_response())
                return response_data
        return "【CANNOT_FIND】"

    # 获取需要匹配的字符串并返回url
    def get_new_url(self, row, url):
        while True:
            try:
                value = re.search("{{(.+?)}}", url).group()
                list = value.replace("{{", "").replace("}}", "").split(":")
                case_id = list[0]
                case_str = list[1]
                new_str = eval(self.get_case_line(case_id, row))[case_str]
                url = url.replace(value, str(new_str))
            except:
                break
        return url

    # 生成要修改的值列表
    def get_revise_list(self, row):
        case_col = tool_global_var.get_filed_depend()
        case_depend = self.get_cell_data(row, case_col)
        case_depend_list = []
        if case_depend != "":
            case_depend_list = case_depend.split(",")
        return case_depend_list

    # 返回加入依赖后的json
    def get_case_json(self, row):
        json_data = eval(self.get_cell_data(row, tool_global_var.get_data()))
        depend_list = self.get_case_list(row) # 生成依赖列表
        revise_list = self.get_revise_list(row) # 生成要修改的值列表
        for i in range(len(depend_list)):
            case_str_list = depend_list[i].split(":")[1].split(",")
            case_id = depend_list[i].split(":")[0]
            revise_str = revise_list[i]
            for case_str in case_str_list:
                self.sheet_data = self.get_sheet_data()
                response = self.get_case_line(case_id, row) # 获取响应数据
                if response != "【CANNOT_FIND】":
                    try:
                        res_str = eval(response)['data'][case_str]  # 获取响应值
                        json_data[revise_str] = str(res_str)
                    except Exception as e:
                        pass
        # 写入返回数据
        deal_str = str(json_data).replace(r"', '", "',\n  '").replace("{'", "{\n  '").replace("'}", "'\n}")  # 格式化字典
        self.write_cell_data(row, tool_global_var.get_data(), deal_str, cell_style=1)
        return json_data

    # 写测试结果
    def write_test_result(self, row, res):
        var = tool_global_var
        if self.get_cell_data(row, var.get_expect()) in res:  # 写是否通过
            self.write_cell_data(row, var.get_result(), "PASS", cell_style=3)
            log.info(f"【测试用例{self.get_cell_data(row, var.get_id())}】===============>> 【PASS！】")
            self.pass_num += 1
            result = "pass"
        else:
            self.write_cell_data(row, var.get_result(), "FAIL", cell_style=4)
            log.info(f"【测试用例{self.get_cell_data(row, var.get_id())}】===============>> 【FAIL！】")
            self.fail_num += 1
            result = "fail"
        self.write_cell_data(row, var.get_response(), res, cell_style=2)  # 写响应结果
        return result

    # 输出测试总结
    def write_test_summary(self):
        all_num = self.pass_num + self.fail_num
        success_rate = round(self.pass_num / all_num, 3) * 100
        failure_rate = round(self.fail_num / all_num, 3) * 100
        res_str = f"本次共执行{all_num}条用例" + "\n" + f"测试通过的有{self.pass_num}条，测试失败的有{self.fail_num}条" + "\n" + f"成功率为{success_rate}%，失败率为{failure_rate}%"
        log.info(res_str)
        return res_str

    # 清空cookie
    def clear_cookie(self):
        fp = open(COOKIE_FILE, "w+", encoding="utf-8")
        fp.close()

    # 执行excel测试用例
    def run_excel_case(self):
        all_case = []  # 存储所有的请求数据，用于传输给pytest的参数
        var = tool_global_var
        for row in range(1, self.get_lines()):
            if self.get_cell_data(row, var.get_run()) == "yes":  # 是否运行
                json_data = eval(self.get_cell_data(row, var.get_data()))  # 获取excel数据
                # 用例标题
                case_name = self.get_cell_data(row, var.get_fuction())
                # 处理method
                method = self.get_cell_data(row, var.get_run_way())
                # 处理url
                url ='https://'+URL+self.get_new_url(row, self.get_cell_data(row, var.get_url()))
                # 处理data
                if self.get_cell_data(row, var.get_case_depend()) != "":
                    data = self.get_case_json(row)
                else:
                    data = json_data
                # 处理headers
                headers = None
                if self.get_cell_data(row, var.get_cookie()) == 'yes':  # 读cookie
                    try:
                        fp_cookie = open(COOKIE_FILE, mode="r", encoding="utf-8")
                        headers = json.loads(fp_cookie.read())
                        fp_cookie.close()
                    except Exception as e:
                        log.error(f"读cookie错误！\n{e}")
                # 发请求
                res = self.runs.send_request(method=method, url=url, data=data, headers=headers)
                # 写cookie
                if self.get_cell_data(row, var.get_cookie()) == 'write':
                    try:
                        cookies = headersPack(res.headers)
                        cookies.create_headers()
                    except Exception as e:
                        log.error(f"写cookie错误！\n{e}")
                # 在excel中写入结果
                try:
                    write_str = str(res.json())
                except Exception as e:
                    write_str = str("响应失败！")
                    log.error(e)
                log.info(write_str)
                result = self.write_test_result(row, write_str)
                case = {
                    "title": case_name,
                    "method": method,
                    "url": url,
                    "data": data,
                    "result": result,
                    "res": res
                }
                all_case.append(case)
        return all_case


if __name__ == '__main__':
    runs = Requests()
    excel = excelPack(file_name=EXCEL_FILE, runs=runs)
    excel.clear_cookie()
    excel.run_excel_case()
    excel.write_test_summary()
