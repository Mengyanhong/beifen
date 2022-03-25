from API_project.Configs.Config_Info import Config_info
import requests, json, urllib3, pprint, time

urllib3.disable_warnings()


class Skb_Search_Api(Config_info):
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
        lists_Qq = []
        lists_Email = []
        lists_Mobile_sources = set()
        lists_Fixed_sources = set()
        lists_contacts_sources = set()
        contacts_one_mobile = None  # 第一条联系方式为手机，获取联系方式号码
        contacts_one = None  # 获取第一条联系方式，手机或者固话
        contact_response = self.skb_contacts_num(id=pid, module=module).json()
        if contact_response["error_code"] != 0:
            print(pid, entName, "联系方式接口调用失败", contact_response)
            assert contact_response["error_code"] == 0
            unfoldNum = False
        else:
            if contact_response['data']['contacts']:
                unfoldNum = True
                details_response_contacts_value = contact_response['data']['contacts']
            elif contact_response['data']['contactNum'] != 0:
                unfoldNum = False
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
                unfoldNum = True
                # print('pid:', pid, '企业名称', entName, '\n该企业联系方式为空', contact_response)
                details_response_contacts_value = []

            if details_response_contacts_value:
                contacts_sum = 0  # 设置初始值计数
                for contacts_value in details_response_contacts_value:
                    if contacts_value['type'] == 1:
                        if contacts_sum == 0:
                            contacts_one_mobile = contacts_value['content']
                            contacts_one = contacts_value['content']
                        contacts_sum += 1
                        lists_Mobile.append(contacts_value['content'])
                        for contact_sources_value in contacts_value['sources']:
                            lists_Mobile_sources.add(contact_sources_value["sourceName"])
                            lists_contacts_sources.add(contact_sources_value["sourceName"])
                    elif contacts_value['type'] == 2:
                        if contacts_sum == 0:
                            contacts_one = contacts_value['content']
                        contacts_sum += 1
                        lists_Fixed.append(contacts_value['content'])
                        for contact_sources_value in contacts_value['sources']:
                            lists_Fixed_sources.add(contact_sources_value["sourceName"])
                            lists_contacts_sources.add(contact_sources_value["sourceName"])
                    elif contacts_value['type'] == 3:
                        contacts_sum += 1
                        lists_Qq.append(contacts_value['content'])
                        for contact_sources_value in contacts_value['sources']:
                            lists_contacts_sources.add(contact_sources_value["sourceName"])
                    else:
                        contacts_sum += 1
                        lists_Email.append(contacts_value['content'])
                        for contact_sources_value in contacts_value['sources']:
                            lists_contacts_sources.add(contact_sources_value["sourceName"])
        return {"Mobile": lists_Mobile, "Fixed": lists_Fixed, "Qq": lists_Qq, "Email": lists_Email,
                "Mobile_sources": list(lists_Mobile_sources), "Fixed_sources": list(lists_Fixed_sources),
                "contacts_sources": list(lists_contacts_sources), "contacts_one_mobile": contacts_one_mobile,
                "contacts_one": contacts_one, "unfoldNum": unfoldNum}

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
                   "pagesize": 10, "page": 2}
        response = requests.post(url, headers=self.headers_skb(), json=payload,
                                 verify=False)  # 搜索未查看，未转机器人,未转crm，有手机，有固话的数据
        return response

    def skb_address_search(self, filterUnfold=2, filterSyncRobot=1, filterSync=1, contact=1):
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
        url = f'https://{self.skb_url_Host()}/api_skb/v1/advanced_search'
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
        response = requests.post(url=url, headers=self.headers_skb(), json=body, verify=False)
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

    def search_shop(self, headers=None, shopName="", hasUnfolded=2, hasSyncClue=1, hasSyncRobot=1, cv=None):
        if cv is None:
            cv = [{"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": ["1030"]}, "cr": "IN"},
                  {"cn": "contactType", "cv": ["1", "2"], "cr": "IN"}]
        else:
            cv = cv
        if hasUnfolded != 2:
            hasUnfolded = hasUnfolded
        if hasSyncClue != 1:
            hasSyncClue = hasSyncClue
        if hasSyncRobot != 1:
            hasSyncRobot = hasSyncRobot
        url = f'https://{self.skb_url_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": shopName, "hasUnfolded": hasUnfolded, "hasSyncClue": hasSyncClue,
                           "hasSyncRobot": hasSyncRobot,
                           "syncRobotRangeDate": [], "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": cv}}

        response = requests.post(url, headers=self.headers_skb(), json=Request_payload)
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

    # 获取查看状况
    def unfoldStatistics_Api(self, way, search_payload, pid_list, sync_from="syncRobot", page=None):
        url = f'https://{self.skb_url_Host()}/api_skb/v1/unfoldStatistics'
        payload = {
            "pids": pid_list,
            "way": way,
            "from": sync_from
        }
        payload.update(search_payload)
        if page is not None:
            payload.update({"page": 1, "pagesize": page})
            payload.pop("pids")
        else:
            payload.pop("page")
            payload.pop("pagesize")
        if way == "shop_search_list":
            payload.pop("from")
            url = f'https://{self.skb_url_Host()}/api_skb/v1/shop/unfoldStatistics'
        response = requests.post(url=url, headers=self.headers_skb(), json=payload)
        return response


