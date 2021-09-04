# # -*- coding: utf-8 -*-
# # @Time    : 2021/8/6—15:33
# # @Author  : 孟艳红
# # @File    : 1.py
# # import random
# # a = random.randint(0,1-1)
# # print(a)
# #
# #
# import requests,pprint,json,time
# # site_sum = site_config.org_sites_list()
# path='companyDetail/staticConfig?namespace=shopDivision'
# header =  {
#             'app_token': 'f6620ff6729345c8b6101174e695d0ab',
#             'Authorization': f'Token token=5c3bf587deaff969b8ca07627bc40bba',
#             'Content-Type': 'application/json',
#             'crm_platform_type': 'lixiaoyun'
#         }
# url = 'https://test.lixiaoskb.com/api_skb/v1/'
# r=requests.get(url+path,headers=header).json()['data']['shopDivision']
# # a=r['data']['shopDivision']['normal']
# # print(a)
# province_list = []
# city_list = []
# district_list = []
#
# list_shenglen = len(r["normal"])
# for i in range(list_shenglen):
#     province_name = r["normal"][i]["NAME"]
#     province_value = r["normal"][i]["NUM"]
#     province_list.append((province_name,province_value))
#     list_shilen = len(r["normal"][i]["children"])
#     for j in range(list_shilen):
#         city_name = r["normal"][i]["children"][j]["NAME"]
#         city_value = r["normal"][i]["children"][j]["NUM"]
#         city_list.append((city_name,city_value))
#         list_qulen = len(r["normal"][i]["children"][j]["children"])
#         for q in range(list_qulen):
#             district_name = r["normal"][i]["children"][j]["children"][q]["NAME"]
#             district_value = r["normal"][i]["children"][j]["children"][q]["NUM"]
#             district_list.append((district_name,district_value))
# for i in city_list:
#     city_list= i[1]
#     # print(district)
#     url = 'https://skb-test.weiwenjia.com/api_skb/v1/shop_search'
#     Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
#                                "condition": {"cn": "composite", "cr": "MUST", "cv": [
#                                    {"cn": "area", "cv": {"province": [], "city": [city_list], "district": []}, "cr": "IN"}]}}
#     response = requests.post(url, headers=header, json=Request_payload).json()
#     time.sleep(2.5)
#     print('\r',i[0],end='')
#     assert response['error_code'] == 0
#
# # for i in range(len(r['r'])):
# #     category_list.append((r['r'][i]['name'],r['r'][i]['value']))
# #     for j in range(len(r['r'][i]['sub'])):
# #         category2_list.append((r['r'][i]['sub'][j]['name'],r['r'][i]['sub'][j]['value']))
# #
# # print(r.json())
import pytest
