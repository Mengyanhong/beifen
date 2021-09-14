import xlrd
"""
Ŀ�꣺ʹ��excel��������ʵ�ֵ�¼�ӿڵ��Զ������ԣ�
���̣�
    1- ���Խӿ��ĵ�-----ok
    2- ���������ļ�-----ok
    3- ʵ�ֵ�¼�ӿڵĴ���༭---ok
    4- ��ȡ��������-----x
    5- ��¼�ӿڽ��excel����ʵ���Զ������ԣ�-----x
"""

#----------------��ȡexcel��������-----------------------
"""
����ʵ��һ��excel������ȡ����
�汾:v1.0
���幦�ܣ�
    1- ��ȡָ��������
    2- �߱�����һЩ��Ч����
ʵ�ַ�����
    1- ��excel�ļ�
    2- ��ȡ��Ӧ����
    3- ��������
    4- �ر�
"""
#---------------�汾����-------------------
"""
�汾��v1.1
����������
    1- �����û�ѡ���κ�������  
        1- �б��  9,11
        2- ����--���ʺϣ�URL ǰ������
    2- ����ɸѡ
        1- ȫ��ִ��   -all
        2- �ֶ�ִ��   tc003-tc007
        3- ���ִ��   tc001,tc007,tc009
        4- ���ϳ���   ['tc001','tc004-tc007','tc009']
"""
#----------------��ȡexcel��������-----------------------
"""
����ʵ��һ��excel������ȡ����
�汾:v1.0
���幦�ܣ�
    1- ��ȡָ��������
    2- �߱�����һЩ��Ч����
ʵ�ַ�����
    1- ��excel�ļ�
    2- ��ȡ��Ӧ����
    3- ��������
���Է�����
    1- ������ѡ���𣬻���һ������ִ��
    2- ����ѡ���Ի�ȡĳЩ��
"""
#---------------�汾����-------------------
"""
�汾��v1.2
����������
    1- �����û�ѡ���κ�������  
        1- �б��  9,11
        2- ����--���ʺϣ�URL ǰ������
    2- ����ɸѡ
        1- ȫ��ִ��   -all
        2- �ֶ�ִ��   tc003-tc007
        3- ���ִ��   tc001,tc007,tc009
        4- ���ϳ���   ['tc001','tc004-tc007','tc009']
"""


