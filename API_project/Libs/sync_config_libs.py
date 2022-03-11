from pprint import pprint
import requests, json, time, pytest, os, random
from API_project.Configs.Configuration import User_Config
from API_project.Configs.search_API import search
from API_project.Configs.shop_API import shop_api


# 转移操作通用Api
class sync_config:
    def __init__(self, host, way, pages, headers=None, useQuota=True):
        '''
        初始化参数
        :param host:
        :param way:
        :param pages:
        :param canCover:
        :param dataColumns:
        :param numberCounts:
        :param headers:
        :param useQuota:
        '''
        self.host = host
        self.search = search(host)
        self.shop_search = shop_api(host)
        self.user_api = User_Config(host)
        self.way = way
        self.header = headers
        self.useQuota = useQuota
        self.pages = pages

        print('sync_config初始化参数,host,{}, way,{}, pages,{}, headers,{}, useQuota,{}'.
              format(host, way, pages, headers, useQuota))

    # 转移前各维度搜索结果处理

    def search_value_list(self):
        # 搜索未查看，未转机器人的数据，有固话
        if self.way == 'search_list':
            response = self.search.skb_search()
            list_companyName_add = 'companyName'
        elif self.way == 'advanced_search_list':
            response = self.search.advanced_search()
            list_companyName_add = 'companyName'
        elif self.way == 'shop_search_list':
            response = self.shop_search.search_shop()
            list_companyName_add = 'name'
        else:
            response = self.search.skb_address_search(contact=2)
            list_companyName_add = 'companyName'
        request_payloads = json.loads(response.request.body.decode("unicode_escape"))
        request_url = response.request.url
        request_headers = response.request.headers
        response_value = response.json()
        response.close()
        pid_list = []
        pid_companyName_list = []
        if response_value['data'] == {}:
            print("搜索结果为空", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data'] != {}
        elif response_value['data']['total'] == 0:
            print("搜索结果为空", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data']['total'] != 0
        elif response_value["error_code"] != 0:
            print("搜索异常", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['error_code'] != 0
        else:
            if response_value['data']['items']:
                for i in response_value['data']['items']:
                    pid_list.append(i['id'])
                    pid_companyName_list.append(
                        {'pid': i['id'], 'company_name': i[list_companyName_add]})
        return {"pid_list": pid_list, "pid_companyName_list": pid_companyName_list,
                "payloads_request": request_payloads}

    # 转移后等待转移结束
    def search_elapsed_time(self):
        # for date_value in range(200):
        # starting_time = time.time()
        time.sleep(2.2)
        if self.way == 'search_list':
            response = self.search.skb_search().json()
        elif self.way == 'advanced_search_list':
            response = self.search.advanced_search().json()
        elif self.way == 'shop_search_list':
            response = self.shop_search.search_shop().json()
        else:
            response = self.search.skb_address_search(contact=2).json()
        if response['error_code'] == 0:
            # end_time = time.time()
            print("转移结束,开始执行判断")
            # print('转移耗时', int(time.time() - stattime), 's')
        elif response['error_code'] == 401:
            print("接口401", response)
        elif response['error_code'] == 10007:
            self.search_elapsed_time()
        else:
            print("接口调用失败，搜索结果\n", response)

    # 转移前获取查看状况
    def unfoldStatistics_Api(self, search_payload, pid_list, sync_from="syncRobot", page=None, headers=None):
        url = f'https://{self.user_api.skb_url_Host()}/api_skb/v1/unfoldStatistics'
        payload = {
            "pids": pid_list,
            "way": self.way,
            "from": sync_from
        }
        if page is not None:
            payload.update({"page": 1, "pagesize": page})
            payload.pop("pids")
        if self.way == "shop_search_list":
            payload.pop("from")
            url = f'https://{self.user_api.skb_url_Host()}/api_skb/v1/shop/unfoldStatistics'
        payload.update(search_payload)
        if self.header is not None:
            headers = self.header
        elif headers is not None:
            headers = headers
        else:
            headers = self.user_api.headers_skb()
        response = requests.post(url=url, headers=headers, json=payload)
        return response

    # 联系方式获取
    def list_contact(self, pid, entName):
        # if self.useQuota is not True:
        #     useQuota = self.useQuota
        # elif useQuota is not True:
        #     useQuota = useQuota
        # else:
        #     useQuota = True
        list_contacts_value = self.search.skb_list_contact(pid=pid, entName=entName, module=self.way,
                                                           useQuota=self.useQuota)
        return list_contacts_value
        # lists_Mobile = []
        # lists_Fixed = []
        # lists_Email = []
        # lists_Qq = []
        # # lists_Mobile_sources = set()
        # # lists_Fixed_sources = set()
        # # lists_contacts_sources = set()
        #
        # contact_response = self.search.skb_contacts_num(id=pid, module=self.way).json()
        # contact_response_contact = contact_response['data']['contacts']
        # contact_response_contactNum = contact_response['data']['contactNum']
        # if contact_response["error_code"] != 0:
        #     print(pid, entName, "联系方式接口调用失败", contact_response)
        #     assert contact_response["error_code"] == 0
        # else:
        #     if contact_response_contact:
        #         details_response_contacts_value = contact_response_contact
        #     elif contact_response_contactNum != 0:
        #         contact_response_tow = self.search.skb_contacts(id=pid, entName=entName, module=self.way).json()
        #         if contact_response_tow["error_code"] != 0:
        #             print(pid, entName, "联系方式接口调用失败tow", contact_response_tow)
        #             details_response_contacts_value = []
        #             assert contact_response_tow["error_code"] == 0
        #         elif not contact_response_tow['data']['contacts']:
        #             print(pid, entName, "有联系方式但是获取失败tow", contact_response_tow)
        #             details_response_contacts_value = []
        #             assert contact_response_tow['data']['contacts'] != []
        #         else:
        #             details_response_contacts_value = contact_response_tow['data']['contacts']
        #     else:
        #         print('pid:', pid, '企业名称', entName, '\n该企业联系方式为空', contact_response)
        #         details_response_contacts_value = []
        #     if details_response_contacts_value:
        #         for contacts_value in details_response_contacts_value:
        #             if contacts_value['type'] == 1:
        #                 lists_Mobile.append(contacts_value['content'])
        #             elif contacts_value['type'] == 2:
        #                 lists_Fixed.append(contacts_value['content'])
        #             elif contacts_value['type'] == 3:
        #                 lists_Qq.append(contacts_value['content'])
        #             else:
        #                 lists_Email.append(contacts_value['content'])
        # return {"Mobile": lists_Mobile, "Fixed": lists_Fixed, "Qq": lists_Qq, "Email": lists_Email}

    # @staticmethod
    # 转机器人流量额度判断
    def sync_robot_quantity_verdicts(self, quantity_start=None, quantity_stop=None, quantity_rebate=None,
                                     hasSmartSyncRobot=True, hasUnfolded=None, useQuota=True, unfoldNum=0,
                                     pid_companyName_list_sum=None):
        pid_companyName_sum = len(pid_companyName_list_sum)
        if self.pages is None and self.way == "map_search_list":
            Unfolded_sum = 500
        elif self.pages is None:
            Unfolded_sum = pid_companyName_sum
        else:
            Unfolded_sum = self.pages
        # if self.useQuota is not True:
        #     useQuota = self.useQuota
        # elif useQuota is not True:
        #     useQuota = useQuota
        # else:
        #     useQuota = True
        if self.useQuota is True:
            if hasSmartSyncRobot is True:
                if quantity_start <= (Unfolded_sum - unfoldNum):
                    if quantity_stop != 0:
                        print(pid_companyName_list_sum)
                        print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
                              self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
                              Unfolded_sum, '企业数量', pid_companyName_sum)
                    assert quantity_stop == 0
                else:
                    if quantity_stop != (quantity_start - (Unfolded_sum - unfoldNum)):
                        print(pid_companyName_list_sum)
                        print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
                              self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
                              Unfolded_sum, '企业数量', pid_companyName_sum)
                    assert quantity_stop == (quantity_start - (Unfolded_sum - unfoldNum))

            else:
                if self.pages is None and self.way == "map_search_list" or self.pages is not None:
                    if quantity_stop < (quantity_start - (Unfolded_sum - unfoldNum) + quantity_rebate):
                        print(pid_companyName_list_sum)
                        print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
                              self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
                              Unfolded_sum, '企业数量', pid_companyName_sum)
                    assert quantity_stop >= (quantity_start - (Unfolded_sum - unfoldNum) + quantity_rebate)

                else:
                    if quantity_stop != (quantity_start - (Unfolded_sum - unfoldNum) + quantity_rebate):
                        print(pid_companyName_list_sum)
                        print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
                              self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
                              Unfolded_sum, '企业数量', pid_companyName_sum)
                    assert quantity_stop == (quantity_start - (Unfolded_sum - unfoldNum) + quantity_rebate)
        else:
            if quantity_start != quantity_stop:
                print(pid_companyName_list_sum)
                print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
                      self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
                      Unfolded_sum, '企业数量', pid_companyName_sum)
            assert quantity_start == quantity_stop