class Get_Company_Info(Skb_Search_Api):
    # def __init__(self, test):
    #     self.user = User_Config(test)

    def getCompanyBase(self, pid):  # 请求详情页信息
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getCompanyBaseInfo?'
        params = {'id': f'{pid}',
                  'countSection': 1,
                  'market_source': 'advance_search_list',
                  'version': 'v3',
                  'search_result_size': 10,
                  'search_result_page': 1,
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb())
        return response

    def getEntSectionInfo(self, pid, section, label=None, page=None):  # 企业详情一级菜单
        '''
        :param pid: #企业pid
        :param section: #菜单选择，Development：企业发展,RiskInfo:风险信息, ManageInfo:经营情况
        :param label: #数据维度，TradeShow：参展
        :param page: #翻页页码
        :return:
        '''

        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        if page is not None:
            params = {'id': f'{pid}',
                      'label': label,
                      'page': page,
                      'section': section,
                      'version': 'v2'
                      }
        else:
            params = {'id': f'{pid}',
                      'section': section,
                      'version': 'v2'
                      }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getAnnualReportDetail(self, annualReportId):  # 年报详情获取
        '''
        :param annualReportId: #年报id
        :return:
        '''
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getAnnualReportDetail?'
        params = {'annualReportId': annualReportId,
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_ManageInfo(self, pid, sourceName):  # 经营情况_招聘平台筛选
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'page': 1,
                  'section': 'ManageInfo',
                  'label': 'RecruitmentDetail',
                  'sourceName': sourceName,
                  'version': 'v2',
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_IPR(self, pid, templateSuppiler):  # 知识产权_建站方筛选
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'page': 1,
                  'section': 'IPR',
                  'label': 'WebsiteInformation',
                  'templateSuppiler': templateSuppiler,
                  'version': 'v2',
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getWebsiteInfo(self, _id):  # 知识产权_建站方_详情
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getWebsiteInfo?'
        params = {'id': f'{_id}'}
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_RiskInfo_subset(self, pid, page=1, subset='EndBookInfo'):  # 风险信息子菜单_详情
        '''

        :param pid: #企业pid
        :param page: #翻页页码
        :param subset: #风险信息下的子菜单，EndBookInfo：终本案件，Executor：被执行人
        :return:
        '''
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {
            'label': subset,
            'id': f'{pid}',
            'page': page,
            'section': 'RiskInfo',
            'version': 'v2'
        }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_InterpersonalRelations(self, pid):  # 员工人脉_详情
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {'id': f'{pid}',
                  'section': 'InterpersonalRelations',
                  'version': 'v2',
                  'pageSize': 20
                  }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response

    def getEntSectionInfo_InterpersonalRelations_subset(self, pid, page=1, subset='Maimai'):  # 员工人脉子菜单_详情
        '''
        :param pid: #企业pid
        :param page: #翻页页码
        :param subset: #员工人脉下的子菜单，Maimai：脉脉，LinkedinUserInfo：领英，PersonalMicroblog：微博
        :return:
        '''
        url = f'https://{self.biz_url_Host()}/api_skb/v1/companyDetail/getEntSectionInfo?'
        params = {
            'label': subset,
            'id': f'{pid}',
            'page': page,
            'pageSize': 20,
            'section': 'InterpersonalRelations',
            'version': 'v2'
        }
        response = requests.get(url, params=params,
                                headers=self.headers_skb(), verify=False)
        return response


#
# if __name__ == '__main__':
#     pprint.pprint(
#         getCompanyBaseInfo('test').getCompanyBase(pid='c495bbe252bd24337b88ad8f355dedeb').json()['data']['tags'])

# if __name__ == '__main__':
#     print(getCompanyBaseInfo('test').getEntSectionInfo_RiskInfo_subset(
#         pid='90c2f9836fe55b385f877f629bc59aee', subset='Executor').json())
# import time
# if __name__ == '__main__':
#     re = getCompanyBaseInfo("test").getEntSectionInfo(pid="958c3be9812d5c13cb4d15eeacc6c793",
#                                                       section='ManageInfo',label='TradeShow',page=2).json()
#     print(re)
#     totals = re['data']["TradeShow"]['total']
#     startDate_list = []
#     if 10 < totals:
#         totals_num = round(totals // 10)
#         totals_nums = round(totals / 10, 2)
#         if totals_nums > totals_num:
#             totals_num+=2
#         print(totals_num)
#         print(totals_nums)
#         for totalss in range(2, totals_num):
#             print(totalss)
#             details_responses = getCompanyBaseInfo("test").getEntSectionInfo(pid="958c3be9812d5c13cb4d15eeacc6c793",
#                                                                            section='ManageInfo',
#                                                                            label='TradeShow',
#                                                                            page=totalss).json()
#             print(details_responses)
#             for AnnualReport_items_ids in details_responses['data']['TradeShow']['items']:
#                 if AnnualReport_items_ids["startDate"] != "":
#                     startDate_list.append(time.strftime("%Y-%m-%d", time.localtime(
#                         int(AnnualReport_items_ids["startDate"]) / 1000)))
#     print(startDate_list)
class Robot_Api(Skb_Search_Api):
    # 查询号码管理内号码是否存在
    def robot_uncalled(self, query_name, queryType=2, created_at=None, phoneType=None, page=1, per_page=1000):
        """
         # 查询号码管理内号码是否存在
        :param page:
        :param per_page: 查询数量
        :param phoneType: 查询时号码类型筛选，1：固话，0：手机
        :param created_at:  时间过滤
        :param query_name: 查询内容，str型
        :param queryType:  查询字段，int型，1：姓名，2：公司名，3：号码,4:外呼计划编号
        :return:
        """
        url = f'https://{self.robot_url_Host()}/api/v1/customers/uncalled'
        if phoneType is not None:
            uncalled_payload = {
                'page': page,
                'per_page': per_page,
                'queryType': queryType,
                'query': query_name,
                'phoneType': phoneType
            }
        else:
            uncalled_payload = {
                'page': page,
                'per_page': per_page,
                'queryType': queryType,
                'query': query_name
            }
        if created_at is not None:
            uncalled_payload.update({'created_at': created_at})
        response = requests.get(url, params=uncalled_payload, headers=self.headers_robot())
        assert response.status_code == 200
        return response

    # 查询任务记录
    def task_list(self):
        url = "https://{}/api_skb/v1/clues/task_list?pageNum=1&pageSize=10".format(self.skb_url_Host())
        # payload = {}
        response = requests.get(url=url, headers=self.headers_skb())
        # assert response.status_code == 200
        # request_payloads = json.loads(response.request.body.decode("unicode_escape"))
        status_code = response.status_code
        request_url = response.request.url
        request_headers = response.request.headers
        response_value = response.json()
        response.close()
        if status_code != 200:
            print("搜索结果为空", response_value, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert status_code == 200
        elif response_value["error_code"] != 0:
            print("搜索结果有误", response_value, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['error_code'] == 0
        elif not response_value['data']['result']:
            print("搜索结果为空", response_value, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data']['result']
        elif response_value['data']['result'][0] == {}:
            print("搜索结果为空", response_value, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data']['result'][0] != {}
        return response_value

    # 查询任务记录详情
    def task_contact_list(self, taskId, errorReason='', contactType='', success='', pageSize=10, pageNum=1):
        '''
        查询任务记录详情
        :param taskId: 任务id
        :param errorReason:转移失败原因
        :param contactType:号码类型1：手机，2:固话
        :param success:转移状态，True,False
        :param pageSize: 展示数量
        :param pageNum: 页码
        :return:
        '''
        url = "https://{}/api_skb/v1/clues/task_contact_list?".format(self.skb_url_Host())
        payload = {'taskId': taskId,
                   'errorReason': errorReason,
                   'contactType': contactType,
                   'success': success,
                   'pageSize': pageSize,
                   'pageNum': pageNum
                   }
        response = requests.get(url=url, params=payload, headers=self.headers_skb())
        status_code = response.status_code
        request_url = response.request.url
        request_headers = response.request.headers
        response_value = response.json()
        if status_code != 200:
            print("搜索接口报错", response_value, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert status_code == 200
        elif response_value["error_code"] != 0:
            print("搜索结果有误", response_value, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['error_code'] == 0
        elif response_value['data'] == {}:
            print("搜索结果为空", response_value, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data'] != {}
        else:
            response.close()
        return response_value

    # 查询外呼计划
    def robot_out_call_plan(self, gateway_Id=None):
        """
        :param gateway_Id: 计划线路，str类型
        :return:
        """
        if self.host == "lxcrm":
            gateway_Id = self.robot_gateway()["gatewayId"]
        if gateway_Id is None:
            payload = {"page": 1, "per_page": 10}
        else:
            payload = {"page": 1, "per_page": 10, "gatewayId": gateway_Id}
        url = f'https://{self.robot_url_Host()}/api/v1/plan/list'
        response = requests.post(url, json=payload, headers=self.headers_robot())
        assert response.status_code == 200
        assert response.json()["data"]["list"] != []
        return response

    # 执行转机器人
    def robot_sync(self, out_id=None, pids=None, pages=None, seach_value=None, useQuota=True,
                   dataColumns=None, phoneStatus=None, numberCount=0, needCallPlan=False, canCover=False, way=None,
                   gatewayId=None, surveyId=None, gateway_name=None):
        """
        :param gateway_name: 计划名称
        :param out_id: 计划ID
        :param pids: pid数量
        :param pages: 页码
        :param seach_value: 搜索传参
        :param useQuota: 扣点方式
        :param dataColumns: 号码类型
        :param phoneStatus: 过滤方式
        :param numberCount: 转移号码方式
        :param needCallPlan: 是否需要创建外呼计划
        :param canCover: 重复号码是否导入
        :param way: 模块
        :param gatewayId: 外呼线路
        :param surveyId: 话术id
        :return:
        """

        if phoneStatus is None:
            phone = [0, 1, 2, 3]
        else:
            phone = phoneStatus
        if dataColumns is None:
            dataColumns = [0]
        if self.host == "lxcrm":
            gatewayId = self.robot_gateway()["gatewayId"]
        payload = {
            "way": way,
            "from": "syncRobot",
            "useQuota": useQuota,  # 是否使用额度
            "dataColumns": dataColumns,  # 数据字段[0, 1] // 0: 手机，1：固话
            "phoneStatus": phone,  # 手机过滤 [0, 1, 2 , 3] //[0, 1, 3]: 过滤疑似代理记账号码 [0, 1, 2]: 过滤异常号码
            "numberCount": numberCount,  # 号码数量 0: 全部,1: 仅一条
            "canCover": canCover,  # 重复号码是否导入 true / false
            "needCallPlan": needCallPlan,  # 是否需要创建外呼计划 true / false
        }
        out_payload = {
            "id": out_id,
            "need_push": 0,
            "retry_interval": None,
            "max_retry": None,
            "gatewayNumberId": None,
            "start_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "hangup_message_rules": [],
            "call_type": 0,
            "customers_ids": [],
            "platform": "IK"
        }

        gatewayId_value = {
            "plan_name": gateway_name,
            "survey_id": surveyId,
            "gatewayId": gatewayId,
            "strategy": 1,
            "need_push": 1,
            "need_finish_message": True,
            "start_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "need_hangup_message": False,
            "retry_interval": None,
            "max_retry": None,
            "gatewayNumberId": None,
            "hangup_message_rules": [],
            "call_type": 0,
            "customers_ids": [],
            "platform": "IK"
        }
        payload.update(seach_value)
        if pids is None:
            payload.update({"page": 1, "pagesize": pages})
        else:
            payload.update({"pids": pids})
            payload.pop('page')
            payload.pop('pagesize')
        if way == 'shop_search_list':
            payload.pop("from")
            clues = 'shopClues'
        else:
            clues = 'clues'
        if needCallPlan is True:
            if out_id is not None:
                print("加入的外呼计划为，" + gateway_name)
                payload.update({"payload": out_payload})
            else:
                print("创建的外呼计划为，" + gateway_name)
                payload.update({"payload": gatewayId_value})
        url = f'https://{self.skb_url_Host()}/api_skb/v1/{clues}/sync_robot'
        response = requests.post(url=url, headers=self.headers_skb(), json=payload)
        return response


# if __name__ == "__main__":
#     response = Robot_Api("test").task_list()
#     print(response)
# if __name__=="__main__":
#     a={'pid': '394a27a9b217a903699f914b90f3baf8', 'company_name': '天津海泰旅游管理有限公司'}
#     b = Robot_Api("test").robot_uncalled(query_name=a["company_name"],phoneType=str(1), queryType=2)
#     print(b.json())
# if __name__ == '__main__':
#     from pprint import pprint
#     pprint(Robot_Api("test").robot_out_call_plan().json())
# if __name__ == "__main__":
#     from pprint import pprint
#     pprint(Robot_Api("staging").task_contact_list())

class Skb_Shop_Api(Robot_Api):
    # def __init__(self, test):
    #     self.user = User_Config(test)

    def search_shop(self, headers=None, shopName="", hasUnfolded=2, hasSyncClue=1, hasSyncRobot=1, cv=None):
        if cv is None:
            cv = [{"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": ["1030"]}, "cr": "IN"},
                  {"cn": "contactType", "cv": ["1", "2"], "cr": "IN"}]
        else:
            cv = cv
        if hasUnfolded != 2:
            hasUnfolded = hasUnfolded
        if hasSyncClue != 1:
            hasSyncClue = hasSyncClue
        if hasSyncRobot != 1:
            hasSyncRobot = hasSyncRobot
        url = f'https://{self.skb_url_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": shopName, "hasUnfolded": hasUnfolded, "hasSyncClue": hasSyncClue,
                           "hasSyncRobot": hasSyncRobot,
                           "syncRobotRangeDate": [], "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": cv}}
        if headers is None:
            header = self.headers_skb()
        else:
            header = headers
        response = requests.post(url, headers=header, json=Request_payload)
        return response

    def category(self, shopName="", hasUnfolded=0, hasSyncClue=0, hasSyncRobot=0, cv=None, categoryL1=None,
                 categoryL2=None, headers=None, page=1, pagesize=10):
        '''

        :param shopName: 关键词
        :param hasUnfolded: 查看状态，0：全部，1：已查，2：未查
        :param hasSyncClue: 转线索状态，0：全部，1：未转，2：已转
        :param hasSyncRobot: 转机器人状态，0：全部，1：未转，2：已转
        :param cv: 筛选条件
        :param categoryL1: 一级分类筛选
        :param categoryL2: 二级分类筛选
        :param headers: 用户信息
        :param page: 页码
        :param pagesize: 结果数
        :return: 搜索结果
        '''
        if categoryL1 is None:
            categoryL1 = []
        else:
            categoryL1 = [categoryL1]
        if categoryL2 is None:
            categoryL2 = []
        else:
            categoryL2 = [categoryL2]
        if cv is None:
            cv = [{'cn': 'category', 'cv': {'categoryL1': categoryL1, 'categoryL2': categoryL2}, 'cr': 'IN'}]
        if hasUnfolded != 2:
            hasUnfolded = hasUnfolded
        if hasSyncClue != 1:
            hasSyncClue = hasSyncClue
        if hasSyncRobot != 1:
            hasSyncRobot = hasSyncRobot
        if shopName != "":
            shopName = shopName
        if headers is None:
            headers = self.headers_skb()
        if page != 1:
            page = page
        if pagesize != 10:
            pagesize = pagesize
        url = f'https://{self.skb_url_Host()}/api_skb/v1/shop_search'
        Request_payload = {'shopName': shopName, 'hasUnfolded': hasUnfolded, 'hasSyncClue': hasSyncClue,
                           'hasSyncRobot': hasSyncRobot, 'syncRobotRangeDate': [], 'page': page, 'pagesize': pagesize,
                           'condition': {'cn': 'composite', 'cr': 'MUST', 'cv': cv}}
        response = requests.post(url=url, headers=headers, json=Request_payload)
        return response

    def area_province(self, province):
        url = f'https://{self.skb_url_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [province], "city": [], "district": []}, "cr": "IN"}]}}
        response = requests.post(url, headers=self.headers_skb(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()

    def area_city(self, city):
        url = f'https://{self.skb_url_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [], "city": [city], "district": []}, "cr": "IN"}]}}
        response = requests.post(url, headers=self.headers_skb(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()

    def area_district(self, district):
        url = f'https://{self.skb_url_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [], "city": [], "district": [district]}, "cr": "IN"}]}}
        response = requests.post(url, headers=self.headers_skb(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()


class Config_api(Robot_Api):
    '''
    api调用
    '''
