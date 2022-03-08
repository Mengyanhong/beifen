
from API_project.Configs.Configuration import User_Config
import requests, json, urllib3, pprint

urllib3.disable_warnings()


class Skb_Search_Api(User_Config):
    # def __init__(self, test):
    #     self.user = User_Config(test)

    def skb_contacts_num(self, module='shop_search_list', id=None):  # 查询联系方式
        """

        :param module: 查询模块
        :param id: 企业id
        :return:
        """
        payload = {'pid': id}
        clue_path = 'clue'
        if module == 'shop_search_list':
            payload = {'shopId': id}
            clue_path = 'shopClue'
        url = f'https://{self.skb_url_Host()}/api_skb/v1/{clue_path}/contacts_num'
        response = requests.get(url=url, params=payload, headers=self.headers_skb(), verify=False)
        return response

    def skb_contacts(self, entName, module=None, id=None):  # 查询联系方式
        """
        :param entName: 企业名称
        :param module: 查询模块
        :param id: 企业id
        :return:
        """

        clue_path = 'clue'
        if module == "search_list":
            sources = 'search_detail'
        elif module == "advanced_search_list":
            sources = 'advance_search_detail'
        elif module == "map_search_list":
            sources = 'map_search_detail'
        elif module == "shop_search_list":
            sources = 'shop_search_list'
            clue_path = 'shopClue'
        elif module == "industry_tags_search_list":
            sources = 'industry_tags_search_detail'
        elif module == "batch_search_list":
            sources = 'batch_search_detail'
        else:
            sources = 'search_detail'
        payload = {'pid': id,
                   'source': sources,
                   'entName': entName}

        url = f'https://{self.skb_url_Host()}/api_skb/v1/{clue_path}/contacts'
        response = requests.get(url=url, params=payload, headers=self.headers_skb(), verify=False)
        return response

    def skb_list_contact(self, pid, entName, module, useQuota=True):
        lists_Mobile = []
        lists_Fixed = []
        lists_Email = []
        lists_Qq = []
        lists_Mobile_sources = set()
        lists_Fixed_sources = set()
        lists_contacts_sources = set()
        contact_response = self.skb_contacts_num(id=pid, module=module).json()
        contact_response_contact = contact_response['data']['contacts']
        contact_response_contactNum = contact_response['data']['contactNum']
        if contact_response["error_code"] != 0:
            print(pid, entName, "联系方式接口调用失败", contact_response)
            assert contact_response["error_code"] == 0
        else:
            if contact_response_contact:
                details_response_contacts_value = contact_response_contact
            elif contact_response_contactNum != 0:
                if useQuota is True:
                    contact_response_tow = self.skb_contacts(id=pid, entName=entName, module=module).json()
                    if contact_response_tow["error_code"] != 0:
                        print(pid, entName, "联系方式接口调用失败tow", contact_response_tow)
                        details_response_contacts_value = []
                        assert contact_response_tow["error_code"] == 0
                    elif not contact_response_tow['data']['contacts']:
                        print(pid, entName, "有联系方式但是获取失败tow", contact_response_tow)
                        details_response_contacts_value = []
                        assert contact_response_tow['data']['contacts'] != []
                    else:
                        details_response_contacts_value = contact_response_tow['data']['contacts']
                else:
                    details_response_contacts_value = []
            else:
                print('pid:', pid, '企业名称', entName, '\n该企业联系方式为空', contact_response)
                details_response_contacts_value = []

            if details_response_contacts_value:
                for contacts_value in details_response_contacts_value:
                    if contacts_value['type'] == 1:
                        lists_Mobile.append(contacts_value['content'])
                        for contact_sources_value in contacts_value['sources']:
                            lists_Mobile_sources.add(contact_sources_value["sourceName"])
                            lists_contacts_sources.add(contact_sources_value["sourceName"])
                    elif contacts_value['type'] == 2:
                        lists_Fixed.append(contacts_value['content'])
                        for contact_sources_value in contacts_value['sources']:
                            lists_Fixed_sources.add(contact_sources_value["sourceName"])
                            lists_contacts_sources.add(contact_sources_value["sourceName"])
                    elif contacts_value['type'] == 3:
                        lists_Qq.append(contacts_value['content'])
                        for contact_sources_value in contacts_value['sources']:
                            lists_contacts_sources.add(contact_sources_value["sourceName"])
                    else:
                        lists_Email.append(contacts_value['content'])
                        for contact_sources_value in contacts_value['sources']:
                            lists_contacts_sources.add(contact_sources_value["sourceName"])
        return {"Mobile": lists_Mobile, "Fixed": lists_Fixed, "Qq": lists_Qq, "Email": lists_Email,
                "Mobile_sources": list(lists_Mobile_sources), "Fixed_sources": list(lists_Fixed_sources),
                "contacts_sources": list(lists_contacts_sources)}

    def skb_search(self, keyword="天津", filterUnfold=2, filterSyncRobot=1, filterSync=1, contact=[1, 2]):
        """
        :param keyword: 搜索关键词
        :param filterUnfold:  是否查看，1：已查看，2：未查看，0：全部
        :param filterSyncRobot: 是否转机器人，1：未转，2：已转，0：全部
        :param filterSync: 是否转crm，1：未转，2：已转，"0"：全部
        :param contact:  联系方式搜索字段，1：手机，2：固话，
        :return:
        """
        url = f'https://{self.skb_url_Host()}/api_skb/v1/search'
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
                   "pagesize": 10, "page": 4}
        response = requests.post(url, headers=self.headers_skb(), json=payload,
                                 verify=False)  # 搜索未查看，未转机器人,未转crm，有手机，有固话的数据
        return response

    def skb_address_search(self, headers=None, filterUnfold=2, filterSyncRobot=1, filterSync=1, contact=1):
        """
        :param filterUnfold: 是否查看，1：已查看，2：未查看，0：全部
        :param filterSyncRobot: 是否转机器人，1：未转，2：已转，0：全部f
        :param filterSync:  是否转crm，1：未转，2：已转，"0"：全部
        :param contact: 联系方式搜索字段，1：手机，2：固话，
        :return:
        """
        url = f'https://{self.skb_url_Host()}/api_skb/v1/search'
        payload = {"scope": "address", "keyword": "", "page": 3, "pagesize": 10,
                   "filter": {"location": ["120111"], "industryshort": [], "secindustryshort": [],
                              "establishment": ["0"], "contact": [contact], "entstatus": [1], "circle": None,
                              "filterSync": filterSync,
                              "filterUnfold": filterUnfold, "filterSyncRobot": filterSyncRobot,
                              "registercapital": ["0"], "enttype": ["0"]}}

        response = requests.post(url, headers=self.headers_skb(), json=payload,
                                 verify=False)  # 搜索未查看，未转机器人,未转crm，有手机，有固话的数据
        return response

    def advanced_search(self, cv=None, hasSyncClue=1, hasSyncRobot=1, hasUnfolded=2, page=1,
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
                  {"cn": "hasFixed", "cr": "IS", "cv": True},
                  {"cn": "hasQq", "cr": "IS", "cv": True, },
                  {"cn": "hasAbnormal", "cr": "IS", "cv": True}]
        else:
            cv = cv
        URL = f'https://{self.skb_url_Host()}/api_skb/v1/advanced_search'
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
        response = requests.post(URL, headers=self.headers_skb(), json=body, verify=False)
        return response

    def search_API(self, cn, cv, cr):  # 高级搜索单个条件搜索
        URL = f'https://{self.skb_url_Host()}/api_skb/v1/advanced_search'
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
        response = requests.post(URL, headers=self.headers_skb(), json=body, verify=False)
        return response

    def nestedSearch_API(self, cn1, nn1, cr1, cv1, cn2, nn2, cr2, cv2):  ##高级搜索附加条件搜索
        URL = f'https://{self.skb_url_Host()}/api_skb/v1/advanced_search'
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
        response = requests.post(URL, headers=self.headers_skb(), json=body, verify=False)
        return response