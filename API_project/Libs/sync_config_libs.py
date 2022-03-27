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
        self.way = way
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
        if response_value['error_code'] == 10007:
            print("搜索结果为空", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['error_code'] == 0
        elif response_value["error_code"] != 0:
            print("搜索异常", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['error_code'] == 0
        elif response_value['data']['total'] == 0:
            print("搜索结果为空", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data']['total'] != 0
        elif response_value['data'] == {}:
            print("搜索结果为空", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data'] != {}
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
    def sync_robot_quantity_verdicts(self, quantity_start, quantity_stop,
                                     unfoldNum, pid_companyName_list_sum):
        '''
        扣点判断
        :param quantity_start: 初始额度
        :param quantity_stop: 转移结束后的额度
        :param unfoldNum: 已查看数量
        :param pid_companyName_list_sum: 企业列表
        :return:
        '''
        print("开始执行额度判断")
        pid_companyName_sum = len(pid_companyName_list_sum)
        if self.pages is None and self.way == "map_search_list":
            Unfolded_sum = 500
        elif self.pages is None:
            Unfolded_sum = pid_companyName_sum
        else:
            Unfolded_sum = self.pages
        if self.useQuota is True:
            if quantity_start <= (Unfolded_sum - unfoldNum):
                if quantity_stop != 0:
                    print(pid_companyName_list_sum)
                    print('初始额度', quantity_start, '结束时额度', quantity_stop, '页码',
                          self.pages, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
                          Unfolded_sum, '企业数量', pid_companyName_sum)
                assert quantity_stop == 0
            else:
                if quantity_stop != (quantity_start - (Unfolded_sum - unfoldNum)):
                    print(pid_companyName_list_sum)
                    print('初始额度', quantity_start, '结束时额度', quantity_stop, '页码',
                          self.pages, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
                          Unfolded_sum, '企业数量', pid_companyName_sum)
                assert quantity_stop == (quantity_start - (Unfolded_sum - unfoldNum))
            # if hasSmartSyncRobot is True:
            #     if quantity_start <= (Unfolded_sum - unfoldNum):
            #         if quantity_stop != 0:
            #             print(pid_companyName_list_sum)
            #             print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
            #                   self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
            #                   Unfolded_sum, '企业数量', pid_companyName_sum)
            #         assert quantity_stop == 0
            #     else:
            #         if quantity_stop != (quantity_start - (Unfolded_sum - unfoldNum)):
            #             print(pid_companyName_list_sum)
            #             print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
            #                   self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
            #                   Unfolded_sum, '企业数量', pid_companyName_sum)
            #         assert quantity_stop == (quantity_start - (Unfolded_sum - unfoldNum))

            # else:
            #     if self.pages is None and self.way == "map_search_list" or self.pages is not None:
            #         if quantity_stop < (quantity_start - (Unfolded_sum - unfoldNum) + quantity_rebate):
            #             print(pid_companyName_list_sum)
            #             print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
            #                   self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
            #                   Unfolded_sum, '企业数量', pid_companyName_sum)
            #         assert quantity_stop >= (quantity_start - (Unfolded_sum - unfoldNum) + quantity_rebate)
            #
            #     else:
            #         if quantity_stop != (quantity_start - (Unfolded_sum - unfoldNum) + quantity_rebate):
            #             print(pid_companyName_list_sum)
            #             print('初始额度', quantity_start, '结束时额度', quantity_stop, '未扣除的额度', quantity_rebate, '页码',
            #                   self.pages, '是否灰测', hasSmartSyncRobot, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
            #                   Unfolded_sum, '企业数量', pid_companyName_sum)
            #         assert quantity_stop == (quantity_start - (Unfolded_sum - unfoldNum) + quantity_rebate)
        else:
            if quantity_start != quantity_stop:
                print(pid_companyName_list_sum)
                print('初始额度', quantity_start, '结束时额度', quantity_stop, '页码',
                      self.pages, '扣点方式', self.useQuota, '已查看数量', unfoldNum, '转移数量',
                      Unfolded_sum, '企业数量', pid_companyName_sum)
            assert quantity_start == quantity_stop
        print("额度判断结束，测试结束")


class Sync_robot(sync_config):
    def __init__(self, host, way, pages, canCover, dataColumns, numberCounts, needCallPlan, headers_parameters=None,
                 useQuota=True):
        super(Sync_robot, self).__init__(host=host, way=way, pages=pages, headers_parameters=headers_parameters,
                                         useQuota=useQuota)
        self.canCover = canCover
        self.dataColumns = dataColumns
        self.numberCounts = numberCounts
        self.needCallPlan = needCallPlan
        print('Sync_robot初始化参数,canCover,{}, dataColumns,{}, numberCounts,{}，needCallPlan{}'.
              format(canCover, dataColumns, numberCounts, needCallPlan))

    # 机器人企业查询
    def find_phone(self, company_name, phone, page=1):
        find_phone_list = []
        resp_robot_cll_value = self.robot_uncalled(query_name=company_name, queryType=2, phoneType=phone,
                                                   page=page).json()
        assert resp_robot_cll_value["code"] == 0
        if resp_robot_cll_value['data']['list']:
            for Mobile_type1 in resp_robot_cll_value['data']['list']:
                find_phone_list.append(Mobile_type1["phone"])
            if resp_robot_cll_value['data']['hasNextPage'] is True:
                return find_phone_list + self.find_phone(company_name=company_name, phone=phone, page=(page + 1))
            else:
                return find_phone_list
        return find_phone_list

    # 机器人号码查询
    def find_robot_phone(self, Mobile, company_name):
        list_sync_robot_filter = []  # 创建未转移的手机集合
        list_sync_robot_verdicts = []  # 创建手机转移结果集合
        list_sync_robot_repetition = []  # 创建手机重复转移结果集合
        if Mobile:
            for Mobile_value in Mobile:
                time.sleep(0.2)
                Mobile_robot_value = self.robot_uncalled(query_name=Mobile_value, queryType=3).json()
                if Mobile_robot_value["code"] != 0:  # 判断查询接口是否成功
                    print("机器人号码管理接口调用失败,号码为", Mobile_value)
                elif not Mobile_robot_value['data']['list']:  # 判断转移的号码在机器人内是否存在
                    list_sync_robot_filter.append(Mobile_value)
                else:
                    repetition_mobile = False
                    for company_name_phone1 in Mobile_robot_value['data']['list']:
                        if company_name_phone1["company_name"] == company_name:  # 判断查询的企业是所转移的企业
                            list_sync_robot_verdicts.append(Mobile_value)
                            repetition_mobile = True
                            break
                    if repetition_mobile is False:  # 判断查询的号码是重复号码
                        list_sync_robot_repetition.append(Mobile_value)
        return {
            "list_sync_robot_filter": list_sync_robot_filter,
            "list_sync_robot_verdicts": list_sync_robot_verdicts,
            "list_sync_robot_repetition": list_sync_robot_repetition,
        }

    # 查询转机器人后的转移结果,速度快压力大
    def sync_robot_verdicts(self, Mobile, Fixed, company_name):
        list_sync_robot_filter_type1 = []  # 创建未转移的手机集合
        list_sync_robot_repetition_type1 = []  # 创建手机重复转移结果集合
        list_sync_robot_verdicts_type1 = []  # 创建手机转移结果集合
        list_sync_robot_verdicts_type2 = []  # 创建固话转移结果集合
        list_sync_robot_filter_type2 = []  # 创建未转移的固话集合
        list_sync_robot_repetition_type2 = []  # 创建固话重复转移结果集合
        start_time = time.time()
        if Mobile:
            phones_value = self.find_robot_phone(company_name=company_name, Mobile=Mobile)
            list_sync_robot_filter_type1.extend(phones_value["list_sync_robot_filter"])
            list_sync_robot_verdicts_type1.extend(phones_value["list_sync_robot_verdicts"])
            list_sync_robot_repetition_type1.extend(phones_value["list_sync_robot_repetition"])
        if Fixed:
            phones_value_fixed = self.find_robot_phone(company_name=company_name, Mobile=Fixed)
            list_sync_robot_filter_type2.extend(phones_value_fixed["list_sync_robot_filter"])
            list_sync_robot_verdicts_type2.extend(phones_value_fixed["list_sync_robot_verdicts"])
            list_sync_robot_repetition_type2.extend(phones_value_fixed["list_sync_robot_repetition"])
        end_time = time.time()
        if list_sync_robot_verdicts_type1 == [] and list_sync_robot_verdicts_type2 == []:
            resp_robot_verdicts = False  # 收集是否转移成功信息
        else:
            resp_robot_verdicts = True  # 收集是否转移成功信息
        print("获取转机器人结果号码查询耗时", end_time - start_time)
        return {
            "resp_robot_verdicts": resp_robot_verdicts,
            "list_sync_robot_filter_type1": list_sync_robot_filter_type1,
            "list_sync_robot_verdicts_type1": list_sync_robot_verdicts_type1,
            "list_sync_robot_repetition_type1": list_sync_robot_repetition_type1,
            "list_sync_robot_filter_type2": list_sync_robot_filter_type2,
            "list_sync_robot_verdicts_type2": list_sync_robot_verdicts_type2,
            "list_sync_robot_repetition_type2": list_sync_robot_repetition_type2,
        }

    # 查询转机器人后的转移结果,速度慢压力小
    def sync_robot_verdicts_tow(self, Mobile, Fixed, company_name):
        list_sync_robot_filter_type1 = []  # 创建未转移的手机集合
        list_sync_robot_repetition_type1 = []  # 创建手机重复转移结果集合
        list_sync_robot_verdicts_type1 = []  # 创建手机转移结果集合
        list_sync_robot_verdicts_type2 = []  # 创建固话转移结果集合
        list_sync_robot_filter_type2 = []  # 创建未转移的固话集合
        list_sync_robot_repetition_type2 = []  # 创建固话重复转移结果集合
        start_time = time.time()
        for phone_sum in [0, 1]:
            if phone_sum == 0:
                list_sync_robot_verdicts_type1.extend(list(set(self.find_phone(
                    company_name=company_name, phone=phone_sum)).intersection(set(Mobile))))
            else:
                list_sync_robot_verdicts_type2.extend(list(set(self.find_phone(
                    company_name=company_name, phone=phone_sum)).intersection(set(Mobile))))
        end_time = time.time()
        print("获取转机器人结果企业名查询耗时", end_time - start_time)
        start_time = time.time()
        mobile_list = list(set(Mobile).difference(set(list_sync_robot_verdicts_type1)))
        fixed_list = list(set(Fixed).difference(set(list_sync_robot_verdicts_type2)))
        end_time = time.time()
        print("获取转机器人结果集合耗时", end_time - start_time)
        start_time = time.time()
        if mobile_list:
            phones_value = self.find_robot_phone(company_name=company_name, Mobile=mobile_list)
            list_sync_robot_filter_type1.extend(phones_value["list_sync_robot_filter"])
            list_sync_robot_verdicts_type1.extend(phones_value["list_sync_robot_verdicts"])
            list_sync_robot_repetition_type1.extend(phones_value["list_sync_robot_repetition"])
        if fixed_list:
            phones_value_fixed = self.find_robot_phone(company_name=company_name, Mobile=fixed_list)
            list_sync_robot_filter_type2.extend(phones_value_fixed["list_sync_robot_filter"])
            list_sync_robot_verdicts_type2.extend(phones_value_fixed["list_sync_robot_verdicts"])
            list_sync_robot_repetition_type2.extend(phones_value_fixed["list_sync_robot_repetition"])
        end_time = time.time()
        if list_sync_robot_verdicts_type1 == [] and list_sync_robot_verdicts_type2 == []:
            resp_robot_verdicts = False  # 收集是否转移成功信息
        else:
            resp_robot_verdicts = True  # 收集是否转移成功信息
        print("获取转机器人结果号码查询耗时", end_time - start_time)
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
                             ):
        '''
        转移方式，仅1条or全部
        :param company_name_pid_list:  企业信息
        :param list_sync_robot_filter:  转移时被过滤的号码
        :param list_robot_stop_canCover:  转移时的重复号码
        :param list_contact_all: 企业全部手机号码
        :param robot_stop_value: 转移结束后，转移成功的号码
        :param list_contact_one: 企业的第一条号码
        :return:
        '''
        sync_robot_value_sum = 0
        if self.numberCounts == 1:
            if list_contact_one is not None:
                if not robot_stop_value:
                    if list_contact_one in list_robot_stop_canCover:
                        if self.canCover is True:
                            print(company_name_pid_list, '\n转移仅一条出错选择重复数据仍然转移时，重复的号码没有转移成功\n转移的号码为',
                                  list_contact_one, "重复的号码为", list_robot_stop_canCover)
                    elif list_contact_one in list_sync_robot_filter:
                        print(company_name_pid_list, '\n转移仅一条出错,联系方式不为空但是转移失败，联系方式被过滤\n转移的号码为',
                              robot_stop_value, "过滤的号码为", list_sync_robot_filter)
                    else:
                        print(company_name_pid_list, '\n转移仅一条出错,联系方式不为空但是转移失败\n转移的号码为',
                              robot_stop_value, "联系方式为", list_contact_one)
                elif len(robot_stop_value) != 1:
                    print(company_name_pid_list, '\n转移仅一条出错,转移的联系方式超出1条联\n转移的号码为',
                          robot_stop_value)
            else:
                print(company_name_pid_list, '\n转移仅一条，联系方式为空')
        else:
            if list_contact_one is not None:
                if not robot_stop_value:
                    if set(list_contact_all).issubset(set(list_robot_stop_canCover)) is True:
                        if self.canCover is True:
                            print(company_name_pid_list, '\n转移全部号码出错选择重复数据仍然转移时，重复的号码没有转移成功', '\n转移成功的号码为',
                                  list_contact_all, "\n重复的号码为", list_robot_stop_canCover)
                    elif set(list_contact_all).issubset(set(list_sync_robot_filter)) is True:
                        print(company_name_pid_list, '\n转移全部出错成功转移为0,联系方式不为空但是转移失败，联系方式被过滤\n全部号码为',
                              list_contact_all, "过滤的号码为", list_sync_robot_filter)
                    else:
                        filter_errro_value = list(set(list_contact_all).difference(set(list_robot_stop_canCover)))
                        canCover_errro_value = list(set(list_contact_all).difference(set(list_sync_robot_filter)))
                        if filter_errro_value:
                            print(company_name_pid_list, '\n转移全部出错成功转移为0,部分联系方式重复，部分联系方式被过滤\n被过滤的号码为',
                                  list(set(list_contact_all).difference(set(list_robot_stop_canCover))), "全部联系方式为",
                                  list_contact_all)
                        if canCover_errro_value:
                            if self.canCover is True:
                                print(company_name_pid_list, '\n转移全部号码出错选择重复数据仍然转移时，重复的号码没有转移成功', '\n转移成功的号码为',
                                      list_contact_all, "\n重复的号码为", canCover_errro_value)
                            else:
                                if set(canCover_errro_value).issubset(set(list_robot_stop_canCover)) is False:
                                    print(company_name_pid_list, '\n转移仅全部号码出错选择重复数据不转移时，部分号码不重复但是没有转移成功\n没有转移的号码为',
                                          set(canCover_errro_value).difference(set(list_robot_stop_canCover)),
                                          "\n重复的号码为",
                                          list_robot_stop_canCover)
                elif robot_stop_value != list_contact_all:
                    errro_value = list(set(list_contact_all).difference(set(robot_stop_value)))
                    if set(errro_value).issubset(set(list_robot_stop_canCover)) is True:
                        if self.canCover is True:
                            print(company_name_pid_list, '\n转移全部号码出错选择重复数据仍然转移时，重复的号码没有转移成功', '\n转移成功的号码为',
                                  robot_stop_value, "\n重复的号码为", errro_value)
                    elif set(errro_value).issubset(set(list_sync_robot_filter)) is True:
                        print(company_name_pid_list, '\n转移全部出错,联系方式不为空但是转移失败，部分联系方式被过滤\n全部号码为',
                              errro_value, "\n过滤的号码为", list_sync_robot_filter)
                    else:
                        filter_errro_value = list(set(errro_value).difference(set(list_robot_stop_canCover)))
                        canCover_errro_value = list(set(errro_value).difference(set(list_sync_robot_filter)))
                        if canCover_errro_value:
                            if self.canCover is True:
                                print(company_name_pid_list, '\n转移全部号码出错选择重复数据仍然转移时，重复的号码没有转移成功', '\n转移成功的号码为',
                                      list_contact_all, "\n重复的号码为", canCover_errro_value)
                            else:
                                if set(canCover_errro_value).issubset(set(list_robot_stop_canCover)) is False:
                                    print(company_name_pid_list, '\n转移仅全部号码出错选择重复数据不转移时，部分号码不重复但是没有转移成功\n没有转移的号码为',
                                          set(canCover_errro_value).difference(set(list_robot_stop_canCover)),
                                          "\n重复的号码为",
                                          canCover_errro_value)
                        if filter_errro_value:
                            print(company_name_pid_list, '\n转移全部出错,部分联系方式重复，部分联系方式被过滤\n被过滤的号码为',
                                  list(set(errro_value).difference(set(list_robot_stop_canCover))), "全部联系方式为",
                                  list_contact_all)
            else:
                print(company_name_pid_list, '\n转移全部，联系方式为空')
        return sync_robot_value_sum

    # 重复判断
    def canCover_verdicts(self, list_robot_stop_canCover, list_contact_one, list_contact_all,
                          company_name_pid_list):
        canCover = True
        if self.canCover is True:
            if self.numberCounts == 1:
                if list_contact_one in list_robot_stop_canCover:
                    # canCover = False
                    print(company_name_pid_list, '\n转移仅一条出错选择重复数据仍然转移时，重复的号码没有转移成功\n转移的号码为',
                          list_contact_one, "重复的号码为", list_robot_stop_canCover)
            else:
                if list_robot_stop_canCover:
                    # canCover = False
                    print(company_name_pid_list, '\n转移全部号码出错选择重复数据仍然转移时，重复的号码没有转移成功', '\n转移成功的号码为',
                          list_contact_all, "\n重复的号码为", list_robot_stop_canCover)
        else:
            if self.numberCounts == 1:
                if list_contact_one not in list_robot_stop_canCover:
                    print(company_name_pid_list, '\n转移仅一条出错选择重复数据不转移时，号码不重复但是没有转移成功\n转移的号码为',
                          list_contact_one, "重复的号码为", list_robot_stop_canCover)
            else:
                if set(list_contact_all).issubset(set(list_robot_stop_canCover)) is False:
                    print(company_name_pid_list, '\n转移仅全部号码出错选择重复数据不转移时，部分号码不重复但是没有转移成功\n没有转移的号码为',
                          set(list_contact_all).difference(set(list_robot_stop_canCover)), "\n重复的号码为",
                          list_robot_stop_canCover)
        # return canCover

    # 转移结果判断
    def sync_robot_value_verdicts_assert(self, sync_robot_value,
                                         company_name_pid_list, list_contact_all,
                                         ):
        '''
        转移结果判断
        :param list_contact_all:
        :param sync_robot_value:  转机器人后的转移结果{}
        :param company_name_pid_list:  操作的企业pid和企业名，{}
        :return:
        '''
        if sync_robot_value["resp_robot_verdicts"] is True:  # 判断转移结果不为空
            if self.dataColumns == [0]:
                if sync_robot_value["list_sync_robot_verdicts_type2"]:
                    print(company_name_pid_list, '\n转移出错固话进行了转移,转移的固话为',
                          sync_robot_value["list_sync_robot_verdicts_type2"], '\n条件，canCover', self.canCover, 'way',
                          self.way, 'page', self.pages, 'dataColumns', self.dataColumns, 'numberCounts',
                          self.numberCounts)
                # 判断转移方式，仅1条or全部
                self.numberCount_verdicts(list_contact_all=list_contact_all["Mobile"],
                                          list_contact_one=list_contact_all[
                                              "contacts_one_mobile"],
                                          robot_stop_value=sync_robot_value[
                                              "list_sync_robot_verdicts_type1"],
                                          list_robot_stop_canCover=sync_robot_value[
                                              "list_sync_robot_repetition_type1"],
                                          list_sync_robot_filter=sync_robot_value[
                                              "list_sync_robot_filter_type1"],
                                          company_name_pid_list=company_name_pid_list,
                                          )
            else:
                list_contact_Api_all = list_contact_all["Mobile"] + list_contact_all["Fixed"]
                sync_robot_value_all = sync_robot_value["list_sync_robot_verdicts_type1"] + sync_robot_value[
                    "list_sync_robot_verdicts_type2"]
                sync_robot_value_can_all = sync_robot_value["list_sync_robot_repetition_type1"] + sync_robot_value[
                    "list_sync_robot_repetition_type2"]
                sync_robot_value_filter_all = sync_robot_value["list_sync_robot_filter_type1"] + sync_robot_value[
                    "list_sync_robot_filter_type2"]
                # 判断转移方式，仅1条or全部
                self.numberCount_verdicts(list_contact_all=list_contact_Api_all,
                                          list_contact_one=list_contact_all["contacts_one"],
                                          robot_stop_value=sync_robot_value_all,
                                          list_robot_stop_canCover=sync_robot_value_can_all,
                                          list_sync_robot_filter=sync_robot_value_filter_all,
                                          company_name_pid_list=company_name_pid_list)
        return

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
            if list_contact_Api["Mobile"] == [] and list_contact_Api["Fixed"] == []:
                if list_contact_Api["Qq"] != [] or list_contact_Api["Email"] != []:
                    if self.useQuota is True and list_contact_Api["unfoldNum"] is False and hasSmartSyncRobot is False:
                        sync_robot_value_sum += 1
        return sync_robot_value_sum

    #  获取转移任务并执行任务判断
    def sync_robot_task_list(self, list_robot_filter_Mobile, list_robot_repetition_Mobile, list_robot_verdicts_Mobile,
                             list_robot_verdicts_Fixed, list_robot_filter_Fixed, list_robot_repetition_Fixed, out_id,
                             start_robot_sync_time, quantity_stop, quantity_start, search_response_body, pages,
                             out_callCount, resp_out_query_value_value):
        '''
        获取转移任务并执行任务判断
        :param resp_out_query_value_value: 转移结束后的外呼计划数量
        :param out_callCount: 外呼计划数量
        :param quantity_start: 转移前的额度
        :param quantity_stop: 转移后的额度
        :param start_robot_sync_time: 转机器人时间
        :param list_robot_filter_Mobile: 创建未转移的手机集合
        :param list_robot_repetition_Mobile:  创建手机重复转移结果集合
        :param list_robot_verdicts_Mobile: 创建手机转移结果集合
        :param list_robot_verdicts_Fixed: 创建固话转移结果集合
        :param list_robot_filter_Fixed: 创建未转移的固话集合
        :param list_robot_repetition_Fixed: 创建固话重复转移结果集合
        :return:
        '''
        task_list_value = self.task_list()["data"]["result"][0]
        # a = ['id', 'name', '', '', '', '']
        # createTime_num = int(task_list_value["createTime"]/1000)
        createTime = time.strftime("%Y-%m-%d-%H:%M", time.localtime(int(int(task_list_value["createTime"]) / 1000)))
        # start_robot_sync_times = time.strftime("%Y-%m-%d-%H:%M", time.localtime(int(start_robot_sync_time)))
        task_id_value = task_list_value["id"]
        print("开始判断任务记录，任务id{},任务开始时间{}".format(task_id_value, createTime))
        assert self.way == task_list_value["source"]
        assert start_robot_sync_time == createTime
        assert int(4) == int(task_list_value["status"])
        assert int(task_list_value["operationType"]) == int(1)
        assert int(quantity_start) == int(task_list_value["deductionCount"] + quantity_stop)
        if int(task_list_value["filteredNumbers"]) == 0 and int(task_list_value["importedNumbers"]) == 0:
            assert task_list_value["hasDetails"] is False
            # 判断外呼计划数量
        if self.needCallPlan is True:
            if out_id is None:
                assert int(task_list_value["filteredNumbers"]) == resp_out_query_value_value
            else:
                assert (out_callCount + int(task_list_value["filteredNumbers"])) == resp_out_query_value_value
        # if pages is None:
        #     print("过滤", task_list_value["filteredNumbers"])
        #     print(int(len(list_robot_filter_Mobile) + len(list_robot_repetition_Mobile) + len(
        #         list_robot_repetition_Fixed) + len(list_robot_filter_Fixed)))
        #     print("转移", task_list_value["importedNumbers"])
        #     print(int(len(list_robot_verdicts_Mobile) + len(list_robot_verdicts_Fixed)))

        # searchCondition = json.loads(task_list_value["searchCondition"])["filter"]
        # assert search_response_body == searchCondition
        if task_list_value["hasDetails"] is True:
            if self.task_contact_list(taskId=task_id_value)["data"]["count"] != \
                    task_list_value["filteredNumbers"] + task_list_value["importedNumbers"]:
                print("转移出错，任务记录内的转移数量和任务详情的数量不一致，任务id{}".format(task_id_value))
            else:
                task_contact_Mobile_sum = self.task_contact_list(taskId=task_id_value, contactType=1)["data"][
                    "count"]
                task_contact_Fixed_sum = self.task_contact_list(taskId=task_id_value, contactType=2)["data"]["count"]
                list_robot_all_Mobile_sum = len(list_robot_filter_Mobile) + len(list_robot_repetition_Mobile) + len(
                    list_robot_verdicts_Mobile)
                list_robot_all_Fixed_sum = len(list_robot_verdicts_Fixed) + len(list_robot_filter_Fixed) + len(
                    list_robot_repetition_Fixed)
                if pages is None:
                    if task_contact_Mobile_sum != list_robot_all_Mobile_sum:
                        print("转移出错，实际转移的手机的数量和任务详情手机的数量不一致，任务id{},详情内数量{}，企业内的数量{}".
                              format(task_id_value, task_contact_Mobile_sum, list_robot_all_Mobile_sum))
                    if task_contact_Fixed_sum != list_robot_all_Fixed_sum:
                        print("转移出错，实际转移的固话的数量和任务详情固话的数量不一致，任务id{},详情内数量{}，企业内的数量{}".
                              format(task_id_value, task_contact_Mobile_sum, list_robot_all_Mobile_sum))
                else:
                    if task_contact_Mobile_sum > list_robot_all_Mobile_sum:
                        print("转移出错，任务详情手机的数量没有大于抽样转移的手机的数量，任务id{},详情内数量{}，企业内的数量{}".
                              format(task_id_value, task_contact_Mobile_sum, list_robot_all_Mobile_sum))
                    if task_contact_Fixed_sum > list_robot_all_Fixed_sum:
                        print("转移出错，任务详情固话的数量没有大于抽样转移的固话的数量，任务id{},详情内数量{}，企业内的数量{}".
                              format(task_id_value, task_contact_Mobile_sum, list_robot_all_Mobile_sum))
            if self.task_contact_list(taskId=task_id_value, success=False)["data"]["count"] != \
                    task_list_value["filteredNumbers"]:
                print("转移出错，任务记录内的转移失败的数量和任务详情转移失败的数量不一致，任务id{}".format(task_id_value))
            else:
                task_contact_Mobile_sum = self.task_contact_list(taskId=task_id_value, success=False,
                                                                 contactType=1)["data"]["count"]
                task_contact_Fixed_sum = self.task_contact_list(taskId=task_id_value, success=False,
                                                                contactType=2)["data"]["count"]
                list_robot_all_Mobile_sum = len(list_robot_filter_Mobile) + len(list_robot_repetition_Mobile)
                list_robot_all_Fixed_sum = len(list_robot_repetition_Fixed) + len(list_robot_filter_Fixed)
                if pages is None:
                    if task_contact_Mobile_sum != list_robot_all_Mobile_sum:
                        print("转移出错，实际转移的手机的失败数量和任务详情手机的失败数量不一致，任务id{},详情内数量{}，企业内的数量{}".
                              format(task_id_value, task_contact_Mobile_sum, list_robot_all_Mobile_sum))
                    if task_contact_Fixed_sum != list_robot_all_Fixed_sum:
                        print("转移出错，实际转移的固话的失败数量和任务详情固话失败的数量不一致，任务id{},详情内数量{}，企业内的数量{}".
                              format(task_id_value, task_contact_Mobile_sum, list_robot_all_Mobile_sum))
                else:
                    if task_contact_Mobile_sum >= list_robot_all_Mobile_sum:
                        print("转移出错，实际转移的手机的失败数量和任务详情手机的失败数量有误，任务id{},详情内数量{}，企业内的数量{}".
                              format(task_id_value, task_contact_Mobile_sum, list_robot_all_Mobile_sum))
                    if task_contact_Fixed_sum >= list_robot_all_Fixed_sum:
                        print("转移出错，实际转移的固话的失败数量和任务详情固话失败的数量有误，任务id{},详情内数量{}，企业内的数量{}".
                              format(task_id_value, task_contact_Mobile_sum, list_robot_all_Mobile_sum))
            if self.task_contact_list(taskId=task_id_value, success=True)["data"]["count"] != \
                    task_list_value["importedNumbers"]:
                print("转移出错，任务记录内的转移成功的数量和任务详情转移成功的数量不一致，任务id{}".format(task_id_value))
            else:
                task_contact_Mobile_sum = self.task_contact_list(taskId=task_id_value, success=True,
                                                                 contactType=1)["data"]["count"]
                task_contact_Fixed_sum = self.task_contact_list(taskId=task_id_value, success=True,
                                                                contactType=2)["data"]["count"]
                list_robot_all_Mobile_sum = len(list_robot_verdicts_Mobile)
                list_robot_all_Fixed_sum = len(list_robot_verdicts_Fixed)
                if pages is None:
                    if task_contact_Mobile_sum != list_robot_all_Mobile_sum:
                        print("转移出错，实际转移的手机的成功数量和任务详情手机的成功数量不一致，任务id{}".format(task_id_value))
                    if task_contact_Fixed_sum != list_robot_all_Fixed_sum:
                        print("转移出错，实际转移的固话的成功数量和任务详情固话成功的数量不一致，任务id{}".format(task_id_value))
                else:
                    if task_contact_Mobile_sum > list_robot_all_Mobile_sum:
                        print("转移出错，实际转移的手机的成功数量和任务详情手机的成功数量出错，任务id{}".format(task_id_value))
                    if task_contact_Fixed_sum > list_robot_all_Fixed_sum:
                        print("转移出错，实际转移的固话的成功数量和任务详情固话成功的数量出错，任务id{}".format(task_id_value))

    #  获取自动转移任务并执行任务判断
    def sync_robot_automation_task_list(self, start_robot_sync_time, search_response_body=None):
        '''
        获取自动转移任务并执行任务判断
        :param search_response_body: 转移参数
        :param start_robot_sync_time: 转机器人时间
        :return:
        '''
        task_list_value = self.task_list()["data"]["result"][0]
        createTime = time.strftime("%Y-%m-%d-%H:%M", time.localtime(int(int(task_list_value["createTime"]) / 1000)))
        task_id_value = task_list_value["id"]
        print("开始判断任务记录，任务id{},任务开始时间{}".format(task_id_value, createTime))
        assert self.way == task_list_value["source"]
        assert start_robot_sync_time == createTime
        assert int(0) == int(task_list_value["status"])
        assert int(task_list_value["operationType"]) == int(2)
        assert int(task_list_value["filteredNumbers"]) == 0
        assert int(task_list_value["importedNumbers"]) == 0
        assert task_list_value["hasDetails"] is False
        assert task_list_value["deductionCount"] == 0

        # searchCondition = json.loads(task_list_value["searchCondition"])["filter"]
        # assert search_response_body == searchCondition
        # 暂停任务
        self.suspend_task(taskId=task_id_value)
        suspend_task_value = self.task_list()["data"]["result"]
        suspend_task_value_id_value = False
        for suspend_task_value_id in suspend_task_value:
            if suspend_task_value_id["id"] == task_id_value:
                suspend_task_value_id_value = True
                if suspend_task_value_id["status"] != 2:
                    print("任务暂停失败,任务id{}".format(task_id_value))
                    assert suspend_task_value_id["status"] == 2
                break
        assert suspend_task_value_id_value is True
        # 开始任务
        self.run_task(taskId=task_id_value)
        run_task_value = self.task_list()["data"]["result"]
        run_task_value_id_value = False
        for run_task_value_id in run_task_value:
            if run_task_value_id["id"] == task_id_value:
                run_task_value_id_value = True
                if run_task_value_id["status"] != 0:
                    print("任务启动失败,任务id{}".format(task_id_value))
                    assert run_task_value_id["status"] == 0
                break
        assert run_task_value_id_value is True
        # 停止任务
        self.stop_task(taskId=task_id_value)
        stop_task_value = self.task_list()["data"]["result"]
        stop_task_value_id_value = False
        for stop_task_value_id in stop_task_value:
            if stop_task_value_id["id"] == task_id_value:
                stop_task_value_id_value = True
                if stop_task_value_id["status"] != 3:
                    print("任务停止失败,任务id{}".format(task_id_value))
                    assert stop_task_value_id["status"] == 3
                break
        assert stop_task_value_id_value is True
        # 删除任务
        self.delete_task(taskId=task_id_value)
        delete_task_value = self.task_list()["data"]["result"]
        delete_task_value_id_value = False
        for delete_task_value_id in delete_task_value:
            if delete_task_value_id["id"] == task_id_value:
                delete_task_value_id_value = True
                print("任务删除失败,任务id{}".format(task_id_value))
                assert delete_task_value_id["id"] != task_id_value
                break
        assert delete_task_value_id_value is False

    def sync_Unfold(self, oid, sync_robot_value, ES_search_value, i, list_contact_Api):
        if self.host == "lxcrm":
            transferredRobotOrgs = "transferredRobotOrgs"
            unfoldedOrgs = "unfoldedOrgs"
        else:
            unfoldedOrgs = "unfoldedOrgsNonProd"
            transferredRobotOrgs = "transferredRobotOrgsNonProd"
        if sync_robot_value is True:
            if str(oid) not in ES_search_value[transferredRobotOrgs] or \
                    transferredRobotOrgs not in ES_search_value.keys():
                print('{}\n转移状态有误，企业转移成功但是转移状态为未转'.format(i))
                # assert str(oid) in ES_search_value[
                #     transferredRobotOrgs] and transferredRobotOrgs in ES_search_value.keys()
            if "hasContact" in ES_search_value.keys() and ES_search_value["hasContact"] is True:
                if unfoldedOrgs not in ES_search_value.keys() or str(oid) not in ES_search_value[unfoldedOrgs]:
                    print('{}查看状态有误, 企业转移成功但是查看状态为未查看'.format(i))
                    # assert str(oid) in ES_search_value[
                    #     unfoldedOrgs] and unfoldedOrgs in ES_search_value.keys()
            else:
                print('{}转移有误, 企业转移成功但是企业无联系方式'.format(i))
        else:
            if transferredRobotOrgs in ES_search_value.keys() and str(oid) in ES_search_value[transferredRobotOrgs]:
                print('{}\n转移状态有误，企业转移失败但是转移状态为未已转机器人'.format(i))
                # assert transferredRobotOrgs not in ES_search_value.keys() or str(oid) not in ES_search_value[
                #     transferredRobotOrgs]
            if self.dataColumns == [0]:
                if not list_contact_Api["Mobile"]:
                    if list_contact_Api["Fixed"] != [] or list_contact_Api["Qq"] != [] or \
                            list_contact_Api["Email"] != []:
                        if self.useQuota is False and list_contact_Api["unfoldNum"] is False:
                            if unfoldedOrgs in ES_search_value.keys() and str(oid) in ES_search_value[unfoldedOrgs]:
                                print('{}查看状态有误，转移时选择不扣点但是查看状态为已查看'.format(i))
                                # assert str(oid) not in ES_search_value[unfoldedOrgs]
                        else:
                            if str(oid) not in ES_search_value[unfoldedOrgs]:
                                print('{}查看状态有误，转移时选择扣点但是查看状态为未查看'.format(i))
                            # assert str(oid) in ES_search_value[unfoldedOrgs]
                    else:
                        if "hasContact" in ES_search_value.keys() and ES_search_value["hasContact"] is True:
                            print('{}联系方式有误'.format(i))
                        assert "hasContact" not in ES_search_value.keys() or ES_search_value["hasContact"] is False

            else:
                if list_contact_Api["Mobile"] == [] and list_contact_Api["Fixed"] == []:
                    if list_contact_Api["Qq"] != [] or list_contact_Api["Email"] != []:
                        if self.useQuota is False and list_contact_Api["unfoldNum"] is False:
                            if unfoldedOrgs in ES_search_value.keys() and str(oid) in ES_search_value[unfoldedOrgs]:
                                print('{}查看状态有误，转移时选择不扣点但是查看状态为已查看'.format(i))
                                # assert str(oid) not in ES_search_value[unfoldedOrgs]
                        else:
                            if str(oid) not in ES_search_value[unfoldedOrgs]:
                                print('{}查看状态有误，转移时选择扣点但是查看状态为未查看'.format(i))
                            # assert str(oid) in ES_search_value[unfoldedOrgs]
                    else:
                        if "hasContact" in ES_search_value.keys() and ES_search_value["hasContact"] is True:
                            print('{}联系方式有误'.format(i))
                        assert "hasContact" not in ES_search_value.keys() or ES_search_value["hasContact"] is False