class Sync_robot(sync_config):

    def __init__(self, host, way, pages, canCover, dataColumns, numberCounts, headers=None, useQuota=True):
        super().__init__(host, way, pages, headers=headers, useQuota=useQuota)
        self.canCover = canCover
        self.dataColumns = dataColumns
        self.numberCounts = numberCounts
        print('Sync_robot初始化参数,canCover,{}, dataColumns,{}, numberCounts,{}'.
              format(canCover, dataColumns, numberCounts))

    # def __del__(self):
    #     class_name = self.__class__.__name__
    #     print(class_name)
    #     self.search_value_list()
    # 执行转机器人
    def sync(self, gatewayname=None, out_id=None, headers=None, pids=None, pages=None, seach_value=None, useQuota=True,
             dataColumns=None,
             phoneStatus=None,
             numberCount=0, needCallPlan=False, canCover=False, way=None, gatewayId=None, surveyId=None):
        if canCover is not False:
            canCover = self.canCover
        """

        :param gatewayname: 计划名称
        :param out_id: 计划ID
        :param headers: 用户信息
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
        true = True
        false = False
        if phoneStatus is None:
            phone = [0, 1, 2, 3]
        else:
            phone = phoneStatus
        if dataColumns is None:
            dataColumns = [0]
        if self.useQuota is not True:
            useQuota = self.useQuota
        elif useQuota is not True:
            useQuota = useQuota
        else:
            useQuota = True
        gatewayId = self.user_api.robot_gateway()["gatewayId"]
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
            "plan_name": gatewayname,
            "survey_id": surveyId,
            "gatewayId": gatewayId,
            "strategy": 1,
            "need_push": 1,
            "need_finish_message": true,
            "start_date": "2021-09-30 17:10:00",
            "need_hangup_message": false,
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
        if headers is None:
            header = self.user_api.headers_skb()
        else:
            header = headers
        if out_id is not None:
            payload.update({"payload": out_payload})
        if gatewayname is not None:
            payload.update({"payload": gatewayId_value})
        url = f'https://{self.user_api.skb_url_Host()}/api_skb/v1/{clues}/sync_robot'
        response = requests.post(url=url, headers=header, json=payload)
        return response

    # 查询号码管理内号码是否存在
    def robot_uncalled(self, query_name, queryType=2, created_at=None, phoneType=None, per_page=1000):
        """
         # 查询号码管理内号码是否存在
        :param per_page: 查询数量
        :param phoneType: 查询时号码类型筛选，1：固话，0：手机
        :param created_at:  时间过滤
        :param query_name: 查询内容，str型
        :param queryType:  查询字段，int型，1：姓名，2：公司名，3：号码,4:外呼计划编号
        :return:
        """
        url = f'https://{self.user_api.robot_url_Host()}/api/v1/customers/uncalled'
        headers = self.user_api.headers_robot()
        payload = {
            'page': 1,
            'per_page': per_page,
            'queryType': queryType,
            'query': query_name
        }
        if created_at is not None:
            payload.update({'created_at': created_at})
        if phoneType is not None:
            payload.update({'phoneType': phoneType})
        response = requests.get(url, params=payload, headers=headers)
        return response

    # if __name__ == '__main__':
    #

    # 查询转机器人前机器人内是否有该企业
    def sync_robot_start_verdicts(self, list_pid_company_name, search_payloads_values):
        # if Mobile is None:
        #     Mobile = []
        # if Fixed is None:
        #     Fixed = []
        resp_robot_verdicts_fixed = True
        resp_robot_verdicts_mobile = True
        list_sync_robot_filter_type1 = []  # 创建未转移的手机集合
        list_sync_robot_verdicts_type1 = []  # 创建手机转移结果集合
        list_sync_robot_repetition_type1 = []  # 创建手机重复转移结果集合

        list_sync_robot_filter_type2 = []  # 创建未转移的固话集合
        list_sync_robot_verdicts_type2 = []  # 创建固话转移结果集合
        list_sync_robot_repetition_type2 = []  # 创建固话重复转移结果集合
        # def select_resp_robot_com():
        #     resp_robot_com = self.robot_uncalled(query_name=company_name, queryType=2, phoneType=phone).json()
        #     # 查询企业是否转移到机器人
        #     if resp_robot_com["code"] != 0 and resp_robot_com["message"] != "操作成功":  # 判断查询接口是否成功
        #         print("机器人号码管理接口调用失败,企业为", company_name)
        #     elif not resp_robot_com['data']['list']:  # 判断转移的企业在机器人内是否存在
        #         if phone == 0:
        #             resp_robot_verdicts_mobile = False
        #         else:
        #             resp_robot_verdicts_fixed = False
        #     else:
        #         if phone == 0:
        #             for Mobile_type1 in resp_robot_com['data']['list']:
        #                 list_sync_robot_verdicts_type1.append(Mobile_type1["phone"])
        #             if resp_robot_com['data']['per_page'] == 1000:
        #                 select_resp_robot_com()
        #         else:
        #             for Mobile_type1 in resp_robot_com['data']['list']:
        #                 list_sync_robot_verdicts_type1.append(Mobile_type1["phone"])
        #             if resp_robot_com['data']['per_page'] == 1000:
        #                 select_resp_robot_com(company_name, phone)
        for phone in [0, 1]:
            resp_robot_com = self.robot_uncalled(query_name=list_pid_company_name["company_name"], queryType=2,
                                                 phoneType=phone).json()
            # 查询企业是否转移到机器人
            if resp_robot_com["code"] != 0:  # 判断查询接口是否成功
                print("机器人号码管理接口调用失败,企业为", list_pid_company_name)
            elif not resp_robot_com['data']['list']:  # 判断转移的企业在机器人内是否存在
                if phone == 0:
                    resp_robot_verdicts_mobile = False
                else:
                    resp_robot_verdicts_fixed = False
            else:
                if phone == 0:
                    for Mobile_type1 in resp_robot_com['data']['list']:
                        list_sync_robot_verdicts_type1.append(Mobile_type1["phone"])
                else:
                    for Fixed_type1 in resp_robot_com['data']['list']:
                        list_sync_robot_verdicts_type2.append(Fixed_type1["phone"])
        if resp_robot_verdicts_mobile is False and resp_robot_verdicts_fixed is False:
            resp_robot_verdicts = False
        elif resp_robot_verdicts_mobile is False and resp_robot_verdicts_fixed is True:
            resp_robot_verdicts = True
        elif resp_robot_verdicts_mobile is True and resp_robot_verdicts_fixed is False:
            resp_robot_verdicts = True
        else:
            resp_robot_verdicts = True

        unfoldStatistics_Api_value = self.unfoldStatistics_Api(
            search_payload=search_payloads_values, pid_list=[list_pid_company_name["pid"]]).json()
        if unfoldStatistics_Api_value["error_code"] != 0:
            print("查看状态查询失败", unfoldStatistics_Api_value)
            assert unfoldStatistics_Api_value["error_code"] == 0

        return {
            "unfoldNum": unfoldStatistics_Api_value["data"]["unfoldNum"],
            "resp_robot_verdicts": resp_robot_verdicts,
            "list_sync_robot_filter_type1": list_sync_robot_filter_type1,
            "list_sync_robot_verdicts_type1": list_sync_robot_verdicts_type1,
            "list_sync_robot_repetition_type1": list_sync_robot_repetition_type1,
            "list_sync_robot_filter_type2": list_sync_robot_filter_type2,
            "list_sync_robot_verdicts_type2": list_sync_robot_verdicts_type2,
            "list_sync_robot_repetition_type2": list_sync_robot_repetition_type2,
        }

    # 查询外呼计划
    def robot_outcallplan(self, gatewayId=None, gateway_HOT=None):
        """
         # 查询外呼计划
        :param gatewayId: 计划线路，str类型
        :return:
        """
        if self.host == 'lxcrm':
            gatewayId = self.user_api.robot_gateway()["gatewayId"]
        else:
            gatewayId = gatewayId
        if gateway_HOT == 'lxcrm':
            payload = {"page": 1, "per_page": 10, "gatewayId": gatewayId}
        else:
            payload = {"page": 1, "per_page": 10}
        url = f'https://{self.user_api.robot_url_Host()}/api/v1/plan/list'
        headers = self.user_api.headers_robot()
        response = requests.post(url, json=payload, headers=headers)
        return response

    # 查询转机器人后的转移结果
    def sync_robot_verdicts(self, Mobile=None, Fixed=None, company_name=None):

        if Mobile is None:
            Mobile = []
        if Fixed is None:
            Fixed = []
        resp_robot_verdicts = True  # 收集是否转移成功信息

        list_sync_robot_filter_type1 = []  # 创建未转移的手机集合
        list_sync_robot_verdicts_type1 = []  # 创建手机转移结果集合
        list_sync_robot_repetition_type1 = []  # 创建手机重复转移结果集合

        list_sync_robot_filter_type2 = []  # 创建未转移的固话集合
        list_sync_robot_verdicts_type2 = []  # 创建固话转移结果集合
        list_sync_robot_repetition_type2 = []  # 创建固话重复转移结果集合

        resp_robot_com = self.robot_uncalled(query_name=company_name, queryType=2).json()
        # 查询企业是否转移到机器人

        if resp_robot_com["code"] != 0 and resp_robot_com["message"] != "操作成功":  # 判断查询接口是否成功
            print("机器人号码管理接口调用失败,企业为", company_name)
        elif not resp_robot_com['data']['list']:  # 判断转移的企业在机器人内是否存在
            resp_robot_verdicts = False
        if Mobile:
            for Mobile_type1 in Mobile:
                resp_robot_type1 = self.robot_uncalled(query_name=Mobile_type1, queryType=3).json()
                if resp_robot_type1["code"] != 0:  # 判断查询接口是否成功
                    print("机器人号码管理接口调用失败,号码为", Mobile_type1)
                elif not resp_robot_type1['data']['list']:  # 判断转移的号码在机器人内是否存在
                    list_sync_robot_filter_type1.append(Mobile_type1)
                else:
                    repetition_mobile = False
                    for company_name_phone1 in resp_robot_type1['data']['list']:
                        if company_name_phone1["company_name"] == company_name:  # 判断查询的企业是所转移的企业
                            list_sync_robot_verdicts_type1.append(Mobile_type1)
                            repetition_mobile = True
                            break
                    if repetition_mobile is False:  # 判断查询的号码是重复号码
                        list_sync_robot_repetition_type1.append(Mobile_type1)

        if Fixed:
            for Fixed_type2 in Fixed:
                resp_robot_type2 = self.robot_uncalled(query_name=Fixed_type2, queryType=3).json()
                if resp_robot_type2["code"] != 0:  # 判断查询接口是否成功
                    print("机器人号码管理接口调用失败,号码为", Fixed_type2, "结果为", resp_robot_type2)
                elif not resp_robot_type2['data']['list']:  # 判断转移的号码在机器人内是否存在
                    list_sync_robot_filter_type2.append(Fixed_type2)
                else:
                    repetition_Fixed = False
                    for company_name_phone2 in resp_robot_type2['data']['list']:
                        if company_name_phone2["company_name"] == company_name:  # 判断查询的企业是所转移的企业
                            list_sync_robot_verdicts_type2.append(Fixed_type2)
                            repetition_Fixed = True
                            break
                    if repetition_Fixed is False:  # 判断查询的号码是重复号码
                        list_sync_robot_repetition_type2.append(Fixed_type2)
        return {
            "resp_robot_verdicts": resp_robot_verdicts,
            "list_sync_robot_filter_type1": list_sync_robot_filter_type1,
            "list_sync_robot_verdicts_type1": list_sync_robot_verdicts_type1,
            "list_sync_robot_repetition_type1": list_sync_robot_repetition_type1,
            "list_sync_robot_filter_type2": list_sync_robot_filter_type2,
            "list_sync_robot_verdicts_type2": list_sync_robot_verdicts_type2,
            "list_sync_robot_repetition_type2": list_sync_robot_repetition_type2,
        }

    # 转移方式，仅1条or全部
    def numberCount_verdicts(self, list_contact_all, list_contact_one, robot_stop_value,
                             list_robot_stop_canCover, list_sync_robot_filter, company_name_pid_list,
                             hasSmartSyncRobot):
        '''
        :param hasSmartSyncRobot: 企业状态是否灰测
        :param company_name_pid_list:  企业信息
        :param list_sync_robot_filter:  转移时被过滤的号码
        :param list_robot_stop_canCover:  转移时的重复号码
        :param numberCount: 转移方式，仅1条or全部
        :param list_contact_all: 企业全部手机号码
        :param robot_stop_value: 转移结束后，转移成功的号码
        :param list_contact_one: 企业的第一条号码
        :return:
        '''
        sync_robot_value_sum = 0
        if self.numberCounts == 1:
            if list_contact_one is not None:
                if len(robot_stop_value) == 0:
                    if list_contact_one in list_robot_stop_canCover:
                        print(company_name_pid_list, '\n转移仅一条出错,联系方式不为空但是转移失败,联系方式重复\n转移的号码为',
                              robot_stop_value, "重复的号码为", list_robot_stop_canCover)
                    elif list_contact_one in list_sync_robot_filter:
                        print(company_name_pid_list, '\n转移仅一条出错,联系方式不为空但是转移失败，联系方式被过滤\n转移的号码为',
                              robot_stop_value, "过滤的号码为", list_sync_robot_filter)
                    else:
                        print(company_name_pid_list, '\n转移仅一条出错,联系方式不为空但是转移失败\n转移的号码为',
                              robot_stop_value, "联系方式为", list_contact_one)
                    sync_robot_value_sum += self.sync_robot_failed_verdicts_assert(list_contact_Api=list_contact_all,
                                                                                   hasSmartSyncRobot=hasSmartSyncRobot)

                elif len(robot_stop_value) != 1:
                    print(company_name_pid_list, '\n转移仅一条出错,转移的联系方式超出1条联\n转移的号码为',
                          robot_stop_value)
            else:
                print(company_name_pid_list, '\n转移仅一条，联系方式为空')
        else:
            # robot_stop_canCover_value_list_sum = self.canCover_verdicts(
            #     robot_stop_canCover_value_list=robot_stop_canCover_value_list,
            #     robot_stop_value=robot_stop_value,
            #     list_contact_all=list_contact_all,
            #     company_name_pid_list=company_name_pid_list)
            if list_contact_one is not None:
                if len(robot_stop_value) == 0:
                    if set(list_contact_all).issubset(set(list_robot_stop_canCover)) is True:
                        print(company_name_pid_list, '\n转移全部出错成功转移为0,联系方式不为空但是转移失败,联系方式重复\n全部的号码为',
                              list_contact_all, "重复的号码为", list_robot_stop_canCover)
                    elif set(list_contact_all).issubset(set(list_sync_robot_filter)) is True:
                        print(company_name_pid_list, '\n转移全部出错成功转移为0,联系方式不为空但是转移失败，联系方式被过滤\n全部号码为',
                              list_contact_all, "过滤的号码为", list_sync_robot_filter)
                    else:
                        if len(list(set(list_contact_all).difference(set(list_robot_stop_canCover)))) != 0:
                            print(company_name_pid_list, '\n转移全部出错成功转移为0,部分联系方式重复，部分联系方式被过滤\n被过滤的号码为',
                                  list(set(list_contact_all).difference(set(list_robot_stop_canCover))), "全部联系方式为",
                                  list_contact_all)
                    sync_robot_value_sum += self.sync_robot_failed_verdicts_assert(list_contact_Api=list_contact_all,
                                                                                   hasSmartSyncRobot=hasSmartSyncRobot)
                elif len(robot_stop_value) != len(list_contact_all):
                    errro_value = list(set(list_contact_all).difference(set(robot_stop_value)))
                    if set(errro_value).issubset(set(list_robot_stop_canCover)) is True:
                        print(company_name_pid_list, '\n转移全部出错,联系方式不为空但是转移失败,联系方式重复\n全部的号码为',
                              errro_value, "重复的号码为", list_robot_stop_canCover)
                    elif set(errro_value).issubset(set(list_sync_robot_filter)) is True:
                        print(company_name_pid_list, '\n转移全部出错,联系方式不为空但是转移失败，联系方式被过滤\n全部号码为',
                              errro_value, "过滤的号码为", list_sync_robot_filter)
                    else:
                        if len(list(set(errro_value).difference(set(list_robot_stop_canCover)))) != 0:
                            print(company_name_pid_list, '\n转移全部出错,部分联系方式重复，部分联系方式被过滤\n被过滤的号码为',
                                  list(set(errro_value).difference(set(list_robot_stop_canCover))), "全部联系方式为",
                                  list_contact_all)
            else:
                print(company_name_pid_list, '\n转移全部，联系方式为空')
        return sync_robot_value_sum

    # 重复判断
    def canCover_verdicts(self, robot_stop_canCover_value_list, robot_stop_value, robot_all_value,
                          company_name_pid_list):
        if self.canCover is True:
            robot_stop_canCover_value_list_sum = 0
            if robot_stop_canCover_value_list:
                print(company_name_pid_list, '转移出错,重复的号码没有进行转移\n重复的号码为',
                      robot_stop_canCover_value_list, '\n条件，canCover',
                      self.canCover, 'way', self.way, 'page',
                      self.pages, 'dataColumns', self.dataColumns, 'numberCounts', self.numberCounts)
        else:
            robot_stop_canCover_value_list_sum = len(robot_stop_canCover_value_list)
            if (len(robot_stop_canCover_value_list) + len(robot_stop_value)) != len(robot_all_value):
                print(company_name_pid_list, '转移出错,重复的号码+转移的号码不等于全部号码\n重复的号码为',
                      robot_stop_canCover_value_list, '\n转移成功的的号码为', robot_stop_value, '\n全部号码数量为', robot_all_value,
                      '\n条件，canCover', '\n重复的号码为', robot_stop_canCover_value_list,
                      self.canCover, 'way', self.way, 'page',
                      self.pages, 'dataColumns', self.dataColumns, 'numberCounts', self.numberCounts)
        return robot_stop_canCover_value_list_sum

    #  转移结果判断
    def sync_robot_value_verdicts_assert(self, sync_robot_start_value, sync_robot_value,
                                         company_name_pid_list, list_contact_all, hasSmartSyncRobot):
        '''
        :param list_contact_all:
        :param sync_robot_start_value: 转机器人前查询企业是否在机器人内的结果{}
        :param sync_robot_value:  转机器人后的转移结果{}
        :param company_name_pid_list:  操作的企业pid和企业名，{}
        :param list_contact:  操作的企业的联系方式，{}
        :param hasSmartSyncRobot: 账户是否灰测
        :return:
        '''

        sync_robot_value_sum = 0
        if sync_robot_value["resp_robot_verdicts"] is True:  # 判断转移结果不为空
            if self.dataColumns == [0]:
                if sync_robot_value["list_sync_robot_verdicts_type2"]:
                    if sync_robot_start_value[company_name_pid_list["pid"]]["resp_robot_verdicts"] is True:
                        sync_robot_value_sum += 1
                    if sync_robot_start_value[company_name_pid_list["pid"]]["list_sync_robot_verdicts_type2"]:
                        robot_fixed_value = set(sync_robot_value["list_sync_robot_verdicts_type2"]).difference(
                            set(sync_robot_start_value[company_name_pid_list["pid"]]["list_sync_robot_verdicts_type2"]))
                        if len(list(robot_fixed_value)) != 0:
                            print(company_name_pid_list, '\n转移出错固话进行了转移,转移的固话为',
                                  list(robot_fixed_value), '\n条件，canCover', self.canCover, 'way', self.way, 'page',
                                  self.pages, 'dataColumns', self.dataColumns, 'numberCounts', self.numberCounts)
                    else:
                        print(company_name_pid_list, '\n转移出错固话进行了转移,转移的固话为',
                              sync_robot_value["list_sync_robot_verdicts_type2"], '\n条件，canCover', self.canCover, 'way',
                              self.way, 'page', self.pages, 'dataColumns', self.dataColumns, 'numberCounts',
                              self.numberCounts)
                sync_robot_value_sum += self.numberCount_verdicts(list_contact_all=list_contact_all["Mobile"],
                                                                  list_contact_one=list_contact_all["contacts_one"],
                                                                  robot_stop_value=sync_robot_value[
                                                                      "list_sync_robot_verdicts_type1"],
                                                                  list_robot_stop_canCover=sync_robot_value[
                                                                      "list_sync_robot_repetition_type1"],
                                                                  list_sync_robot_filter=sync_robot_value[
                                                                      "list_sync_robot_filter_type1"],
                                                                  company_name_pid_list=company_name_pid_list,
                                                                  hasSmartSyncRobot=hasSmartSyncRobot)

                # elif sync_robot_value["list_sync_robot_verdicts_type1"]:
                #     if sync_robot_start_value[company_name_pid_list["pid"]][
                #         "resp_robot_verdicts"] is True:  # 判断企业是否已被转移
                #         sync_robot_value_sum += 1
                #     if sync_robot_start_value[company_name_pid_list["pid"]]["list_sync_robot_verdicts_type1"]:
                #         robot_Mobile_value = list(set(sync_robot_value["list_sync_robot_verdicts_type1"]).difference(
                #             set(sync_robot_start_value[company_name_pid_list["pid"]][
                #                     "list_sync_robot_verdicts_type1"])))
                #     else:
                #         robot_Mobile_value = []
                # else:
                #     sync_robot_value_sum += self.sync_robot_failed_verdicts_assert(
                #         sync_robot_start_value=sync_robot_start_value, sync_robot_value=sync_robot_value,
                #         company_name_pid_list=company_name_pid_list, list_contact_Api=list_contact_all,
                #         hasSmartSyncRobot=hasSmartSyncRobot)
            else:
                list_contact_Api_all = list_contact_all["Mobile"] + list_contact_all["Fixed"]
                sync_robot_value_all = sync_robot_value["list_sync_robot_verdicts_type1"] + sync_robot_value[
                    "list_sync_robot_verdicts_type2"]
                sync_robot_value_can_all = sync_robot_value["list_sync_robot_repetition_type1"] + sync_robot_value[
                    "list_sync_robot_repetition_type2"]
                sync_robot_value_filter_all = sync_robot_value["list_sync_robot_filter_type1"] + sync_robot_value[
                    "list_sync_robot_filter_type2"]

                sync_robot_value_sum += self.numberCount_verdicts(list_contact_all=list_contact_Api_all,
                                                                  list_contact_one=list_contact_all["contacts_one"],
                                                                  robot_stop_value=sync_robot_value_all,
                                                                  list_robot_stop_canCover=sync_robot_value_can_all,
                                                                  list_sync_robot_filter=sync_robot_value_filter_all,
                                                                  company_name_pid_list=company_name_pid_list,
                                                                  hasSmartSyncRobot=hasSmartSyncRobot)
                # if sync_robot_value["list_sync_robot_verdicts_type1"] != [] and sync_robot_value[
                #     "list_sync_robot_verdicts_type2"] != []:
                #     if sync_robot_start_value[company_name_pid_list["pid"]]["resp_robot_verdicts"] is True:
                #         sync_robot_value_sum += 1
                #         robot_start_all_value = list(set(sync_robot_value["list_sync_robot_verdicts_type1"]).difference(
                #             set(sync_robot_start_value[company_name_pid_list["pid"]][
                #                     "list_sync_robot_verdicts_type1"]))) + list(
                #             set(sync_robot_value["list_sync_robot_verdicts_type2"]).difference(
                #                 set(sync_robot_start_value[company_name_pid_list["pid"]][
                #                         "list_sync_robot_verdicts_type2"])))
                #     else:
                #         robot_start_all_value = []
                #
                #
                #
                # elif sync_robot_value["list_sync_robot_verdicts_type1"]:
                #     if sync_robot_start_value[company_name_pid_list["pid"]]["list_sync_robot_verdicts_type1"]:
                #         sync_robot_value_sum += 1
                #         robot_start_Mobile_value = list(
                #             set(sync_robot_value["list_sync_robot_verdicts_type1"]).difference(
                #                 set(sync_robot_start_value[company_name_pid_list["pid"]][
                #                         "list_sync_robot_verdicts_type1"])))
                #     else:
                #         robot_start_Mobile_value = []
                #     self.numberCount_verdicts(list_contact_all=list_contact_all["Mobile"],
                #                               list_contact_one=list_contact_all["contacts_one"],
                #                               robot_stop_value=sync_robot_value["list_sync_robot_verdicts_type1"],
                #                               list_robot_stop_canCover=sync_robot_value[
                #                                   "list_sync_robot_repetition_type1"],
                #                               list_sync_robot_filter=sync_robot_value[
                #                                   "list_sync_robot_filter_type1"],
                #                               company_name_pid_list=company_name_pid_list)
                # elif sync_robot_value["list_sync_robot_verdicts_type2"]:
                #     if sync_robot_start_value[company_name_pid_list["pid"]]["list_sync_robot_verdicts_type2"]:
                #         sync_robot_value_sum += 1
                #         robot_fixed_value = list(set(sync_robot_value["list_sync_robot_verdicts_type2"]).difference(
                #             set(sync_robot_start_value[company_name_pid_list["pid"]][
                #                     "list_sync_robot_verdicts_type2"])))
                #     else:
                #         robot_fixed_value = []
                #     self.numberCount_verdicts(list_contact_all=list_contact_all["Fixed"],
                #                               list_contact_one=list_contact_all["contacts_one"],
                #                               robot_stop_value=sync_robot_value["list_sync_robot_verdicts_type2"],
                #                               list_robot_stop_canCover=sync_robot_value[
                #                                   "list_sync_robot_repetition_type2"],
                #                               list_sync_robot_filter=sync_robot_value[
                #                                   "list_sync_robot_filter_type2"],
                #                               company_name_pid_list=company_name_pid_list)
                # else:
                #     sync_robot_value_sum += self.sync_robot_failed_verdicts_assert(
                #         sync_robot_start_value=sync_robot_start_value, sync_robot_value=sync_robot_value,
                #         company_name_pid_list=company_name_pid_list, list_contact_Api=list_contact_all,
                #         hasSmartSyncRobot=hasSmartSyncRobot)
        else:
            sync_robot_value_sum += self.sync_robot_failed_verdicts_assert(list_contact_Api=list_contact_all,
                                                                           hasSmartSyncRobot=hasSmartSyncRobot)
        return sync_robot_value_sum

    #  未转移成功时的判断
    def sync_robot_failed_verdicts_assert(self, list_contact_Api,
                                          hasSmartSyncRobot):
        sync_robot_value_sum = 0
        if self.dataColumns == [0]:
            if not list_contact_Api["Mobile"]:
                if list_contact_Api["Fixed"] != [] or list_contact_Api["Qq"] != [] or list_contact_Api["Email"] != []:
                    if self.useQuota is True and list_contact_Api["unfoldNum"] is False and hasSmartSyncRobot is False:
                        sync_robot_value_sum += 1
        else:
            # if list_contact_Api["Mobile"] != [] or list_contact_Api["Fixed"] != []:
            #     list_contact_Api_all = list_contact_Api["Mobile"] + list_contact_Api["Fixed"]
            #     sync_robot_value_all = sync_robot_value["list_sync_robot_verdicts_type1"] + sync_robot_value[
            #         "list_sync_robot_verdicts_type2"]
            #     sync_robot_value_can_all = sync_robot_value["list_sync_robot_repetition_type1"] + sync_robot_value[
            #         "list_sync_robot_repetition_type2"]
            #     self.canCover_verdicts(
            #         robot_stop_canCover_value_list=sync_robot_value_can_all,
            #         robot_stop_value=sync_robot_value_all,
            #         robot_all_value=list_contact_Api_all,
            #         company_name_pid_list=company_name_pid_list)
            if list_contact_Api["Mobile"] == [] and list_contact_Api["Fixed"] == []:
                if list_contact_Api["Qq"] != [] or list_contact_Api["Email"] != []:
                    if self.useQuota is True and list_contact_Api["unfoldNum"] is False and hasSmartSyncRobot is False:
                        sync_robot_value_sum += 1
        return sync_robot_value_sum
