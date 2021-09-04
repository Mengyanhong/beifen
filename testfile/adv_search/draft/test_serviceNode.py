# -*- coding: utf-8 -*-
import pytest,openpyxl
from skb_project.adv_search.search_API import search_API

file=openpyxl.load_workbook('运营节点.xlsx')
sheet=file['运营节点']
serviceNodeL1_list = []
for i in range(3,81):
    if (sheet['C'+str(i)]).value!=None:
        serviceNodeL1_list.append(sheet['C'+str(i)].value)

serviceNodeL2_list = []
for i in range(3,81):
    if (sheet['E'+str(i)]).value!=None:
        serviceNodeL2_list.append(sheet['E'+str(i)].value)

class TestserviceNode():
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    def test_serviceNodeL1(self,cr,ES):
        es_client=ES
        for code in serviceNodeL1_list:
            data = search_API('serviceNode', {"serviceNodeL1": [f"{code}"], "serviceNodeL2": []},cr)
            # print(code)
            if len(data['items'])== 0:
                print('错误','serviceNode', {"serviceNodeL1": [f"{code}"], "serviceNodeL2": []},cr)
            # assert len(data['items']) != 0
            else:
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
                        if code not in es_result['serviceNode']:
                            print(f'{code}--{pid}--错误')
                        # assert code in es_result['serviceNode']
                    else:
                        if 'serviceNode' not in list(es_result.keys()):
                            pass
                        else:
                            if code in es_result['serviceNode']:
                                print(f'{code}--{pid}--错误')
                            # assert code not in es_result['serviceNode']

    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    def test_serviceNodeL2(self,cr,ES):
        es_client = ES
        for code in serviceNodeL2_list:
            data = search_API('serviceNode', {"serviceNodeL1": [], "serviceNodeL2": [f"{code}"]},cr)
            if len(data['items'])== 0:
                print('错误','serviceNode', {"serviceNodeL1": [], "serviceNodeL2": [f"{code}"]},cr)
            else:
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
                        if code not in es_result['serviceNode']:
                            print(f'{code}--{pid}--错误')
                        # assert code in es_result['serviceNode']
                    else:
                        if 'serviceNode' not in list(es_result.keys()):
                            pass
                        else:
                            if code in es_result['serviceNode']:
                                print(f'{code}--{pid}--错误')
                            # assert code not in es_result['serviceNode']
