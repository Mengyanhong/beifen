# -*- coding: utf-8 -*-
# @Time    : 2021/7/22—16:22
# @Author  : 孟艳红
# @File    : 123.py
import requests
url = "http://skb-test.weiwenjia.com/api_skb/v1/shop_search"
headers = {
'Authorization': 'Token token=1ceb18ed4a12c77bdb283ee3e9d0ab98',
'crm_platform_type': 'lixiaoyun'
}
# es_client = Elasticsearch('es-cn-nif1oiv5w0009di0f.public.elasticsearch.aliyuncs.com:9200',
#                       http_auth=('mengyanhong', 'Aa123456'))
# list_shenglen = len(shopDivision["normal"])
# for i in range(list_shenglen):
pr = []
# pr_name = shopDivision["normal"][i]["NAME"]
data = {
    "shopName": "",
    "hasUnfolded": 0,
    "hasSyncClue": 0,
    "page": 1,
    "pagesize": 10,
    "condition": {
        "cn": "composite",
        "cr": "MUST",
        "cv": [{
            "cn": "area",
            "cv": {
                "province": pr,
                "city": [],
                "district": []
            },
            "cr": "IN"
        }, {
            "cn": "category",
            "cv": {
                "categoryL1": ["10"],
                "categoryL2": []
            },
            "cr": "IN"
        }]
    }
}
reponses_pr = requests.post(url, headers=headers, json=data)
# reponses_pr = reponses_pr.json()
print(reponses_pr.request.body)