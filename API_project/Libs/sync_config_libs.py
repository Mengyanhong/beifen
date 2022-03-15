from pprint import pprint
import requests, json, time, pytest, os, random
from API_project.Configs.Config_Info import User_Config
from API_project.Configs.Config_Api import Config_api


# from API_project.Configs.shop_API import shop_api


# 转移操作通用Api
class sync_config(Config_api):
    def __init__(self, host, way, pages, headers_parameters=None, useQuota=True):
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
        super(sync_config, self).__init__(host=host, headers_parameters=headers_parameters)
        # self.search = Config_api(host, headers_parameters=headers)
        # self.shop_search = shop_api(host)
        # self.user_api = User_Config(host)
        self.way = way
        # self.header = headers
        self.useQuota = useQuota
        self.pages = pages

        print('sync_config初始化参数,host,{}, way,{}, pages,{}, headers,{}, useQuota,{}'.
              format(host, way, pages, headers_parameters, useQuota))

    # 转移前各维度搜索结果处理
    def search_value_list(self):
        # 搜索未查看，未转机器人的数据，有固话
        if self.way == 'search_list':
            response = self.skb_search()
            list_companyName_add = 'companyName'
        elif self.way == 'advanced_search_list':
            response = self.advanced_search()
            list_companyName_add = 'companyName'
        elif self.way == 'shop_search_list':
            response = self.search_shop()
            list_companyName_add = 'name'
        else:
            response = self.skb_address_search(contact=2)
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
            response = self.skb_search().json()
        elif self.way == 'advanced_search_list':
            response = self.advanced_search().json()
        elif self.way == 'shop_search_list':
            response = self.search_shop().json()
        else:
            response = self.skb_address_search(contact=2).json()
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

    # 联系方式获取
    def list_contact(self, pid, entName):
        list_contacts_value = self.skb_list_contact(pid=pid, entName=entName, module=self.way,
                                                    useQuota=self.useQuota)
        return list_contacts_value

    # 扣点判断
    def sync_robot_quantity_verdicts(self, quantity_start=None, quantity_stop=None, quantity_rebate=None,
                                     hasSmartSyncRobot=True, unfoldNum=0,
                                     pid_companyName_list_sum=None):
        pid_companyName_sum = len(pid_companyName_list_sum)
        if self.pages is None and self.way == "map_search_list":
            Unfolded_sum = 500
        elif self.pages is None:
            Unfolded_sum = pid_companyName_sum
        else:
            Unfolded_sum = self.pages
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
    def __init__(self, host, way, pages, canCover, dataColumns, numberCounts, headers_parameters=None, useQuota=True):
        super(Sync_robot, self).__init__(host=host, way=way, pages=pages, headers_parameters=headers_parameters, useQuota=useQuota)
        self.canCover = canCover
        self.dataColumns = dataColumns
        self.numberCounts = numberCounts
        print('Sync_robot初始化参数,canCover,{}, dataColumns,{}, numberCounts,{}'.
              format(canCover, dataColumns, numberCounts))

    # 查询转机器人前机器人内是否有该企业
    def sync_robot_start_verdicts(self, list_pid_company_name, search_payloads_values):

        resp_robot_verdicts_fixed = True
        resp_robot_verdicts_mobile = True
        list_sync_robot_filter_type1 = []  # 创建未转移的手机集合
        list_sync_robot_verdicts_type1 = []  # 创建手机转移结果集合
        list_sync_robot_repetition_type1 = []  # 创建手机重复转移结果集合

        list_sync_robot_filter_type2 = []  # 创建未转移的固话集合
        list_sync_robot_verdicts_type2 = []  # 创建固话转移结果集合
        list_sync_robot_repetition_type2 = []  # 创建固话重复转移结果集合

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
            search_payload=search_payloads_values, pid_list=[list_pid_company_name["pid"]], way=self.way).json()
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
                        self.canCover_verdicts(list_robot_stop_canCover=list_robot_stop_canCover,
                                               list_contact_one=list_contact_one, list_contact_all=list_contact_all,
                                               company_name_pid_list=company_name_pid_list)
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
            if list_contact_one is not None:
                if len(robot_stop_value) == 0:
                    if set(list_contact_all).issubset(set(list_robot_stop_canCover)) is True:
                        self.canCover_verdicts(list_robot_stop_canCover=list_robot_stop_canCover,
                                               list_contact_one=list_contact_one, list_contact_all=list_contact_all,
                                               company_name_pid_list=company_name_pid_list)
                    elif set(list_contact_all).issubset(set(list_sync_robot_filter)) is True:
                        print(company_name_pid_list, '\n转移全部出错成功转移为0,联系方式不为空但是转移失败，联系方式被过滤\n全部号码为',
                              list_contact_all, "过滤的号码为", list_sync_robot_filter)
                    else:
                        if len(list(set(list_contact_all).difference(set(list_robot_stop_canCover)))) != 0:
                            print(company_name_pid_list, '\n转移全部出错成功转移为0,部分联系方式重复，部分联系方式被过滤\n被过滤的号码为',
                                  list(set(list_contact_all).difference(set(list_robot_stop_canCover))), "全部联系方式为",
                                  list_contact_all)
                        if len(list(set(list_contact_all).difference(set(list_sync_robot_filter)))) != 0:
                            self.canCover_verdicts(list_robot_stop_canCover=list_robot_stop_canCover,
                                                   list_contact_one=list_contact_one,
                                                   list_contact_all=list(
                                                       set(list_contact_all).difference(set(list_sync_robot_filter))),
                                                   company_name_pid_list=company_name_pid_list)
                            # print(company_name_pid_list, '\n转移全部出错成功转移为0,部分联系方式重复，部分联系方式被过滤\n被过滤的号码为',
                            #       list(set(list_contact_all).difference(set(list_sync_robot_filter))), "全部联系方式为",
                            #       list_contact_all)

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
    def canCover_verdicts(self, list_robot_stop_canCover, list_contact_one, list_contact_all,
                          company_name_pid_list):
        if self.canCover is True:
            if self.numberCounts == 1:
                if list_contact_one in list_robot_stop_canCover:
                    print(company_name_pid_list, '\n转移仅一条出错,联系方式不为空选择重复数据仍然转移时，重复的号码没有转移成功\n转移的号码为',
                          list_contact_one, "重复的号码为", list_robot_stop_canCover)
                else:
                    print(company_name_pid_list, '\n转移仅一条出错,联系方式不为空选择重复数据仍然转移时，号码不是重复的但是没有转移成功\n转移的号码为',
                          list_contact_one, "重复的号码为", list_robot_stop_canCover)
            else:
                if set(list_contact_all).issubset(set(list_robot_stop_canCover)) is True:
                    print(company_name_pid_list, '\n转移全部号码出错,联系方式不为空选择重复数据仍然转移时，重复的号码没有转移成功\n转移成功的号码为',
                          list_contact_all, "重复的号码为", list_robot_stop_canCover)
                else:
                    print(company_name_pid_list, '\n转移全部号码出错,联系方式不为空选择重复数据仍然转移时，部分没有重复的号码没有转移成功\n转移成功的号码为',
                          set(list_contact_all).difference(set(list_robot_stop_canCover)), "重复的号码为",
                          list_robot_stop_canCover)
        else:
            if self.numberCounts == 1:
                if list_contact_one not in list_robot_stop_canCover:
                    print(company_name_pid_list, '\n转移仅一条出错,联系方式不为空选择重复数据不转移时，号码不重复但是没有转移成功\n转移的号码为',
                          list_contact_one, "重复的号码为", list_robot_stop_canCover)
            else:
                if set(list_contact_all).issubset(set(list_robot_stop_canCover)) is False:
                    print(company_name_pid_list, '\n转移仅全部号码出错,联系方式不为空选择重复数据不转移时，部分号码不重复但是没有转移成功\n没有转移的号码为',
                          set(list_contact_all).difference(set(list_robot_stop_canCover)), "重复的号码为",
                          list_robot_stop_canCover)

            # robot_stop_canCover_value_list_sum = len(robot_stop_canCover_value_list)
            # if (len(robot_stop_canCover_value_list) + len(robot_stop_value)) != len(robot_all_value):
            #     print(company_name_pid_list, '转移出错,重复的号码+转移的号码不等于全部号码\n重复的号码为',
            #           robot_stop_canCover_value_list, '\n转移成功的的号码为', robot_stop_value, '\n全部号码数量为', robot_all_value,
            #           '\n条件，canCover', '\n重复的号码为', robot_stop_canCover_value_list,
            #           self.canCover, 'way', self.way, 'page',
            #           self.pages, 'dataColumns', self.dataColumns, 'numberCounts', self.numberCounts)
        # return robot_stop_canCover_value_list_sum

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
                    # if sync_robot_start_value[company_name_pid_list["pid"]]["resp_robot_verdicts"] is True:
                    #     sync_robot_value_sum += 1
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
                                                                  list_contact_one=list_contact_all[
                                                                      "contacts_one_mobile"],
                                                                  robot_stop_value=sync_robot_value[
                                                                      "list_sync_robot_verdicts_type1"],
                                                                  list_robot_stop_canCover=sync_robot_value[
                                                                      "list_sync_robot_repetition_type1"],
                                                                  list_sync_robot_filter=sync_robot_value[
                                                                      "list_sync_robot_filter_type1"],
                                                                  company_name_pid_list=company_name_pid_list,
                                                                  hasSmartSyncRobot=hasSmartSyncRobot)
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
