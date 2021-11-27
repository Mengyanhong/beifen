import xlrd
"""
目标：使用excel测试用例实现登录接口的自动化测试！
流程：
    1- 测试接口文档-----ok
    2- 测试用例文件-----ok
    3- 实现登录接口的代码编辑---ok
    4- 读取测试用例-----x
    5- 登录接口结合excel用例实现自动化测试！-----x
"""

#----------------读取excel用例数据-----------------------
"""
需求：实现一个excel用例读取功能
版本:v1.0
具体功能：
    1- 读取指定的数据
    2- 具备过滤一些无效用例
实现方案：
    1- 打开excel文件
    2- 读取对应数据
    3- 过滤数据
    4- 关闭
"""
#---------------版本迭代-------------------
"""
版本：v1.1
功能描述：
    1- 可以用户选择任何列数据  
        1- 列编号  9,11
        2- 列名--更适合！URL 前置条件
    2- 分类筛选
        1- 全部执行   -all
        2- 分段执行   tc003-tc007
        3- 随机执行   tc001,tc007,tc009
        4- 复合场景   ['tc001','tc004-tc007','tc009']
"""
#----------------读取excel用例数据-----------------------
"""
需求：实现一个excel用例读取功能
版本:v1.0
具体功能：
    1- 读取指定的数据
    2- 具备过滤一些无效用例
实现方案：
    1- 打开excel文件
    2- 读取对应数据
    3- 过滤数据
测试反馈：
    1- 不能挑选个别，或者一段用例执行
    2- 不能选择性获取某些列
"""
#---------------版本迭代-------------------
"""
版本：v1.2
功能描述：
    1- 可以用户选择任何列数据  
        1- 列编号  9,11
        2- 列名--更适合！URL 前置条件
    2- 分类筛选
        1- 全部执行   -all
        2- 分段执行   tc003-tc007
        3- 随机执行   tc001,tc007,tc009
        4- 复合场景   ['tc001','tc004-tc007','tc009']
"""


class get_excel_data:
    def __init__(self, exceDir, sheetName, caseName,*colName,selectCase=["all"]):  # 初始化操作数据
        """
        :param exceDir: #文件路径
        :param sheetName:  #操作的表名
        :param caseName: #获取的用例名称
        """
        self.excelDir = exceDir
        self.sheetName = sheetName
        self.caseName = caseName
        self.colName = colName
        self.selectCase = selectCase

    def get_exce_data1(self):
        # 1- 加载Excel文件
        # formatting_info=True 保持表格样式不变
        workBook = xlrd.open_workbook(self.excelDir, formatting_info=True)
        # 2- 查看表格有哪些sheet（字表）
        # print(workBook.sheet_names())
        # 3- 获取需要操作的表格
        worksheet = workBook.sheet_by_name(self.sheetName)
        # 4- Excel表格下标从0开始
        # print(worksheet.row_values(0)) #获取第0行数据
        # print(worksheet.col_values(0)) #获取第0列数据
        # 5- 获取某一个单元格内的数据
        # print(worksheet.cell(1,2).value) #获取第一行第二列的数据

        idex = 0  # 初始值（行）
        reslist = []  # 存放结果列表
        for one in worksheet.col_values(0):  # 遍历第0行数据
            # 1- 筛选用例:无效的用例/不相关的接口用例
            if self.caseName in one:
                reqData = worksheet.cell(idex, 1).value  # 获取case的第1列数据
                expData = worksheet.cell(idex, 2).value  ##获取case的第2列数据
                # 每一组数据 （请求数据，响应期望数据）
                reslist.append((reqData, expData))
            idex += 1
        return reslist

    def get_excel_data2(self):
        """
        :param excelDir: excel路径
        :param sheetName: 操作的表名
        :param caseName: #获取的用例名
        :return: 返回一个list
        :*args：不定项列名
        """
        # 1- 打开/加载excel文件---
        # formatting_info=True  保持excel样式
        workBook = xlrd.open_workbook(self.excelDir, formatting_info=True)
        # 3- 获取需要操作的表
        workSheet = workBook.sheet_by_name(self.sheetName)

        # ---------思路的转换------------
        # 背景：用户输入的列名，但是python处理获取对应列的数据使用的列编号！
        colIdex = []  # 列名的下标存放！
        for i in self.colName:
            # workSheet.row_values(0)--第0行数据 是一个列表，列表通过值取 下标 index
            colIdex.append(workSheet.row_values(0).index(i))
        print("列名下标>>>", colIdex)
        # -----------------------------

        idex = 0  # 行的初始值
        resList = []  # 返回的结果！
        for one in workSheet.col_values(0):
            # 1- 筛选用例:无效的用例/不相关的接口用例
            if self.caseName in one:
                getColData = []  # 列表获取到的数据组合
                for num in colIdex:  # 遍历列名下标
                    res = workSheet.cell(idex, num).value
                    getColData.append(res)  # 这个是列存放列表！
                # 每一组数据 （请求数据，响应期望数据）
                resList.append(getColData)  # resList  行存放列表
            idex += 1  #
        return resList

    def get_excel_data3(self):
        """
        :param excelDir: excel路径
        :param sheetName: 操作的表名
        :param caseName: #获取的用例名
        :return: 返回一个list
        :*args：不定项列名
        :selectCase=["all"]
        """
        # 1- 打开/加载excel文件---
        # formatting_info=True  保持excel样式
        workBook = xlrd.open_workbook(self.excelDir, formatting_info=True)
        # 3- 获取需要操作的表
        workSheet = workBook.sheet_by_name(self.sheetName)

        # ---------思路的转换------------
        # 背景：用户输入的列名，但是python处理获取对应列的数据使用的列编号！
        colIdex = []  # 列名的下标存放！
        for i in self.colName:
            # workSheet.row_values(0)--第0行数据 是一个列表，列表通过值取 下标 index
            colIdex.append(workSheet.row_values(0).index(i))
        print("列名下标>>>", colIdex)
        # -----------------------------

        # ------筛选用例----------------------
        selectList = []
        if self.selectCase[0] == "all":
            # 就是执行第0列数据
            selectList = workSheet.col_values(0)
        else:  # ["001","003-006"]
            for one in self.selectCase:
                if "-" in one:  # 分段的类型
                    start, end = one.split('-')  # 003   006
                    for i in range(int(start), int(end) + 1):
                        selectList.append(self.caseName + f"{i:0>3}")  # ["Login003","Login004"]
                else:
                    selectList.append(self.caseName + f"{one:0>3}")  # ["Login003","Login004"]
        ## ["Login001","Login003","Login004","Login005","Login006"]
        # --------------------------------

        idex = 0  # 行的初始值
        resList = []  # 返回的结果！
        for one in workSheet.col_values(0):
            # 1- 筛选用例:无效的用例/不相关的接口用例
            if self.caseName in one and one in selectList:
                getColData = []  # 列表获取到的数据组合
                for num in colIdex:  # 遍历列名下标
                    res = workSheet.cell(idex, num).value
                    getColData.append(res)  # 这个是列存放列表！
                # 每一组数据 （请求数据，响应期望数据）
                resList.append(getColData)  # resList  行存放列表
            idex += 1  #
        return resList

