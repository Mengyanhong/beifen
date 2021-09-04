# -*- coding: utf-8 -*-
import pytest,openpyxl,time
from search_API import search_API

file=openpyxl.load_workbook('地区.xlsx')
sheet=file['地区']

class TestDistrict():
    @pytest.mark.parametrize('cr',['IN','NOT_IN'])
    def test_province(self,cr,ES):
        es_client = ES
        for i in range(2,33):
            code=sheet['B'+str(i)].value
            time.sleep(3)
            data = search_API('area', {"province": [f"{code}"], "city": [], "district": []},cr)
            assert len(data['items']) != 0
            print(code)
            print(data)

            for j in range(len(data['items'])):
                pid = data['items'][j]['id']
                companyName = data['items'][j]['companyName']
                print(pid)
                print(companyName)

                # 和ES对比
                es_result=es_client.get(index="company_info_prod", id=pid)['_source']
                # 返回es中所有的键，去除 无该字段时的报错
                if cr=='IN':
                    assert es_result['province']==int(code)
                else:
                    assert es_result['province']!=int(code)

    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    def test_city(self,cr,ES):
        es_client = ES
        for i in range(2,369):
            code=sheet['D'+str(i)].value
            time.sleep(3)
            data = search_API('area', {"province": [], "city": [f"{code}"], "district": []},cr)
            assert len(data['items']) != 0
            print(code)
            print(data)

            for j in range(len(data['items'])):
                pid = data['items'][j]['id']
                companyName = data['items'][j]['companyName']
                print(pid)
                print(companyName)

                # 和ES对比
                es_result=es_client.get(index="company_info_prod", id=pid)['_source']
                # 返回es中所有的键，去除 无该字段时的报错
                if cr == 'IN':
                    assert es_result['city']==int(code)
                else:
                    assert es_result['city']!=int(code)

    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    def test_district(self,cr,ES):
        es_client = ES
        for i in range(2,2815):
            code=sheet['F'+str(i)].value
            print(code)
            data = search_API('area', {"province": [], "city": [], "district": [f"{code}"]},cr)
            print(data)
            assert len(data['items'])!=0

            for j in range(len(data['items'])):
                pid = data['items'][j]['id']
                companyName = data['items'][j]['companyName']
                print(pid)
                print(companyName)

                # 和ES对比
                es_result=es_client.get(index="company_info_prod", id=pid)['_source']
                # 返回es中所有的键，去除 无该字段时的报错
                if cr == 'IN':
                    assert es_result['district']==int(code)
                else:
                    assert es_result['district']!=int(code)