# -*- coding: utf-8 -*-

import requests,json
import urllib3
urllib3.disable_warnings()

# test
url='https://test.lixiaoskb.com/api_skb/v1/'
headers={
    'app_token': 'f6620ff6729345c8b6101174e695d0ab',
    'Authorization': 'Token token=151a982655945ff073bf5aa0901a1fba',
    'Content-Type': 'application/json;charset=UTF-8',
    'crm_platform_type': 'ikcrm'
}
#
# #stage
# url='https://stage.lixiaoskb.com/api_skb/v1/'
# headers={
#     'app_token': 'f6620ff6729345c8b6101174e695d0ab',
#     'Authorization': 'Token token=7b0bfb297fad8e086b363f0c0722ea93',
#     'Content-Type': 'application/json',
#     'crm_platform_type': 'lixiaoyun'
# }

# # 正式
# url='https://skb.lixiaoskb.com/api_skb/v1/'
# headers={
#     'app_token': 'a14cc8b00f84e64b438af540390531e4',
#     'Authorization': 'Token token=4fcbdb915b01b3e2cc4b805c3bc27408',
#     'Content-Type': 'application/json',
#     'crm_platform_type': 'lixiaoyun'
# }

def conditionGroups():
    path='companyDetail/conditionGroups?groupName=enterprise&category=advancedSearch'
    r=requests.get(url+path,headers=headers,verify=False)
    data=r.json()['data']
    return data


def staticConfig():
    path='companyDetail/staticConfig?namespace=withLevels'
    r=requests.get(url+path,headers=headers,verify=False)
    data=r.json()['data']
    return data

