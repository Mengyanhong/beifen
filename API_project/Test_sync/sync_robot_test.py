# @Time : 2021/9/9 17:31
# @Author : 孟艳红
# @File : sync_robot_test.py
# from pprint import pprint
import requests, json, time, pytest, os, random
from API_project.Libs.sync_config_libs import Sync_robot

# from API_project.Configs.Config_Info import User_Config

test_host = "staging"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境


class Test_sync_robot:
    # @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', 'map_search_list' , 'shop_search_list'])
    # @pytest.mark.parametrize('page', [None, 500, 1000, 2000])
    # 扣除流量额度，仅转移手机or手机+固话，全部号码or仅一条号码, 加入已有外呼计划
    @pytest.mark.parametrize('way', ['advanced_search_list'])
    # 转移号码数量
    @pytest.mark.parametrize('page', [None])
    # 转移号码类型
    @pytest.mark.parametrize('dataColumns', [[0], [0, 1]])
    # 转移号码方式
    @pytest.mark.parametrize('numberCounts', [0, 1])
    # 重复是否转移
    @pytest.mark.parametrize('canCover', [True])
    # 是否创建外呼计划方式
    @pytest.mark.parametrize('needCallPlan', [True])
    # 是否扣点
    @pytest.mark.parametrize('useQuota', [True])
    def test_sync_robot(self, way, page, dataColumns, numberCounts, canCover, needCallPlan, useQuota, ES):
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        sync_config_Api = Sync_robot(host=test_host, way=way, useQuota=useQuota, pages=page, canCover=canCover,
                                     dataColumns=dataColumns, needCallPlan=needCallPlan,
                                     numberCounts=numberCounts,
                                     )
        userinfo = sync_config_Api.userinfo_skb_Api().json()
        quantity_start = userinfo['data']['uRemainQuota']  # 获取初始额度
        oid = userinfo['data']['oid']  # 获取账户类型是否灰测
        # 执行搜索
        search_values = sync_config_Api.search_value_list()
        assert search_values["pid_list"] != []
        if page is None and way == "map_search_list":
            pid = None
            pages = 500
        elif page is None:
            pid = search_values["pid_list"]
            pages = None
        else:
            pid = None
            pages = page
        if needCallPlan is True:
            resp_out_sync = sync_config_Api.robot_out_call_plan().json()["data"]["list"]  # 获取外呼计划列表
            if resp_out_sync:
                resp_out_sync = resp_out_sync[0]
                out_ids = resp_out_sync["id"]
                out_gatewayId = resp_out_sync["gatewayId"]
                out_surveyId = resp_out_sync["surveyId"]
                out_callCount = resp_out_sync["callCount"]
                out_id = random.choices([out_ids, None])[0]
                if out_id is None:
                    out_jobGroupName = "外呼测试" + time.strftime("%Y年%m月%d日%H时%M分")
                else:
                    out_jobGroupName = resp_out_sync["jobGroupName"]
                # print(resp_out_sync)
                # print("外呼计划id", out_id)
            else:
                print("需要创建外呼计划，但是外呼计划列表为空", resp_out_sync)
                out_id = None
                out_gatewayId = None
                out_surveyId = None
                out_jobGroupName = None
                out_callCount = None
        else:
            out_id = None
            out_gatewayId = None
            out_surveyId = None
            out_jobGroupName = None
            out_callCount = None

        # 获取转移数据的查看状态
        unfoldStatistics_Api_value = sync_config_Api.unfoldStatistics_Api(
            search_payload=search_values["payloads_request"], pid_list=pid, page=pages, way=way).json()
        if unfoldStatistics_Api_value["error_code"] == 0:
            unfoldNum = unfoldStatistics_Api_value["data"]["unfoldNum"]
            # print("查看状态查询", unfoldStatistics_Api_value)
        else:
            unfoldNum = 0
            print("查看状态查询失败", unfoldStatistics_Api_value)

        # 执行转移操作
        resp_sync = sync_config_Api.robot_sync(pids=pid, pages=pages,
                                               seach_value=search_values["payloads_request"], canCover=canCover,
                                               way=way, out_id=out_id, needCallPlan=needCallPlan,
                                               dataColumns=dataColumns,
                                               numberCount=numberCounts, gatewayId=out_gatewayId, surveyId=out_surveyId,
                                               gateway_name=out_jobGroupName, useQuota=useQuota).json()
        start_robot_sync_time = time.strftime("%Y-%m-%d-%H:%M", time.localtime())
        # syn_response_body = json.loads(resp_syn.request.body.decode("unicode_escape"))
        # print(resp_syn.request.url)
        # print(resp_syn.request.headers)
        # resp_sync = resp_syn.json()
        # resp_syn.close()
        if resp_sync['error_code'] == 0:
            start_time = time.time()
            sync_config_Api.search_elapsed_time()
            end_time = time.time()
            print("转移耗时", end_time - start_time)
            quantity_stop = sync_config_Api.userinfo_skb_Api().json()['data']['uRemainQuota']
            list_robot_filter_Mobile = []  # 创建未转移的手机集合
            list_robot_repetition_Mobile = []  # 创建手机重复转移结果集合
            list_robot_verdicts_Mobile = []  # 创建手机转移结果集合
            list_robot_verdicts_Fixed = []  # 创建固话转移结果集合
            list_robot_filter_Fixed = []  # 创建未转移的固话集合
            list_robot_repetition_Fixed = []  # 创建固话重复转移结果集合
            for i in search_values["pid_companyName_list"]:
                # 获取联系方式
                list_contact_Api = sync_config_Api.list_contact(pid=i['pid'], entName=i['company_name'])
                # 获取转机器人结果
                start_time = time.time()
                sync_robot_value = sync_config_Api.sync_robot_verdicts_tow(Mobile=list_contact_Api["Mobile"],
                                                                           Fixed=list_contact_Api["Fixed"],
                                                                           company_name=i['company_name'])
                end_time = time.time()
                print("获取转机器人结果耗时", end_time - start_time)
                list_robot_filter_Mobile.extend(sync_robot_value["list_sync_robot_filter_type1"])
                list_robot_repetition_Mobile.extend(sync_robot_value["list_sync_robot_repetition_type1"])
                list_robot_verdicts_Mobile.extend(sync_robot_value["list_sync_robot_verdicts_type1"])
                list_robot_verdicts_Fixed.extend(sync_robot_value["list_sync_robot_verdicts_type2"])
                list_robot_filter_Fixed.extend(sync_robot_value["list_sync_robot_filter_type2"])
                list_robot_repetition_Fixed.extend(sync_robot_value["list_sync_robot_repetition_type2"])

                ES_search_value = ES.get(index="company_info_prod", id=i['pid'])['_source']
                # 执行转移筛选查看筛选判断
                sync_config_Api.sync_Unfold(oid=oid, sync_robot_value=sync_robot_value["resp_robot_verdicts"],
                                            ES_search_value=ES_search_value, i=i, list_contact_Api=list_contact_Api)
                start_time = time.time()
                # 执行转移判断
                sync_config_Api.sync_robot_value_verdicts_assert(
                    # sync_robot_start_value=sync_robot_start_verdicts_dicde,
                    sync_robot_value=sync_robot_value,
                    company_name_pid_list=i,
                    list_contact_all=list_contact_Api,
                )
                end_time = time.time()
                print("执行转移判断耗时", end_time - start_time)
            # task_list_value = sync_config_Api.task_list()["data"]["result"][0]

            resp_out_query_value_callCount = 0
            #  外呼计划测试
            if needCallPlan is True:
                resp_out_query = sync_config_Api.robot_out_call_plan(gateway_Id=out_gatewayId).json()["data"][
                    "list"]  # 获取外呼计划列表
                # print("获取外呼计划列表", resp_out_query)
                resp_out_query_value_value = False
                for resp_out_query_value in resp_out_query:
                    if out_id is None:
                        if resp_out_query_value["jobGroupName"] == str(out_jobGroupName):
                            # print("创建外呼计划{}".format(out_jobGroupName))
                            resp_out_query_value_callCount = resp_out_query_value["callCount"]
                            resp_out_query_value_value = True
                            if pages is None:
                                assert resp_out_query_value["callCount"] == (
                                        len(list_robot_verdicts_Mobile) + len(list_robot_verdicts_Fixed))
                            else:
                                assert resp_out_query_value["callCount"] > (
                                        len(list_robot_verdicts_Mobile) + len(list_robot_verdicts_Fixed))
                            break
                        # assert out_jobGroupName in resp_out_query_value.values()
                    else:
                        if str(resp_out_query_value["id"]) == str(out_id):
                            resp_out_query_value_callCount = resp_out_query_value["callCount"]
                            resp_out_query_value_value = True
                            # print("加入外呼计划加入前{}，加入后{}".format(out_callCount, resp_out_query_value["callCount"]))
                            assert out_jobGroupName == resp_out_query_value["jobGroupName"]
                            assert out_gatewayId == resp_out_query_value["gatewayId"]
                            assert out_surveyId == resp_out_query_value["surveyId"]
                            assert resp_out_query_value["jobGroupName"] == out_jobGroupName
                            if resp_out_query_value["callCount"] < (len(list_robot_verdicts_Mobile) + len(
                                    list_robot_verdicts_Fixed) + out_callCount):
                                print("加入外呼计划失败加入前{}，加入后{},计划名称为{}，外呼计划ID为{}".format(out_callCount,
                                                                                     resp_out_query_value["callCount"],
                                                                                     out_jobGroupName, out_id))
                                # if pages is None:
                                #     if resp_out_query_value["callCount"] != (len(list_robot_verdicts_Mobile) + len(
                                #             list_robot_verdicts_Fixed) + out_callCount):
                                #         print("加入外呼计划失败加入前{}，加入后{}".format(out_callCount, resp_out_query_value["callCount"]))
                                #         # assert resp_out_query_value["callCount"] == (len(list_robot_verdicts_Mobile) + len(
                                #         #     list_robot_verdicts_Fixed) + out_callCount)
                                # else:
                                #     if resp_out_query_value["callCount"] < (len(list_robot_verdicts_Mobile) + len(
                                #             list_robot_verdicts_Fixed) + out_callCount):
                                #         print("加入外呼计划失败加入前{}，加入后{}".format(out_callCount, resp_out_query_value["callCount"]))
                                #         # assert resp_out_query_value["callCount"] > (len(list_robot_verdicts_Mobile) + len(
                                #         #     list_robot_verdicts_Fixed) + out_callCount)
                            break
                if out_id is None:
                    if resp_out_query_value_value is False:
                        print("创建外呼计划失败,计划名称为{}".format(out_jobGroupName))
                else:
                    if resp_out_query_value_value is False:
                        print("加入外呼计划失败,计划名称为{}，外呼计划ID为{}".format(out_jobGroupName, out_id))
                        # assert resp_out_query_value_value is True
            #  转机器人任务记录判断
            sync_config_Api.sync_robot_task_list(list_robot_filter_Mobile=list_robot_filter_Mobile,
                                                 list_robot_repetition_Mobile=list_robot_repetition_Mobile,
                                                 list_robot_verdicts_Mobile=list_robot_verdicts_Mobile,
                                                 list_robot_verdicts_Fixed=list_robot_verdicts_Fixed,
                                                 list_robot_filter_Fixed=list_robot_filter_Fixed,
                                                 list_robot_repetition_Fixed=list_robot_repetition_Fixed,
                                                 start_robot_sync_time=start_robot_sync_time,
                                                 quantity_stop=quantity_stop, pages=pages, out_id=out_id,
                                                 quantity_start=quantity_start, out_callCount=out_callCount,
                                                 search_response_body=search_values["payloads_request"],
                                                 resp_out_query_value_value=resp_out_query_value_callCount)
        else:
            quantity_stop = sync_config_Api.userinfo_skb_Api().json()['data']['uRemainQuota']
        # 执行扣点判断
        sync_config_Api.sync_robot_quantity_verdicts(quantity_start=quantity_start,
                                                     quantity_stop=quantity_stop,
                                                     unfoldNum=unfoldNum,
                                                     pid_companyName_list_sum=search_values["pid_companyName_list"])

        return '测试结束'

    @pytest.mark.parametrize('ways', ['search_list', 'advanced_search_list'])
    # 转移号码数量
    @pytest.mark.parametrize('page', [None])
    # 转移号码类型
    @pytest.mark.parametrize('dataColumns', [[0], [0, 1]])
    # 转移号码方式
    @pytest.mark.parametrize('numberCounts', [0, 1])
    # 重复是否转移
    @pytest.mark.parametrize('canCover', [True])
    # 是否创建外呼计划方式
    @pytest.mark.parametrize('needCallPlan', [True])
    # 是否扣点
    @pytest.mark.parametrize('useQuota', [True])
    def test_sync_robot_automation(self, ways, page, dataColumns, numberCounts, canCover, needCallPlan, useQuota, ES):
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """

        sync_config_automation_Api = Sync_robot(host=test_host, way=ways, useQuota=useQuota,
                                                pages=page, canCover=canCover, dataColumns=dataColumns,
                                                needCallPlan=needCallPlan, numberCounts=numberCounts,
                                                )
        if sync_config_automation_Api.can_create_task()["data"] is False:
            print("外呼计划已存在")
        # 执行搜索
        search_values = sync_config_automation_Api.search_value_list()
        taskName = "创建自动任务{}".format(time.strftime("%Y-%m-%d-%H-%M-%S"))
        if needCallPlan is True:
            resp_out_sync = sync_config_automation_Api.robot_out_call_plan().json()["data"]["list"]  # 获取外呼计划列表
            if resp_out_sync:
                resp_out_sync = resp_out_sync[0]
                out_ids = resp_out_sync["id"]
                out_gatewayId = resp_out_sync["gatewayId"]
                out_surveyId = resp_out_sync["surveyId"]
                out_callCount = resp_out_sync["callCount"]
                out_id = random.choices([out_ids, None])[0]
                if out_id is None:
                    out_jobGroupName = "外呼测试" + time.strftime("%Y年%m月%d日%H时%M分")
                else:
                    out_jobGroupName = resp_out_sync["jobGroupName"]
                # print(resp_out_sync)
                # print("外呼计划id", out_id)
            else:
                print("需要创建外呼计划，但是外呼计划列表为空", resp_out_sync)
                out_id = None
                out_gatewayId = None
                out_surveyId = None
                out_jobGroupName = None
                out_callCount = None
                # assert resp_out_sync
        else:
            out_id = None
            out_gatewayId = None
            out_surveyId = None
            out_jobGroupName = None
            out_callCount = None
        # 执行转移操作
        resp_syn = sync_config_automation_Api.robot_sync(seach_value=search_values["payloads_request"],
                                                         canCover=canCover, way=ways, out_id=out_id,
                                                         needCallPlan=needCallPlan, dataColumns=dataColumns,
                                                         numberCount=numberCounts, gatewayId=out_gatewayId,
                                                         surveyId=out_surveyId, gateway_name=out_jobGroupName,
                                                         useQuota=useQuota, automation_taskName=taskName)
        start_robot_sync_time = time.strftime("%Y-%m-%d-%H:%M", time.localtime())
        resp_sync = resp_syn.json()
        resp_syn.close()
        if resp_sync['error_code'] != 0:
            # syn_response_body = json.loads(resp_syn.request.body.decode("unicode_escape"))
            print(resp_syn.request.body.decode("unicode_escape"))
            print(resp_syn.request.url)
            print(resp_syn.request.headers)
            print(resp_sync)
        else:
            start_time = time.time()
            sync_config_automation_Api.search_elapsed_time()
            end_time = time.time()
            print("转移耗时", end_time - start_time)
            # 自动任务判断
            sync_config_automation_Api.sync_robot_automation_task_list(
                start_robot_sync_time=start_robot_sync_time,
                search_response_body=search_values["payloads_request"], )
        resp_sync_value = sync_config_automation_Api.robot_sync(seach_value=search_values["payloads_request"],
                                                                canCover=canCover, way=ways, out_id=out_id,
                                                                needCallPlan=needCallPlan, dataColumns=dataColumns,
                                                                numberCount=numberCounts, gatewayId=out_gatewayId,
                                                                surveyId=out_surveyId, gateway_name=out_jobGroupName,
                                                                useQuota=useQuota, automation_taskName=taskName).json()

        assert resp_sync_value["error_code"] == 1303 and resp_sync_value['message'] == '任务名称重复'
