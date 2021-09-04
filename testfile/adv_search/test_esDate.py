# -*- coding: utf-8 -*-
import pytest,time,datetime
from dateutil.relativedelta import relativedelta
from adv_search.search_API import search_API
#成立时间快捷选择区间
#成立时间 时间区间的case 在 test_search_date.py 中

current_time=int(time.time()*1000)
now=datetime.datetime.now().date()
one_year=int(time.mktime(time.strptime((now-relativedelta(years=1)).strftime("%Y-%m-%d"),"%Y-%m-%d"))*1000)
five_year=int(time.mktime(time.strptime((now-relativedelta(years=5)).strftime("%Y-%m-%d"),"%Y-%m-%d"))*1000)
ten_year=int(time.mktime(time.strptime((now-relativedelta(years=10)).strftime("%Y-%m-%d"),"%Y-%m-%d"))*1000)
fifteen_year=int(time.mktime(time.strptime((now-relativedelta(years=15)).strftime("%Y-%m-%d"),"%Y-%m-%d"))*1000)

value_dict={'1':[one_year,current_time],'2':[five_year,one_year],'3':[ten_year,five_year],'4':[fifteen_year,ten_year],'5':['',fifteen_year]}
value_list=[]
for value_dict_key in value_dict.keys():
    value_list.append(value_dict_key)

class TestSearchesDate():
    @pytest.mark.parametrize('value',value_list)
    def test_search_esDate(self,value,ES):
        es_client = ES
        data = search_API('esDate', value, 'IN')
        print('esDate', value)
        assert len(data['items']) != 0
        print(data)

        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 在ES中确认
            es_result=es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错
            es_key_list = []
            for es_key in es_result.keys():
                es_key_list.append(es_key)

            if 'esDate' not in es_key_list:
                assert True == False  # 这是个必错的情况
            else:
                assert es_result['esDate'] <= value_dict[value][1]

                if value=='5':#15年以上没有向上的判断
                    pass
                else:
                    assert es_result['esDate'] >= value_dict[value][0]


