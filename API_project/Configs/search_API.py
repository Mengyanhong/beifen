# -*- coding: utf-8 -*-

import requests,json,urllib3
from API_project.Configs.config_API import user
urllib3.disable_warnings()

class search:
    def __init__(self, test):
        self.user = user(test)

    def skb_contacts_num(self,headers=None,pid=None):  # 查询联系方式
        url = f'https://{self.user.skb_Host()}/api_skb/v1/clue/contacts_num'
        if headers == None:
            header = self.user.headers()
        else:
            header = headers
        payload ={'pid':pid}
        response = requests.get(url,params=payload,headers=header)
        return response

    def search_API(self,cn,cv,cr): #高级搜索单个条件搜索
        URL = f'https://{self.user.skb_Host()}/api_skb/v1/advanced_search'
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
        r=requests.post(URL,headers=self.user.headers(),json=body, verify=False)
        if json.loads(r.text)['error_code'] != 0:
            print('搜索接口报错')
        else:
            data=json.loads(r.text)['data']
            print(URL)
            return(data)

    def nestedSearch_API(self,cn1,nn1,cr1,cv1,cn2,nn2,cr2,cv2): ##高级搜索附加条件搜索
        URL = f'https://{self.user.skb_Host()}/api_skb/v1/advanced_search'
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
        r=requests.post(URL,headers=self.user.headers(),json=body, verify=False)
        if json.loads(r.text)['error_code'] != 0:
            print('搜索接口报错')
        else:
            data=json.loads(r.text)['data']
            return(data)

class getCompanyBaseInfo:
    def __init__(self,test):
        self.get_search = user(test)

    def getCompanyBase(self,pid):
        url = f'https://{self.get_search.biz_url()}/api_skb/v1/companyDetail/getCompanyBaseInfo?'
        params = {'id': f'{pid}',
                  'countSection': 1,
                  'market_source': 'advance_search_list',
                  'version': 'v3',
                  'search_result_size': 10,
                  'search_result_page': 1,
                  }

        re_tag = requests.get(url, params=params,
                              headers=self.get_search.headers())
        return (re_tag)




