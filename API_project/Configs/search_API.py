# -*- coding: utf-8 -*-

import requests,json
import urllib3
urllib3.disable_warnings()
from API_project.Configs.config_API import user

class search:
    def __init__(self, test):
        self.test = test
        self.user = user(test)
    def url(self): #url环境配置
        if self.test == 'test':
            URL='https://skb-test.weiwenjia.com/api_skb/v1/advanced_search'
        elif self.test == 'staging':
            URL='https://skb-staging.weiwenjia.com/api_skb/v1/advanced_search'
        elif self.test == 'lxcrm':
            URL='https://skb.weiwenjia.com/api_skb/v1/advanced_search'
        else:
            print('传参错误')
            URL = None
        return URL
    def search_API(self,cn,cv,cr): #高级搜索单个条件搜索
        body={
            "isCustomerTemplate": 1,
            "condition": {
                "cn": "composite",
                "cr": "MUST",
                "cv": [
                    {
                        "cn": cn,
                        "cv": cv,
                        "cr": cr
                    }
                ]
            },
            "pagesize": 100,
            "page": 1,
            "hasSyncClue": 0,
            "hasSyncRobot": 0,
            "hasUnfolded": 0,
            "sortBy": 0
        }
        r=requests.post(search(self.test).url(),headers=self.user.headers(),json=body, verify=False)
        if json.loads(r.text)['error_code'] != 0:
            print('搜索接口报错')
        else:
            data=json.loads(r.text)['data']
            print(search(self.test).url())
            return(data)

    def nestedSearch_API(self,cn1,nn1,cr1,cv1,cn2,nn2,cr2,cv2): ##高级搜索附加条件搜索
        body={
            "isCustomerTemplate": 1,
            "condition": {
                "cn": "composite",
                "cr": "MUST",
                "cv": [
                        { "cn":"compositeNested",
                          "cr": "MUST",
                          "path": nn1.split('.')[0],
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
            "pagesize": 5,
            "page": 1,
            "hasSyncClue": 0,
            "hasSyncRobot": 0,
            "hasUnfolded": 0,
            "sortBy": 0
        }
        r=requests.post(search(self.test).url(),headers=self.user.headers(),json=body, verify=False)
        if json.loads(r.text)['error_code'] != 0:
            print('搜索接口报错')
        else:
            data=json.loads(r.text)['data']
            return(data)

class getCompanyBaseInfo:
    def __init__(self,test):
        self.test = test
        self.get_search = user(test)
    def url(self):
        if self.test == 'test':
            url = 'https://test.lixiaoskb.com/api_skb/v1/companyDetail/getCompanyBaseInfo?'
        elif self.test == 'staging':
            url = 'https://stage.lixiaoskb.com/api_skb/v1/companyDetail/getCompanyBaseInfo?'
        elif self.test == 'lxcrm':
            url = 'https://biz.lixiaoskb.com/api_skb/v1/companyDetail/getCompanyBaseInfo?'
        else:
            print('传参错误')
            url = None
        return url

    def getCompanyBase(self,pid):
        get_getCompanyBaseInfo = getCompanyBaseInfo(self.test)
        params = {'id': f'{pid}',
                  'countSection': 1,
                  'market_source': 'advance_search_list',
                  'version': 'v3',
                  'search_result_size': 10,
                  'search_result_page': 1,
                  }

        re_tag = requests.get(get_getCompanyBaseInfo.url(), params=params,
                              headers=self.get_search.headers())
        return (re_tag)




