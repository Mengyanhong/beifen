import requests
import json

sum = 0
for i in range(10):
    if i<3:
        print(1)
    else:
        sum+=1
        if sum>2:
            print(sum)
            break


def test_sync():
    url = "https://skb-test.weiwenjia.com/api_skb/v1/clues/sync"
    headers = {
        "Authorization": "Token token=c226f5c5b96665b6aae7ec832e997408",
        "crm_platform_type": "lixiaoyun"
    }
    JSON = {
        "keyword": "信息",
        "filter":
            {
                "location": [],
                "industryshort": [],
                "secindustryshort": [],
                "registercapital": [],
                "establishment": [],
                "entstatus": [],
                "contact": [],
                "sortBy": "0",
                "companysource": [],
                "enttype": [0],
                "employees": [0],
                "hasrecruit": "0",
                "hassem": "0",
                "haswebsite": "0",
                "hastrademark": "0",
                "haspatent": "0",
                "hastender": "0",
                "haswechataccnt": "0",
                "filterUnfold": 0,
                "filterSync": 0,
                "filterSyncRobot": 0,
                "hasBuildingCert": "0",
                "isHighTech": "0",
                "hasFinanceInfo": "0",
                "hasAbnormalInfo": "0"
            },
        "scope": "companyname",
        "pids": ["6b1d2d90b5242bb4dec58e132fbf56e1", "f60198db0221951cfc0902672613944e"],
        "way": "search_list",
        "from": "syncClue",
        "useQuota": True
    }
    r = requests.post(url=url, json=JSON, headers=headers)
    print(r.text)

import requests
def test_search():
    url = "http://skb-test.weiwenjia.com/api_skb/v1/search"
    headers = {
        "Host": "skb-test.weiwenjia.com",
        "app_token": "f6620ff6729345c8b6101174e695d0ab",
        "Authorization": "Token token=c226f5c5b96665b6aae7ec832e997408",
        "Content-Type": "application/json;charset=UTF-8",
        "crm_platform_type": "lixiaoyun",
        "platform_type": "PC"
    }
    json_data = {
        "keyword": "上海",
        "filter": {
            "location": [],
            "industryshort": [],
            "secindustryshort": [],
            "registercapital": [],
            "establishment": [],
            "entstatus": [],
            "contact": [],
            "sortBy": "0",
            "companysource": [],
            "enttype": [0],
            "employees": [0],
            "hasrecruit": "0",
            "hassem": "0",
            "haswebsite": "0",
            "hastrademark": "0",
            "haspatent": "0",
            "hastender": "0",
            "haswechataccnt": "0",
            "filterUnfold": 0,
            "filterSync": 1,
            "filterSyncRobot": 1,
            "hasBuildingCert": "0",
            "isHighTech": "0",
            "hasFinanceInfo": "0",
            "hasAbnormalInfo": "0"
        },
        "scope": "companyname",
        "pagesize": 10,
        "page": 1
    }
    response = requests.post("http://skb-test.weiwenjia.com/api_skb/v1/search", json=json_data, headers=headers,verify=False)
    print(response.json())


# if __name__ == "__main__":
#     test_search()
# -*- coding: utf-8 -*-

# import requests
#
#
# class HttpsClient:
#
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def get(_url, _json):
#         _resp = requests.get(_url, _json)
#         return _resp.content
#
#     @staticmethod
#     def https_post(_url, _json_dict):
#         _resp = requests.post(_url, _json_dict, verify=False)
#         return _resp.text
#
#     @staticmethod
#     def https_post_with_header(_url, _json_dict, _headers):
#         _resp = requests.post(_url, data=_json_dict, headers=_headers, verify=False)
#         return _resp.text
#
#
# if __name__ == '__main__':
#     url = "http://www.baidu.com"
#     json_dict = '{}'
#     result = HttpsClient.https_post(url, json_dict)
#     print(result)