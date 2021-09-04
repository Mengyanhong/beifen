# -*- coding: utf-8 -*-
import pytest,openpyxl
from search_API import search_API

file=openpyxl.load_workbook('行业.xlsx')
sheet=file['行业']
firstIndustry_list = []
for i in range(4,120):
    if (sheet['A'+str(i)]).value!=None:
        firstIndustry_list.append(sheet['A'+str(i)].value)

secondIndustry_list = []
for i in range(4,120):
    if (sheet['C'+str(i)]).value!=None:
        secondIndustry_list.append(str(sheet['C'+str(i)].value))

class TestIndustry():
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    def test_firstIndustry(self,cr,ES):
        es_client=ES
        for code in firstIndustry_list:
            data = search_API('industry', {"firstIndustry": [f"{code}"], "secondIndustry": []},cr)
            print(code)
            assert len(data['items']) != 0
            print(data)

            for i in range(len(data['items'])):
                pid = data['items'][i]['id']
                companyName = data['items'][i]['companyName']
                print(pid)
                print(companyName)

                # 和ES对比
                es_result=es_client.get(index="company_info_prod", id=pid)['_source']
                # 返回es中所有的键，去除 无该字段时的报错
                if cr=='IN':
                    assert code in es_result['firstIndustry']
                else:
                    assert code not in es_result['firstIndustry']

    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    def test_secondIndustry(self,cr,ES):
        es_client = ES
        for code in secondIndustry_list:
            print({"firstIndustry": [], "secondIndustry": [f"{code}"]})
            data = search_API('industry', {"firstIndustry": [], "secondIndustry": [f"{code}"]},cr)
            assert len(data['items']) != 0
            print(data)

            for i in range(len(data['items'])):
                pid = data['items'][i]['id']
                companyName = data['items'][i]['companyName']
                print(pid)
                print(companyName)

                # 和ES对比
                es_result=es_client.get(index="company_info_prod", id=pid)['_source']
                # 返回es中所有的键，去除 无该字段时的报错
                if cr=='IN':
                    assert code in es_result['secondIndustry']
                else:
                    assert code not in es_result['secondIndustry']
