import json, sys, openpyxl, time

# print(sys.argv[0])
projectname = 'API_project'


# print(f"{sys.argv[0].split(projectname)[0]}{projectname}/report/Excel/涵盖证书类型.xlsx")


# class Excel_Files:
#     def __init__(self, file_name='访客识别-用例.xlsx', sheel='中企接口'):
#         '''
#         :param file_name: 用例文件
#         :param sheel: 文件sheel
#         '''
#         self.file_name = file_name
#         self.sheel = sheel
#         self.file = openpyxl.load_workbook(f'..\\Data\\Exce\\{file_name}')  # 打开用例文件
#         self.sheet_header = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']  # 创建文件表头列表
#         self.sheel_file = self.file[sheel]  # 打开用例文件内容
#
#     def excel_index(self, index):
#         '''
#         :param index: 文件表头
#         :return: 表头索引
#         '''
#         row_list = []  # 创建case名称标题列表
#         for i in self.sheel_file[1]:  # 获取case列表标题
#             row_list.append(i.value)  # 将case标题添加到名称标题列表，追加模式
#         case_index = row_list.index(index)  # 获取用例索引
#         return case_index
#
#     def open_case(self, request_name='入参', response_name='出餐', Sizer_name='用例标题', Sizer_name_v='前置条件', Sizer_value=[]):
#         '''
#         :param request_name: 入参表头
#         :param response_name: 出参表头
#         :param Sizer_name: 用例标题表头
#         :param Sizer_value: 用例标题
#         :return: 用例
#         '''
#         case_list = []
#         Sizer_name_len = len(
#             self.sheel_file[self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(Sizer_name)]])
#         # print(
#         #     len(self.sheel_file[self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(request_name)]])) #打印用例数量含空用例
#         for i in range(Sizer_name_len):  # 通过用例索引循环全部用例
#             Sizer_name_value = (self.sheel_file[
#                 str(self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(Sizer_name)]) + str(
#                     i + 1)]).value  # 获取用例标题
#             Sizer_name_valu = (self.sheel_file[
#                 str(self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(Sizer_name_v)]) + str(
#                     i + 1)]).value  # 获取用例标题
#
#             if Sizer_name_value is not None and Sizer_name_value != Sizer_name:  # 判断用例标题不为空 跳过第一行标题
#                 response_value = (self.sheel_file[
#                     self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(response_name)] + str(
#                         i + 1)]).value  # 通过响应索获取响应内容
#                 request_value = (self.sheel_file[
#                     self.sheet_header[Excel_Files(self.file_name, self.sheel).excel_index(request_name)] + str(
#                         i + 1)]).value  # 通过请求索获取请求内容
#                 #     continue
#                 if isinstance(request_value, str):  # 首先判断变量是否为字符串
#                     try:
#                         congig_text = json.loads(request_value)  #
#                     except ValueError:
#                         request_value = request_value
#                     else:
#                         request_value = congig_text
#                 if isinstance(response_value, str):  # 首先判断变量是否为字符串
#                     try:
#                         congig_text = json.loads(response_value)  #
#                     except ValueError:
#                         response_value = response_value
#                     else:
#                         response_value = congig_text
#                 if Sizer_value != []:  # 判断用例筛选不为空
#                     if Sizer_name_value in Sizer_value:  # 判断用例符合筛选内容
#                         case_list.append((request_value, response_value, Sizer_name_valu))  # 将用例入参和出餐写入用例表格
#                 else:
#                     case_list.append((request_value, response_value, Sizer_name_valu))  # 若不进行筛选 直接将用例入参和出餐写入用例表格
#         return case_list
class install_Excel:
    def __init__(self, file_name, file_title_name):
        self.file_name = file_name
        self.file_title_name = file_title_name

    def files_path(self):
        return f"{sys.argv[0].split(projectname)[0]}{projectname}/report/Excel/{self.file_name}.xlsx"

    def files(self, row=1, column=1, value="条件", ):
        try:
            file = openpyxl.load_workbook(
                f"{sys.argv[0].split(projectname)[0]}{projectname}/report/Excel/{self.file_name}.xlsx")  # 打开表格文件
        except:
            file = openpyxl.Workbook()  # 创建新表
            file.active.title = self.file_title_name  # 更改默认表名
            # file.active.title = '涵盖证书类型'  # 更改默认表名
            # ws = wb.get_sheet_by_name('涵盖证书类型') #打开更改后的表格
        return file

    def file(self, file, save=False):
        try:
            ws = file[self.file_title_name]  # 打开文件
            # wl = wb.create_sheet("1") #打开表格索引为1的表格
            # ws = file.active #打开默认表格
        except:
            ws = file.create_sheet(title=self.file_title_name)  # 创建新文件
            # ws = file.create_sheet(title = 'biaoge3',index= 1 ) #创建新表
        return ws

    def install(self, row=1, column=1, value="条件"):
        try:
            file = openpyxl.load_workbook(
                f"{sys.argv[0].split(projectname)[0]}{projectname}/report/Excel/{self.file_name}.xlsx")  # 打开表格文件
        except:
            file = openpyxl.Workbook()  # 创建新表
            file.active.title = self.file_title_name  # 更改默认表名
            # file.active.title = '涵盖证书类型'  # 更改默认表名
            # ws = wb.get_sheet_by_name('涵盖证书类型') #打开更改后的表格
        try:
            ws = file[self.file_title_name]  # 打开文件
            # wl = wb.create_sheet("1") #打开表格索引为1的表格
            # ws = file.active #打开默认表格
        except:
            ws = file.create_sheet(title=self.file_title_name)  # 创建新文件
            # ws = file.create_sheet(title = 'biaoge3',index= 1 ) #创建新表

        ws.cell(row=row, column=column).value = value
        file.save(f"{sys.argv[0].split(projectname)[0]}{projectname}/report/Excel/{self.file_name}.xlsx")



if __name__ == '__main__':
    # install = install_Excel(file_name="测试", file_title_name="测试1")
    # install.install(row=1, column=1, value="1")
    # install.install(row=2, column=1, value="2")
    # install.install(row=3, column=1, value="3")
    file_name = time.strftime("%Y-%m-%d %H:%M:%S").split(":")[0].replace("-", "_").replace(" ", "_")
    install_files = install_Excel(file_name="找企业联系方式", file_title_name=file_name)
    row_sum = 1
    install_files.install(row=1, column=1, value='pid')
    install_files.install(row=1, column=2, value='entName')
    install_files.install(row=1, column=3, value='搜索条件')
    install_files.install(row=1, column=4, value='断言')
    # install = install_Excel(file_name="测试", file_title_name="测试1")
    # files = install.files()
    # file = install.file(file=files)
    # file.cell(row=1, column=1).value = "value111"
    # file.cell(row=2, column=1).value = "value211"
    # file.cell(row=3, column=1).value = "value311"
    # file.cell(row=4, column=1).value = "value411"
    # file.cell(row=5, column=1).value = "value511"
    # files.save(install.files_path())
