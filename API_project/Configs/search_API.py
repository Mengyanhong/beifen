# -*- coding: utf-8 -*-

import requests, json, urllib3, pprint
from API_project.Configs.config_API import user

urllib3.disable_warnings()


class search:
    def __init__(self, test):
        self.user = user(test)

    def skb_contacts_num(self, module='shop_search_list', headers=None, id=None):  # 查询联系方式
        """
        :param headers: 用户信息
        :param pid: 企业pid/店铺id
        :return:
        """
        if module == 'shop_search_list':
            payload = {'shopId': id}
            clue_path = 'shopClue'
            header = self.user.headers()
        else:
            payload = {'pid': id}
            clue_path = 'clue'
            header = self.user.headers()

        url = f'https://{self.user.skb_Host()}/api_skb/v1/{clue_path}/contacts_num'

        response = requests.get(url, params=payload, headers=header)
        return response

    def skb_contacts(self, entName, module='shop_search_list', headers=None, id=None):  # 查询联系方式
        """
        :param headers: 用户信息
        :param pid: 企业pid/店铺id
        :return:
        """
        if module == 'shop_search_list':
            payload = {'shopId': id,
                       'source': 'shop_search_list',
                       'shopName': entName}
            clue_path = 'shopClue'
            header = self.user.headers()
        else:
            payload = {'pid': id,
                       'source': 'advance_search_detail',
                       'entName': entName}
            clue_path = 'clue'
            header = self.user.headers()

        url = f'https://{self.user.skb_Host()}/api_skb/v1/{clue_path}/contacts'

        response = requests.get(url, params=payload, headers=header)
        return response

    def skb_search(self, headers=None, keyword="北京", filterUnfold=2, filterSyncRobot=1, filterSync=1, contact=[1, 2]):
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
                   "pagesize": 3, "page": 2}
        if headers == None:
            header = self.user.headers()
        else:
            header = headers
        response = requests.post(url, headers=header, json=payload, verify=False)  # 搜索未查看，未转机器人,未转crm，有手机，有固话的数据
        return response

    def skb_address_search(self, headers=None, filterUnfold=2, filterSyncRobot=1, filterSync=1, contact=1):
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
                              "establishment": ["0"], "contact": [contact], "entstatus": [1], "circle": None,
                              "filterSync": filterSync,
                              "filterUnfold": filterUnfold, "filterSyncRobot": filterSyncRobot,
                              "registercapital": ["0"], "enttype": ["0"]}}

        if headers == None:
            header = self.user.headers()
        else:
            header = headers
        response = requests.post(url, headers=header, json=payload, verify=False)  # 搜索未查看，未转机器人,未转crm，有手机，有固话的数据
        return response

    def advanced_search(self, headers=None, cv=None, hasSyncClue=1, hasSyncRobot=1, hasUnfolded=2, page=1,
                        pagesize=10):  # 高级搜索单个条件搜索
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
                "page": page,
                "pagesize": pagesize,
                "templateType": 0,
                "templateName": "",
                "userClick": 1}
        if headers == None:
            header = self.user.headers()
        else:
            header = headers
        r = requests.post(URL, headers=header, json=body, verify=False)
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
            return data


class getCompanyBaseInfo:
    def __init__(self, test):
        self.user = user(test)

    def getCompanyBase(self, pid):  # 请求详情页信息
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getCompanyBaseInfo?'
        params = {'id': f'{pid}',
                  'countSection': 1,
                  'market_source': 'advance_search_list',
                  'version': 'v3',
                  'search_result_size': 10,
                  'search_result_page': 1,
                  }
        re_tag = requests.get(url, params=params,
                              headers=self.user.headers())
        return re_tag

    def getEntSectionInfo(self, pid, section, headers = None):  # 企业详情一级菜单
        '''

        :param pid:  #企业pid
        :param section:  #菜单选择，Development：企业发展,RiskInfo:风险信息, ManageInfo:经营情况
        :return:
        '''
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'section': section,
                  'version': 'v2'
                  }
        if headers == None:
            header = self.user.headers()
        else:
            header = headers
        response = requests.get(url, params=params,
                                headers=header, verify=False)
        return response
# if __name__ == '__main__':
#     re = getCompanyBaseInfo("test").getEntSectionInfo(pid="47df1dc4ade329964b2ea0f69ee7b8da",
#                       section='ManageInfo').json()
#     print(re)

    def getAnnualReportDetail(self, annualReportId):  # 年报详情获取
        '''
        :param annualReportId: #年报id
        :return:
        '''
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getAnnualReportDetail?'
        params = {'annualReportId': annualReportId,
                  }
        response = requests.get(url, params=params,
                                headers=self.user.headers())
        return response

    def getEntSectionInfo_ManageInfo(self, pid, sourceName):  # 经营情况_招聘平台筛选
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'page': 1,
                  'section': 'ManageInfo',
                  'label': 'RecruitmentDetail',
                  'sourceName': sourceName,
                  'version': 'v2',
                  }
        re_tag = requests.get(url, params=params,
                              headers=self.user.headers())
        return re_tag

    def getEntSectionInfo_IPR(self, pid, templateSuppiler):  # 知识产权_建站方筛选
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'page': 1,
                  'section': 'IPR',
                  'label': 'WebsiteInformation',
                  'templateSuppiler': templateSuppiler,
                  'version': 'v2',
                  }
        re_tag = requests.get(url, params=params,
                              headers=self.user.headers())
        return re_tag

    def getWebsiteInfo(self, _id):  # 知识产权_建站方_详情
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getWebsiteInfo?'
        params = {'id': f'{_id}'}
        re_tag = requests.get(url, params=params,
                              headers=self.user.headers())
        return re_tag

    def getEntSectionInfo_RiskInfo_subset(self, pid, page=1, subset='EndBookInfo'):  # 风险信息子菜单_详情
        '''

        :param pid: #企业pid
        :param page: #翻页页码
        :param subset: #风险信息下的子菜单，EndBookInfo：终本案件，Executor：被执行人
        :return:
        '''
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {
            'label': subset,
            'id': f'{pid}',
            'page': page,
            'section': 'RiskInfo',
            'version': 'v2'
        }
        response = requests.get(url, params=params,
                                headers=self.user.headers())
        return response

    def getEntSectionInfo_InterpersonalRelations(self, pid):  # 员工人脉_详情
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'section': 'InterpersonalRelations',
                  'version': 'v2',
                  'pageSize': 20
                  }
        response = requests.get(url, params=params,
                                headers=self.user.headers())
        return response

    def getEntSectionInfo_InterpersonalRelations_subset(self, pid, page=1, subset='Maimai'):  # 员工人脉子菜单_详情
        '''

        :param pid: #企业pid
        :param page: #翻页页码
        :param subset: #员工人脉下的子菜单，Maimai：脉脉，LinkedinUserInfo：领英，PersonalMicroblog：微博
        :return:
        '''
        url = f'https://{self.user.biz_url()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {
            'label': subset,
            'id': f'{pid}',
            'page': page,
            'pageSize': 20,
            'section': 'InterpersonalRelations',
            'version': 'v2'
        }
        response = requests.get(url, params=params,
                                headers=self.user.headers())
        return response


if __name__ == '__main__':
    pprint.pprint(
        getCompanyBaseInfo('test').getCompanyBase(pid='c495bbe252bd24337b88ad8f355dedeb').json()['data']['tags'])

# if __name__ == '__main__':
#     print(getCompanyBaseInfo('test').getEntSectionInfo_RiskInfo_subset(
#         pid='90c2f9836fe55b385f877f629bc59aee', subset='Executor').json())
