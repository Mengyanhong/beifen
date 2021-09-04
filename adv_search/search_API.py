# -*- coding: utf-8 -*-

import requests, json
import urllib3

urllib3.disable_warnings()

# # test
# url='https://skb-test.weiwenjia.com/api_skb/v1/advanced_search'
# headers={
#     'app_token': 'f6620ff6729345c8b6101174e695d0ab',
#     'Authorization': 'Token token=42f0ce329bd6d4ed7ca5be881ead6a60',
#     'Content-Type': 'application/json;charset=UTF-8',
#     'crm_platform_type': 'lixiaoyun'
# }

# stage
# url='https://skb-staging.weiwenjia.com/api_skb/v1/advanced_search'
# headers={
#     'app_token': 'f6620ff6729345c8b6101174e695d0ab',
#     'Authorization': 'Token token=7b0bfb297fad8e086b363f0c0722ea93',
#     'Content-Type': 'application/json',
#     'crm_platform_type': 'lixiaoyun'
# }

# 正式
url = 'https://skb.weiwenjia.com/api_skb/v1/advanced_search'
headers = {
    'app_token': 'a14cc8b00f84e64b438af540390531e4',
    'Authorization': 'Token token=18033bf7b969d9b12ef830c66c1f2464',
    'Content-Type': 'application/json',
    'crm_platform_type': 'lixiaoyun'
}


def search_API(cn, cr, cv):
    body = {
        # "isCustomerTemplate": 1,
        "condition": {
            "cn": "composite",
            "cr": "MUST",
            "cv": [
                {
                    "cn": cn,
                    "cr": cr,
                    "cv": cv
                }
            ]
        },
        "pagesize": 20,
        "page": 1,
        "hasSyncClue": 0,
        "hasSyncRobot": 0,
        "hasUnfolded": 0,
        "sortBy": 0
    }
    r = requests.post(url, headers=headers, json=body, verify=False)
    res = r.json()
    if res['error_code'] != 0:
        return res['message']
    else:
        return res['data']
    # if json.loads(r.text)['error_code'] != 0:
    #     print('搜索接口报错\n',r.json())
    # else:
    #     data=json.loads(r.text)['data']
    #     return(data)


def nestedSearch_API(cn1,nn1,cr1,cv1,cn2,nn2,cr2,cv2):
    body={
        # "isCustomerTemplate": 1,
        "condition": {
            "cn": "composite",
            "cr": "MUST",
            "cv": [
                    { "cn":"compositeNested",
                      "path": nn1.split('.')[0],
                      "cr": "MUST",
                      "cv": [
                                { "cn": cn1,
                                  "nn": nn1,
                                  "cr": cr1,
                                  "cv": cv1 },
                                {  "cn": cn2,
                                   "nn": nn2,
                                   "cr": cr2,
                                   "cv": cv2 }
                            ]
                      }]
        },
        "pagesize": 10,
        "page": 1,
        "hasSyncClue": 0,
        "hasSyncRobot": 0,
        "hasUnfolded": 0,
        "sortBy": 0
    }
    # planmald = {
    #     "hasSyncClue": 0,
    #     "hasSyncRobot": 0,
    #     "hasUnfolded": 0,
    #     "sortBy": 0,
    #     "page": 1,
    #     "pagesize": 10,
    #     "condition": {
    #         "cn": "composite",
    #         "cr": "MUST",
    #         "cv": [
    #             {
    #                 "cn": "compositeNested",
    #                 "path": inData[0]['nn'].split('.')[0],
    #                 "cr": "MUST",
    #                 "cv": [
    #                     {
    #                         "cn": inData[0]['cn'],
    #                         "cr": inData[0]['cr'],
    #                         "cv": inData[0]['cv'],
    #                         "nn": inData[0]['nn']
    #                     },
    #                     {
    #                         "cn": inData[1]['cn'],
    #                         "cr": inData[1]['cr'],
    #                         "cv": inData[1]['cv'],
    #                         "nn": inData[1]['nn']
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # }
    r = requests.post(url, headers=headers, json=body, verify=False)
    res = r.json()
    if res['error_code'] != 0:
        return res['message']
    else:
        return res
    # if json.loads(r.text)['error_code'] != 0:
    #     print('搜索接口报错')
    # else:
    #     data=json.loads(r.text)['data']
    #     return(data)


# if __name__ == '__main__':
#     a = search_API('isChineseTop500', 'IS', 'true')
#     print(a)
#     b = nestedSearch_API([
#     {"cn": "recruitPlatform","cr": "IN","cv": ["54"],"nn": "recruitment.platform"},
#     {"cn": "recruitment.jobDetail","cr": "IN", "cv": ["测试"],"nn": "recruitment.jobDetail"}
#     ])
#     print(b)
