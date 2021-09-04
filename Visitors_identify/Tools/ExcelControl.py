# -*- coding: utf-8 -*-
# @Time    : 2021/8/4—12:50
# @Author  : 孟艳红
# @File    : ExcelControl.py
import openpyxl,json


class Excel_Files:
    def __init__(self, file_name='访客识别-用例.xlsx', sheel='中企接口'):
        '''
        :param file_name: 用例文件
        :param sheel: 文件sheel
        '''
        self.file_name = file_name
        self.sheel = sheel
        self.file = openpyxl.load_workbook(f'..\\Data\\Exce\\{file_name}')  # 打开用例文件
        self.sheet_header = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']  # 创建文件表头列表
        self.sheel_file = self.file[sheel]  # 打开用例文件内容

    def excel_index(self, index):
        '''
        :param index: 文件表头
        :return: 表头索引
        '''
        row_list = []  # 创建case名称标题列表
        for i in self.sheel_file[1]:  # 获取case列表标题
            row_list.append(i.value)  # 将case标题添加到名称标题列表，追加模式
        case_index = row_list.index(index)  # 获取用例索引
        return case_index

    def open_case(self, request_name='入参', response_name='出餐', Sizer_name='用例标题',Sizer_name_v='前置条件', Sizer_value=[]):
        '''
        :param request_name: 入参表头
        :param response_name: 出参表头
        :param Sizer_name: 用例标题表头
        :param Sizer_value: 用例标题
        :return: 用例
        '''
        case_list = []
        Sizer_name_len = len(self.sheel_file[self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(Sizer_name)]])
        # print(
        #     len(self.sheel_file[self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(request_name)]])) #打印用例数量含空用例
        for i in range(Sizer_name_len):  # 通过用例索引循环全部用例
            Sizer_name_value = (self.sheel_file[
                str(self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(Sizer_name)]) + str(
                    i + 1)]).value # 获取用例标题
            Sizer_name_valu = (self.sheel_file[
                str(self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(Sizer_name_v)]) + str(
                    i + 1)]).value  # 获取用例标题

            if Sizer_name_value is not None and Sizer_name_value != Sizer_name: # 判断用例标题不为空 跳过第一行标题
                response_value = (self.sheel_file[
                    self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(response_name)] + str(
                        i + 1)]).value # 通过响应索获取响应内容
                request_value = (self.sheel_file[
                    self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(request_name)] + str(
                        i + 1)]).value  # 通过请求索获取请求内容
                #     continue
                if isinstance(request_value, str):  # 首先判断变量是否为字符串
                    try:
                        congig_text = json.loads(request_value)  #
                    except ValueError:
                        request_value=request_value
                    else:
                        request_value=congig_text
                if isinstance(response_value, str):  # 首先判断变量是否为字符串
                    try:
                        congig_text = json.loads(response_value)  #
                    except ValueError:
                        response_value=response_value
                    else:
                        response_value=congig_text
                if Sizer_value != []:  # 判断用例筛选不为空
                    if Sizer_name_value in Sizer_value:   # 判断用例符合筛选内容
                        case_list.append((request_value,response_value,Sizer_name_valu))   # 将用例入参和出餐写入用例表格
                else:
                    case_list.append((request_value,response_value,Sizer_name_valu))  # 若不进行筛选 直接将用例入参和出餐写入用例表格
        return case_list


if __name__ == '__main__':
    Excel = Excel_Files().open_case(Sizer_value=['站点接口-添加图片','站点接口-添加图片错误校验'])
    print(type(Excel[-1]))
    print(Excel[-1])
    print(Excel)
