import json, sys, openpyxl, time

class install_Excel:
    def __init__(self, file_name, file_title_name, projectname='home'):
        """

        :param file_name: 文件名
        :param file_title_name: 工作表
        :param projectname:  项目根路径
        """
        self.file_name = file_name
        self.file_title_name = file_title_name
        self.projectname = projectname
        self.sheet_header = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']  # 创建文件表头列表

    def files_path(self):
        return f"{sys.path[0].split(self.projectname)[0]}{self.projectname}/API_project/report/Excel/{self.file_name}.xlsx"

    def files(self):
        try:
            file = openpyxl.load_workbook(
                f"{sys.path[0].split(self.projectname)[0]}{self.projectname}/API_project/report/Excel/{self.file_name}.xlsx")  # 打开表格文件
        except:
            file = openpyxl.Workbook()  # 创建新表
            file.active.title = self.file_title_name  # 更改默认表名
            # file.active.title = '涵盖证书类型'  # 更改默认表名
            # ws = wb.get_sheet_by_name('涵盖证书类型') #打开更改后的表格
        return file

    def file(self, file):
        try:
            ws = file[self.file_title_name]  # 打开文件
            # wl = wb.create_sheet("1") #打开表格索引为1的表格
            # ws = file.active #打开默认表格
        except:
            ws = file.create_sheet(title=self.file_title_name)  # 创建新文件
            # ws = file.create_sheet(title = 'biaoge3',index= 1 ) #创建新表
        return ws

    def install(self, row=1, column=1, value="条件"):
        """

        :param row: 行
        :param column: 列
        :param value:  写入值
        :return:
        """
        try:
            file = openpyxl.load_workbook(
                f"{sys.path[0].split(self.projectname)[0]}{self.projectname}/API_project/report/Excel/{self.file_name}.xlsx")  # 打开表格文件
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
        ws.cell(row=row, column=column).value = value  #写入内容
        file.save(
            f"{sys.path[0].split(self.projectname)[0]}{self.projectname}/API_project/report/Excel/{self.file_name}.xlsx")  #保存文件

    def read_sum(self, index=None):
        try:
            file = openpyxl.load_workbook(
                f"{sys.path[0].split(self.projectname)[0]}{self.projectname}/API_project/report/Excel/{self.file_name}.xlsx")  # 打开表格文件
        except:
            file = openpyxl.Workbook()  # 创建新表
            file.active.title = self.file_title_name  # 更改默认表名
        try:
            ws = file[self.file_title_name]  # 打开文件
        except:
            ws = file.create_sheet(title=self.file_title_name)  # 创建新文件
        ws_max_row = ws.max_row #最大行
        ws_max_column = ws.max_column  # 最大列
        # if index is not None:
        #     row_list = []  # 创建case名称标题列表
        #     for i in ws[1]:  # 获取case列表标题
        #         row_list.append(i.value)  # 将case标题添加到名称标题列表，追加模式
        #     ws_sum = len(ws[self.sheet_header[row_list.index(index)]])  # 获取用例索引
        # else:
        #     ws_sum = len(ws['A'])
        ws_sum = ws.min_row
        return ws_max_row

    def read_one_value(self):
        try:
            file = openpyxl.load_workbook(
                f"{sys.path[0].split(self.projectname)[0]}{self.projectname}/API_project/report/Excel/{self.file_name}.xlsx")  # 打开表格文件
        except:
            file = openpyxl.Workbook()  # 创建新表
            file.active.title = self.file_title_name  # 更改默认表名
        try:
            ws = file[self.file_title_name]  # 打开文件
        except:
            ws = file.create_sheet(title=self.file_title_name)  # 创建新文件
        ws_sum = ws['A1'].value
        return ws_sum


if __name__ == '__main__':
    # install = install_Excel(file_name="测试", file_title_name="测试1")
    # install.install(row=1, column=1, value="1")
    # install.install(row=2, column=1, value="2")
    # install.install(row=3, column=1, value="3")
    # file_name = time.strftime("%Y-%m-%d %H:%M:%S").split(":")[0].replace("-", "_").replace(" ", "_")
    # install_files = install_Excel(file_name="找企业联系方式121", file_title_name=file_name)
    # row_sum = 1
    # install_files.install(row=1, column=1, value='pid')
    # install_files.install(row=1, column=2, value='entName')
    # install_files.install(row=1, column=3, value='搜索条件')
    # install_files.install(row=1, column=4, value='断言')
    # install = install_Excel(file_name="测试", file_title_name="测试1")
    # files = install.files()
    # file = install.file(file=files)
    # file.cell(row=1, column=1).value = "value111"
    # file.cell(row=2, column=1).value = "value211"
    # file.cell(row=3, column=1).value = "value311"
    # file.cell(row=4, column=1).value = "value411"
    # file.cell(row=5, column=1).value = "value511"
    # files.save(install.files_path())
    file_name = time.strftime("%Y年%m月%d日%H时%M分")
    install_files = install_Excel(file_name="test_prod_stagin", file_title_name=file_name)
    row_sum = install_files.read_sum() + 1
    print(row_sum)
    # install_files.install(row=1, column=1, value='pid')
    print(install_files.read_one_value() is None)
