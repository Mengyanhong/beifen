# -*- coding: utf-8 -*-
#二级选项搜索
import pytest,openpyxl,time
from adv_search.search_API import search_API

class TestTwoCategory():
    def setup(self):
        file = openpyxl.load_workbook('二级选项.xlsx')

        #取出行业列表
        sheet = file['行业']
        self.firstIndustry_list = []
        for i in range(4, 120):
            if (sheet['A' + str(i)]).value != None:
                self.firstIndustry_list.append(sheet['A' + str(i)].value)
        self.secondIndustry_list = []
        for i in range(4, 120):
            if (sheet['C' + str(i)]).value != None:
                self.secondIndustry_list.append(str(sheet['C' + str(i)].value))

        # 取出运营节点列表
        sheet = file['运营节点']
        self.serviceNodeL1_list = []
        for i in range(3, 81):
            if (sheet['C' + str(i)]).value != None:
                self.serviceNodeL1_list.append(sheet['C' + str(i)].value)
        self.serviceNodeL2_list = []
        for i in range(3, 81):
            if (sheet['E' + str(i)]).value != None:
                self.serviceNodeL2_list.append(sheet['E' + str(i)].value)

        # 取出运营节点列表
        sheet = file['海关登记行业']
        self.cusIndusCategoryL1_list = []
        for i in range(3, 84):
            if (sheet['C' + str(i)]).value != None:
                self.cusIndusCategoryL1_list.append(sheet['C' + str(i)].value)
        self.cusIndusCategoryL2_list = []
        for i in range(3, 84):
            if (sheet['E' + str(i)]).value != None:
                self.cusIndusCategoryL2_list.append(sheet['E' + str(i)].value)

        # 取出商标商品服务列表
        sheet = file['商标商品服务']
        self.inventoryL1_list = []
        for i in range(3, 563):
            if (sheet['C' + str(i)]).value != None:
                self.inventoryL1_list.append(sheet['C' + str(i)].value)
        self.inventoryL2_list = []
        for i in range(3, 563):
            if (sheet['E' + str(i)]).value != None:
                self.inventoryL2_list.append(sheet['E' + str(i)].value)

        # sheet = file['涵盖证书类型']
        # self.certL1Type_list = []
        # for i in range(3, 84):
        #     if (sheet['C' + str(i)]).value != None:
        #         self.certL1Type_list.append(sheet['C' + str(i)].value)
        # self.certL2Type_list = []
        # for i in range(3, 84):
        #     if (sheet['E' + str(i)]).value != None:
        #         self.certL2Type_list.append(sheet['E' + str(i)].value)

    # @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    # @pytest.mark.parametrize(['category','level1','level2'],
    #                          [['industry','firstIndustry','secondIndustry'],['serviceNode','serviceNodeL1','serviceNodeL2'],
    #                          ['cusIndusCategory','cusIndusCategoryL1','cusIndusCategoryL2'],
    #                           ['tradeMarkInventoryCategory','inventoryL1','inventoryL2'],
    #                           ['certType','certL1Type','certL2Type']])
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize(['category','level1','level2'],
                              [['tradeMarkInventoryCategory','inventoryL1','inventoryL2']])
    def test_firstCategory(self,cr,category,level1,level2,ES):
        es_client=ES

        first_list=[]   #选择对应的选项列表
        esCheck_field=''  #行业es上分1级2级两个字段，其他暂时不分
        if category=='industry':
            first_list=self.firstIndustry_list
            esCheck_field = level1
        elif category=='serviceNode':
            first_list=self.serviceNodeL1_list
            esCheck_field=category
        elif category=='cusIndusCategory':
            first_list = self.cusIndusCategoryL1_list
            esCheck_field = category
        elif category=='tradeMarkInventoryCategory':
            first_list = self.inventoryL1_list
            esCheck_field = category
        # elif category=='certType':
        #     first_list = self.certL1Type_list
        #     esCheck_field = category

        for code in first_list:
            # print('level1', code)
            time.sleep(3)
            data = search_API(category, {level1: [f"{code}"], level2: []},cr)
            if len(data['items']) == 0:
                print('level1', code)
            # assert len(data['items']) != 0
            # print(data)

            for i in range(len(data['items'])):
                pid = data['items'][i]['id']
                companyName = data['items'][i]['companyName']
                # print(pid)
                # print(companyName)

                # 和ES对比
                es_result=es_client.get(index="company_info_prod", id=pid)['_source']
                # 返回es中所有的键，去除 无该字段时的报错
                if cr=='IN':
                    assert code in es_result[esCheck_field]
                else:
                    if esCheck_field not in list(es_result.keys()):
                        pass
                    else:
                        assert code not in es_result[esCheck_field]

    # @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    # @pytest.mark.parametrize(['category','level1','level2'],
    #                          [['industry','firstIndustry','secondIndustry'],['serviceNode','serviceNodeL1','serviceNodeL2'],
    #                          ['cusIndusCategory','cusIndusCategoryL1','cusIndusCategoryL2'],
    #                           ['tradeMarkInventoryCategory','inventoryL1','inventoryL2']])
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize(['category','level1','level2'],
                              [['tradeMarkInventoryCategory','inventoryL1','inventoryL2']])
    def test_secondCategory(self,cr,category,level1,level2,ES):
        es_client = ES

        second_list=[]   #选择对应的选项列表
        esCheck_field=''  #行业es上分1级2级两个字段，其他暂时不分
        if category=='industry':
            second_list=self.secondIndustry_list
            esCheck_field = level2
        elif category=='serviceNode':
            second_list=self.serviceNodeL2_list
            esCheck_field=category
        elif category=='cusIndusCategory':
            second_list = self.cusIndusCategoryL2_list
            esCheck_field = category
        elif category=='tradeMarkInventoryCategory':
            second_list = self.inventoryL2_list
            esCheck_field = category

        for code in second_list:
            # print('level2', code)
            time.sleep(3)
            data = search_API(category, {level1: [], level2: [f"{code}"]},cr)
            if len(data['items']) == 0:
                print('level2', code)
            # assert len(data['items']) != 0
            # print(data)

            for i in range(len(data['items'])):
                pid = data['items'][i]['id']
                companyName = data['items'][i]['companyName']
                # print(pid)
                # print(companyName)

                # 和ES对比
                es_result=es_client.get(index="company_info_prod", id=pid)['_source']
                # 返回es中所有的键，去除 无该字段时的报错
                if cr=='IN':
                    assert code in es_result[esCheck_field]
                else:
                    if esCheck_field not in list(es_result.keys()):
                        pass
                    else:
                        assert code not in es_result[esCheck_field]
