# -*- coding: utf-8 -*-
# @Time : 2021/9/9 11:31
# @Author : 孟艳红
# @File : est_file.py
import datetime
from pprint import pprint
import json, requests

import random
# a = 3931
print(random.randint(0,9))
a=[]
a.append(111)
print(a)
import re
load1='仰天大笑出门去,我辈岂是蓬蒿人'
print(re.findall('门(.*?)岂',load1))



# b = 3210
# true = True
# false = False
# ah = {"keyword":"上海","filter":{"location":[],"industryshort":[],"secindustryshort":[],"registercapital":[],"establishment":[],"entstatus":[],"contact":[],"sortBy":"0","companysource":[],"enttype":[0],"employees":[0],"hasrecruit":"0","hassem":"0","haswebsite":"0","hastrademark":"0","haspatent":"0","hastender":"0","haswechataccnt":"0","filterUnfold":2,"filterSync":0,"filterSyncRobot":0,"hasBuildingCert":"0","isHighTech":"0","hasFinanceInfo":"0","hasAbnormalInfo":"0","syncRobotRangeDate":[]},"scope":"companyname","matchType":"most_fields","pids":["0bccbb2dc4ebbc8dbb52faf31ffc6f89","dcb8e2f6a5ddbaa6e2534039dc8b5977","b49df16f3e78f258377b3739655d753f","dd964881127e76cefa33c392da1bc34c","66c79e55756e3ede30a06d816b1093e9","f090c31eaac628c910ee4a694b1eb469","8078bbf1aeabae967c88820b66389081","b1e635e244dd15f810cef27e9aad601d","a8944aa2ade62044eb308c0907361c9d","e95a99ea157f225f8224639986c179c8"],"way":"search_list","from":"syncRobot","useQuota":true,"dataColumns":[0,1],"phoneStatus":[0,1,2,3],"numberCount":1,"canCover":false,"needCallPlan":false,"origin":"https://lxcrm.weiwenjia.com"}
# pprint(ah)

# data = {'key1': True}
# data_json = json.dumps(data)
# data_jso = json.loads(data_json)
# print(data_jso)
# true=True
# false=False
# url = 'https://skb-test.weiwenjia.com/api_skb/v1/shopClues/sync_robot'
# pla = {"shopName": "", "hasUnfolded": 2, "hasSyncClue": 1, "hasSyncRobot": 1, "syncRobotRangeDate": [],
#         "condition": {"cn": "composite", "cr": "MUST",
#                       "cv": [{"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": []}, "cr": "IN"}]},
#         "pids": ["5422602", "77916263"], "way": "shop_search_list", "useQuota": true, "dataColumns": [0, 1],
#         "phoneStatus": [0, 1, 2, 3], "numberCount": 0, "canCover": false, "needCallPlan": false,
#         }
# ha={
#             'app_token': 'f6620ff6729345c8b6101174e695d0ab',
#             'Authorization': 'Token token=b792810fccc3ab092d476927049d4643',
#             'Content-Type': 'application/json',
#             'crm_platform_type': 'ikcrm'
#         }
# po = requests.post(url,headers=ha,json=pla)
# print(po.json())
# import time
# print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
print(datetime.datetime(2021, 9, 17, 00, 00, 00))
import uuid

# data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 3, 5, 6, 7, 8, 9, 6, 5, 4, 3, 8, 9]
# # batch_step = round(len(data) / 10)
# # print(batch_step)
# for index in range(0, len(data), 5):
#     item_list = data[index:index + 5]
#     print(item_list)
#     # print(2000000/2000)
# import random
#
# print(str(random.randint(10,100)))
# example
# from pymongo import MongoClient
#
# mdb = MongoClient('120.133.26.xxx:20002', username='xt', password='xxxxxx')
# image_ids = ["001", "002", "003", ...]
#
# image_dict = {}
# batch_step = round(len(image_ids) / 10)
# for idx in range(0, len(image_ids), batch_step):
#     image_ids_part = image_ids[idx:idx + batch_step]
#     image_infos = mdb['数据库名']['图片表名'].find({"image_id": {"$in": image_ids_part}})
#
#     image_one = {}
#     for image_info in image_infos:
#         if image_info.get("image_size"):
#             image_one[image_info.get("image_id")] = image_info
#             image_dict.update(image_one)
