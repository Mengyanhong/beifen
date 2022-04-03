# -*- coding: utf-8 -*-
# @Time : 2021/9/9 11:31
# @Author : 孟艳红
# @File : est_file.py
import datetime
from pprint import pprint
import json, requests

import random

# a = 3931
print(random.randint(0, 9))
a = []
a.append(111)
print(a)
import re

load1 = '仰天大笑出门去,我辈岂是蓬蒿人'
print(re.findall('门(.*?)岂', load1))

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

true = True
false = False
searchCondition = {"condition": {"cn": "composite", "cr": "MUST", "cv": [
    {"id": "b3a619a5-6025-4e2e-881a-8aff9aa58199", "cn": "hasMobile", "cr": "IS", "cv": true},
    {"id": "07908e74-4385-4c0f-8931-5a93d4877105", "cn": "entStatus", "cr": "IN", "cv": ["1"]},
    {"id": "95783391-3ef9-4a6a-a275-9623b4f82c2c", "cn": "hasArchitCert", "cr": "IS", "cv": false},
    {"id": "6a9e5183-3a7b-4fd4-ac99-d7810913bd03", "cn": "composite", "cr": "SHOULD",
     "cv": [{"id": "d1e304a5-6ce6-4596-8505-6f562c6df127", "cn": "entName", "cr": "IN", "cv": ["工程", "建筑"]},
            {"id": "b7a1c0b7-45cf-4f18-8ea7-4f29d1f2b5ed", "cn": "latest6MonthJobName", "cr": "IN",
             "cv": ["造价工程师", "土木工程师", "造价师"]},
            {"id": "2921423c-6e52-4528-900b-8391a56d709e", "cn": "opScope", "cr": "IN", "cv": ["建筑工程", "工程施工"]}]},
    {"id": "ccc7329a-af1a-4673-825c-2899e541dfe2", "cn": "entName", "cr": "NOT_IN", "cv": ["咨询", "企业服务"]},
    {"id": "b0662720-e465-4524-8169-5b30eb5907e2", "cn": "opScope", "cr": "NOT_IN", "cv": ["证书办理", "企业服务", "知识产权代办"]}]},
                   "hasSyncClue": 0, "hasSyncRobot": 0, "hasUnfolded": 0, "sortBy": 0, "syncRobotRangeDate": [],
                   "pids": ["4de38efd3817855255fa67bb9b0bbf10", "a13c4068efc840143dd07d0b144025ee",
                            "6578b4bd7b259196713ed2d903995dd5", "b7cf3aa16de9402eda5c2388f86d4e74",
                            "05c2c3b42689f6845107e360709da74b", "061efb32877a80a403bf800d32aca743",
                            "bc71c054c9c2d1b0d7804319473477d2", "9285cc549df5a9e8f51d375d7ddfd224",
                            "dd77be1bd19a7c46edf58298ed4829c8", "3a1b387a212a7bf88da4f109c427da19"],
                   "way": "advanced_search_list", "templateType": 1, "templateName": "新办业务", "userClick": 0,
                   "from": "syncRobot", "useQuota": true, "dataColumns": [0, 1], "phoneStatus": [0, 1, 2, 3],
                   "numberCount": 0, "canCover": false, "needCallPlan": false, "origin": "https://ik-staging.ikcrm.com"}
print(set(searchCondition))

searchConditions ="{\"canCover\":false,\"commonCondition\":false,\"condition\":{\"cn\":\"composite\",\"cr\":\"MUST\",\"cv\":[{\"cn\":\"hasMobile\",\"cr\":\"IS\",\"cv\":true},{\"cn\":\"entStatus\",\"cr\":\"IN\",\"cv\":[\"1\"]},{\"cn\":\"hasArchitCert\",\"cr\":\"IS\",\"cv\":false},{\"cn\":\"composite\",\"cr\":\"SHOULD\",\"cv\":[{\"cn\":\"entName\",\"cr\":\"IN\",\"cv\":[\"工程\",\"建筑\"]},{\"cn\":\"latest6MonthJobName\",\"cr\":\"IN\",\"cv\":[\"造价工程师\",\"土木工程师\",\"造价师\"]},{\"cn\":\"opScope\",\"cr\":\"IN\",\"cv\":[\"建筑工程\",\"工程施工\"]}]},{\"cn\":\"entName\",\"cr\":\"NOT_IN\",\"cv\":[\"咨询\",\"企业服务\"]},{\"cn\":\"opScope\",\"cr\":\"NOT_IN\",\"cv\":[\"证书办理\",\"企业服务\",\"知识产权代办\"]}]},\"contact\":\"\",\"dataColumns\":[0,1],\"delNoContact\":0,\"distinctUniq\":true,\"dropdown\":0,\"enableDeepSearch\":0,\"extraReturnFields\":[],\"filter\":{\"filterSync\":1,\"filterSyncRobot\":0,\"filterUnfold\":0},\"from\":\"syncRobot\",\"fromSync\":false,\"hasSyncClue\":\"ALL\",\"hasSyncRobot\":\"ALL\",\"hasUnfolded\":\"ALL\",\"isSimpleHead\":false,\"keyword\":\"\",\"modified\":false,\"needCallPlan\":false,\"note\":\"\",\"numberCount\":0,\"origin\":\"https://ik-staging.ikcrm.com\",\"page\":1,\"pagesize\":10,\"phoneStatus\":[\"0\",\"1\",\"2\",\"3\"],\"pidListHasCondition\":false,\"pids\":[\"4de38efd3817855255fa67bb9b0bbf10\",\"a13c4068efc840143dd07d0b144025ee\",\"6578b4bd7b259196713ed2d903995dd5\",\"b7cf3aa16de9402eda5c2388f86d4e74\",\"05c2c3b42689f6845107e360709da74b\",\"061efb32877a80a403bf800d32aca743\",\"bc71c054c9c2d1b0d7804319473477d2\",\"9285cc549df5a9e8f51d375d7ddfd224\",\"dd77be1bd19a7c46edf58298ed4829c8\",\"3a1b387a212a7bf88da4f109c427da19\"],\"scope\":\"\",\"searchBusiness\":\"advancedSearch\",\"searchObj\":\"enterprise\",\"searchType\":0,\"sortBy\":\"DEFAULT\",\"source\":\"\",\"start\":-1,\"syncRobotRangeDate\":[],\"templateName\":\"新办业务\",\"templateType\":\"SYSTEM\",\"useQuota\":true,\"userClick\":0,\"userClicked\":false,\"verify\":0,\"way\":\"advanced_search_list\"}"
print(set(searchCondition).intersection(set(json.loads(searchConditions))))
# print(json.loads(searchConditions).items())
# print(json.loads(searchConditions)["condition"])
# print(json.loads(searchConditions).keys())
if searchCondition == searchConditions:
    print(1)