class get_excel_data:
    def __init__(self, exceDir, sheetName, caseName,*colName,selectCase=["all"]):  # ��ʼ����������
        """
        :param exceDir: #�ļ�·��
        :param sheetName:  #�����ı���
        :param caseName: #��ȡ����������
        """
        self.excelDir = exceDir
        self.sheetName = sheetName
        self.caseName = caseName
        self.colName = colName
        self.selectCase = selectCase

    def get_exce_data1(self):
        # 1- ����Excel�ļ�
        # formatting_info=True ���ֱ����ʽ����
        workBook = xlrd.open_workbook(self.excelDir, formatting_info=True)
        # 2- �鿴�������Щsheet���ֱ�
        # print(workBook.sheet_names())
        # 3- ��ȡ��Ҫ�����ı��
        worksheet = workBook.sheet_by_name(self.sheetName)
        # 4- Excel����±��0��ʼ
        # print(worksheet.row_values(0)) #��ȡ��0������
        # print(worksheet.col_values(0)) #��ȡ��0������
        # 5- ��ȡĳһ����Ԫ���ڵ�����
        # print(worksheet.cell(1,2).value) #��ȡ��һ�еڶ��е�����

        idex = 0  # ��ʼֵ���У�
        reslist = []  # ��Ž���б�
        for one in worksheet.col_values(0):  # ������0������
            # 1- ɸѡ����:��Ч������/����صĽӿ�����
            if self.caseName in one:
                reqData = worksheet.cell(idex, 1).value  # ��ȡcase�ĵ�1������
                expData = worksheet.cell(idex, 2).value  ##��ȡcase�ĵ�2������
                # ÿһ������ ���������ݣ���Ӧ�������ݣ�
                reslist.append((reqData, expData))
            idex += 1
        return reslist

    def get_excel_data2(self):
        """
        :param excelDir: excel·��
        :param sheetName: �����ı���
        :param caseName: #��ȡ��������
        :return: ����һ��list
        :*args������������
        """
        # 1- ��/����excel�ļ�---
        # formatting_info=True  ����excel��ʽ
        workBook = xlrd.open_workbook(self.excelDir, formatting_info=True)
        # 3- ��ȡ��Ҫ�����ı�
        workSheet = workBook.sheet_by_name(self.sheetName)

        # ---------˼·��ת��------------
        # �������û����������������python�����ȡ��Ӧ�е�����ʹ�õ��б�ţ�
        colIdex = []  # �������±��ţ�
        for i in self.colName:
            # workSheet.row_values(0)--��0������ ��һ���б��б�ͨ��ֵȡ �±� index
            colIdex.append(workSheet.row_values(0).index(i))
        print("�����±�>>>", colIdex)
        # -----------------------------

        idex = 0  # �еĳ�ʼֵ
        resList = []  # ���صĽ����
        for one in workSheet.col_values(0):
            # 1- ɸѡ����:��Ч������/����صĽӿ�����
            if self.caseName in one:
                getColData = []  # �б��ȡ�����������
                for num in colIdex:  # ���������±�
                    res = workSheet.cell(idex, num).value
                    getColData.append(res)  # ������д���б�
                # ÿһ������ ���������ݣ���Ӧ�������ݣ�
                resList.append(getColData)  # resList  �д���б�
            idex += 1  #
        return resList

    def get_excel_data3(self):
        """
        :param excelDir: excel·��
        :param sheetName: �����ı���
        :param caseName: #��ȡ��������
        :return: ����һ��list
        :*args������������
        :selectCase=["all"]
        """
        # 1- ��/����excel�ļ�---
        # formatting_info=True  ����excel��ʽ
        workBook = xlrd.open_workbook(self.excelDir, formatting_info=True)
        # 3- ��ȡ��Ҫ�����ı�
        workSheet = workBook.sheet_by_name(self.sheetName)

        # ---------˼·��ת��------------
        # �������û����������������python�����ȡ��Ӧ�е�����ʹ�õ��б�ţ�
        colIdex = []  # �������±��ţ�
        for i in self.colName:
            # workSheet.row_values(0)--��0������ ��һ���б��б�ͨ��ֵȡ �±� index
            colIdex.append(workSheet.row_values(0).index(i))
        print("�����±�>>>", colIdex)
        # -----------------------------

        # ------ɸѡ����----------------------
        selectList = []
        if self.selectCase[0] == "all":
            # ����ִ�е�0������
            selectList = workSheet.col_values(0)
        else:  # ["001","003-006"]
            for one in self.selectCase:
                if "-" in one:  # �ֶε�����
                    start, end = one.split('-')  # 003   006
                    for i in range(int(start), int(end) + 1):
                        selectList.append(self.caseName + f"{i:0>3}")  # ["Login003","Login004"]
                else:
                    selectList.append(self.caseName + f"{one:0>3}")  # ["Login003","Login004"]
        ## ["Login001","Login003","Login004","Login005","Login006"]
        # --------------------------------

        idex = 0  # �еĳ�ʼֵ
        resList = []  # ���صĽ����
        for one in workSheet.col_values(0):
            # 1- ɸѡ����:��Ч������/����صĽӿ�����
            if self.caseName in one and one in selectList:
                getColData = []  # �б��ȡ�����������
                for num in colIdex:  # ���������±�
                    res = workSheet.cell(idex, num).value
                    getColData.append(res)  # ������д���б�
                # ÿһ������ ���������ݣ���Ӧ�������ݣ�
                resList.append(getColData)  # resList  �д���б�
            idex += 1  #
        return resList

