# -*- coding: utf-8 -*-

import requests, json, urllib3
from API_project.Configs.config_API import user

urllib3.disable_warnings()


class search:
    def __init__(self, test):
        self.user = user(test)

    def skb_contacts_num(self,module='skb', headers=None, id=None):  # 查询联系方式
        """
        :param headers: 用户信息
        :param pid: 企业pid/店铺id
        :return:
        """
        url = f'https://{self.user.skb_Host()}/api_skb/v1/clue/contacts_num'
        if headers == None:
            header = self.user.headers()
        else:
            header = headers
        if module=='skb':
            payload = {'pid': id}
        elif module=='skb':
            payload = {'shopId': id}
        else:
            payload = None
        response = requests.get(url, params=payload, headers=header)
        return response

    def shop_contacts_num(self, headers=None, shopId=None):  # 查询联系方式
        """
        :param headers: 用户信息
        :param shopId: 店铺id
        :return:
        """
        url = f'https://{self.user.skb_Host()}/api_skb/v1/shopClue/contacts_num'
        if headers == None:
            header = self.user.headers()
        else:
            header = headers
        payload = {'shopId': shopId}
        response = requests.get(url, params=payload, headers=header)
        return response

    def skb_search(self, keyword="北京", filterUnfold=2, filterSyncRobot=1, filterSync=1, contact=[1, 2]):
        """
        :param keyword: 搜索关键词
        :param filterUnfold:  是否查看，1：已查看，2：未查看，0：全部
        :param filterSyncRobot: 是否转机器人，1：未转，2：已转，0：全部
        :param filterSync: 是否转crm，1：未转，2：已转，"0"：全部
        :param contact:  联系方式搜索字段，1：手机，2：固话，
        :return:
        """
        url = f'https://{self.user.skb_Host()}/api_skb/v1/search'
        payload = {"keyword": keyword,
                   "filter": {"location": [], "industryshort": [], "secindustryshort": [], "registercapital": [],
                              "establishment": [], "entstatus": [], "contact": contact, "sortBy": "0",
                              "companysource": [],
                              "enttype": [0], "employees": [0], "hasrecruit": "0", "hassem": "0", "haswebsite": "0",
                              "hastrademark": "0", "haspatent": "0", "hastender": "0", "haswechataccnt": "0",
                              "filterUnfold": filterUnfold, "filterSync": filterSync,
                              "filterSyncRobot": filterSyncRobot, "hasBuildingCert": "0",
                              "isHighTech": "0", "hasFinanceInfo": "0", "hasAbnormalInfo": "0",
                              "syncRobotRangeDate": []}, "scope": "companyname", "matchType": "most_fields",
                   "pagesize": 10, "page": 1}
        header = self.user.shop_headers()
        response = requests.post(url, headers=header, json=payload, verify=False)  # 搜索未查看，未转机器人,未转crm，有手机，有固话的数据
        return response

    def skb_address_search(self, filterUnfold=2, filterSyncRobot=1, filterSync=1, contact=1):
        """
        :param filterUnfold: 是否查看，1：已查看，2：未查看，0：全部
        :param filterSyncRobot: 是否转机器人，1：未转，2：已转，0：全部
        :param filterSync:  是否转crm，1：未转，2：已转，"0"：全部
        :param contact: 联系方式搜索字段，1：手机，2：固话，
        :return:
        """
        url = f'https://{self.user.skb_Host()}/api_skb/v1/search'
        payload = {"scope": "address", "keyword": "", "page": 1, "pagesize": 20,
                   "filter": {"location": ["110105"], "industryshort": [], "secindustryshort": [],
                              "establishment": ["0"], "contact": [contact], "entstatus": [1], "circle": None, "filterSync": filterSync,
                              "filterUnfold": filterUnfold, "filterSyncRobot": filterSyncRobot, "registercapital": ["0"], "enttype": ["0"]}}
        header = self.user.shop_headers()
        response = requests.post(url, headers=header, json=payload, verify=False)  # 搜索未查看，未转机器人,未转crm，有手机，有固话的数据
        return response

    def advanced_search(self, cv=None, hasSyncClue=1, hasSyncRobot=1, hasUnfolded=2):  # 高级搜索单个条件搜索
        """
        :param cv:  搜索条件
        :param hasSyncClue:  是否转crm，1：未转，2：已转，0：全部
        :param hasSyncRobot:  是否转机器人，1：未转，2：已转，0：全部
        :param hasUnfolded:  是否查看，1：已查看，2：未查看，0：全部
        :return:
        """
        if cv is None:
            cv = [{"cn": "hasMobile", "cr": "IS", "cv": True},
                  {"cn": "hasFixed", "cr": "IS", "cv": True}]
        else:
            cv = cv
        URL = f'https://{self.user.skb_Host()}/api_skb/v1/advanced_search'
        body = {"hasSyncClue": hasSyncClue,
                "hasSyncRobot": hasSyncRobot,
                "hasUnfolded": hasUnfolded,
                "sortBy": 0,
                "syncRobotRangeDate": [],
                "condition": {"cn": "composite",
                              "cr": "MUST",
                              "cv": cv},
                "page": 1,
                "pagesize": 10,
                "templateType": 0,
                "templateName": "",
                "userClick": 1}
        r = requests.post(URL, headers=self.user.headers(), json=body, verify=False)
        return (r)

    def search_API(self, cn, cv, cr):  # 高级搜索单个条件搜索
        URL = f'https://{self.user.skb_Host()}/api_skb/v1/advanced_search'
        body = {
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
        r = requests.post(URL, headers=self.user.headers(), json=body, verify=False)
        if json.loads(r.text)['error_code'] != 0:
            print('搜索接口报错')
        else:
            data = json.loads(r.text)['data']
            print(URL)
            return (data)

    def nestedSearch_API(self, cn1, nn1, cr1, cv1, cn2, nn2, cr2, cv2):  ##高级搜索附加条件搜索
        URL = f'https://{self.user.skb_Host()}/api_skb/v1/advanced_search'
        body = {
            "isCustomerTemplate": 1,
            "condition": {
                "cn": "composite",
                "cr": "MUST",
                "cv": [
                    {"cn": "compositeNested",
                     "cr": "MUST",
                     "path": nn1.split('.')[0],
                     "cv": [
                         {"cn": cn1,
                          "nn": nn1,
                          "cr": cr1,
                          "cv": cv1},
                         {"cn": cn2,
                          "nn": nn2,
                          "cr": cr2,
                          "cv": cv2}
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
        r = requests.post(URL, headers=self.user.headers(), json=body, verify=False)
        if json.loads(r.text)['error_code'] != 0:
            print('搜索接口报错')
        else:
            data = json.loads(r.text)['data']
            return (data)


class getCompanyBaseInfo:
    def __init__(self, test):
        self.get_search = user(test)

    def getCompanyBase(self, pid):
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
