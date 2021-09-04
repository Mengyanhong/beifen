# -*- coding: utf-8 -*-
# import openpyxl
# from skb_project.adv_search.config_API import staticConfig
# import urllib3
# urllib3.disable_warnings()
#
# staticConfig=staticConfig()['tradeMarkInventoryCategory']
# level1_num_api=len(staticConfig)
#
# file='二级选项.xlsx'
# data=openpyxl.load_workbook(file)
# sheet_last=data['商标商品服务']
#
# # a=sheet_last['J2'].value
# # print(a[-1])
#
# for i in range(2,518):
#     a=sheet_last['J'+str(i)].value
#     sheet_last['J'+str(i)].value=a.rstrip()
# data.save(file)
import yaml,pytest,time,requests,random, datetime
from adv_search.search_API import headers
from elasticsearch import Elasticsearch

from adv_search.conftest import ES

with open('multiSelect.yaml') as f:
    yaml_data = yaml.safe_load(f)
    f.close()
# print(yaml_data)
# key = list(yaml_data.keys())
# keys = yaml_data[key]
# yaml_data_list = []
# yaml_data_list.append({'key':key,'keys':keys})

# key_list = list(yaml_data.keys())
# data_list = yaml_data[key_list[0]]
from adv_search.search_API import search_API
#
data = search_API('techTypeCompany', [10], 'IN')
# print(len(data['items'])-1)
# print(data['items'])
pid = data['items'][1]['id']
# print(pid)

# a = [random.randint(0, len(data['items'])-1) for i in range(20)]
# print(a)
# key_list_SearchCondition = list(yaml_data.keys())
# data_list = []
# for i in range(len(key_list_SearchCondition)):
#         if key_list_SearchCondition[i] == "SearchCondition_techTypeCompany":
#             for label_value in yaml_data[key_list_SearchCondition[i]]["cv"]["options"]:
#                 data_list.append((yaml_data[key_list_SearchCondition[i]]["name"], label_value["value"], label_value["label"],key_list_SearchCondition[i]))
#         else:
#             for value in yaml_data[key_list_SearchCondition[i]]:
#                 data_list.append((key_list_SearchCondition[i],value,None,None))
# print(data_list)
# for i in a:
#     print(i%2)
#     print(isinstance(i/2, int))

# @pytest.mark.parametrize('level1',pid)
# def test_firstCategory(level1,ES):
#     print(level1)
es_client = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200', #最新地址
                              http_auth=('mengyanhong', 'Aa123456'))
es_result = es_client.get(index="company_info_prod", id=pid)['_source']
print(es_result)
#
# print(datetime.date.today())
# currentDate = datetime.date.today()  # 当前日期
# current_day = currentDate.day
# current_month = currentDate.month
# current_year = currentDate.year
# print(currentDate)
from dateutil.parser import parse


start = '2024-02-03T08:00:00.000+0800'
# start = start.split('+')[0]
# current =  datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f')
# timeStamp = int(time.mktime(current.timetuple())*1000)
# print(timeStamp)

if str(type(start)) == "<class 'str'>":
    print(str(type(start)))
# print(int(timeStamp*1000))
# print(current_month)
