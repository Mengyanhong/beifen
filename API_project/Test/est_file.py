# -*- coding: utf-8 -*-
# @Time : 2021/9/9 11:31
# @Author : 孟艳红
# @File : est_file.py
from pprint import pprint
import json,requests

# a = 3931
# b = 3210
# true = True
# false = False
# ah = {"keyword":"上海","filter":{"location":[],"industryshort":[],"secindustryshort":[],"registercapital":[],"establishment":[],"entstatus":[],"contact":[],"sortBy":"0","companysource":[],"enttype":[0],"employees":[0],"hasrecruit":"0","hassem":"0","haswebsite":"0","hastrademark":"0","haspatent":"0","hastender":"0","haswechataccnt":"0","filterUnfold":2,"filterSync":0,"filterSyncRobot":0,"hasBuildingCert":"0","isHighTech":"0","hasFinanceInfo":"0","hasAbnormalInfo":"0","syncRobotRangeDate":[]},"scope":"companyname","matchType":"most_fields","pids":["0bccbb2dc4ebbc8dbb52faf31ffc6f89","dcb8e2f6a5ddbaa6e2534039dc8b5977","b49df16f3e78f258377b3739655d753f","dd964881127e76cefa33c392da1bc34c","66c79e55756e3ede30a06d816b1093e9","f090c31eaac628c910ee4a694b1eb469","8078bbf1aeabae967c88820b66389081","b1e635e244dd15f810cef27e9aad601d","a8944aa2ade62044eb308c0907361c9d","e95a99ea157f225f8224639986c179c8"],"way":"search_list","from":"syncRobot","useQuota":true,"dataColumns":[0,1],"phoneStatus":[0,1,2,3],"numberCount":1,"canCover":false,"needCallPlan":false,"origin":"https://lxcrm.weiwenjia.com"}
# pprint(ah)

# data = {'key1': True}
# data_json = json.dumps(data)
# data_jso = json.loads(data_json)
# print(data_jso)
true=True
false=False
url = 'https://skb-test.weiwenjia.com/api_skb/v1/shopClues/sync_robot'
pla = {"shopName": "", "hasUnfolded": 2, "hasSyncClue": 1, "hasSyncRobot": 1, "syncRobotRangeDate": [],
        "condition": {"cn": "composite", "cr": "MUST",
                      "cv": [{"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": []}, "cr": "IN"}]},
        "pids": ["5422602", "77916263"], "way": "shop_search_list", "useQuota": true, "dataColumns": [0, 1],
        "phoneStatus": [0, 1, 2, 3], "numberCount": 0, "canCover": false, "needCallPlan": false,
        }
ha={
            'app_token': 'f6620ff6729345c8b6101174e695d0ab',
            'Authorization': 'Token token=b792810fccc3ab092d476927049d4643',
            'Content-Type': 'application/json',
            'crm_platform_type': 'ikcrm'
        }
po = requests.post(url,headers=ha,json=pla)
print(po.json())