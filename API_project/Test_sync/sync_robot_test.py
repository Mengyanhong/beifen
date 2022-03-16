# @Time : 2021/9/9 17:31
# @Author : 孟艳红
# @File : sync_robot_test.py

# from pprint import pprint
import requests, json, time, pytest, os, random
from API_project.Libs.sync_config_libs import Sync_robot
from API_project.Configs.Config_Info import User_Config

test_host = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境


class Test_sync_robot:
    # @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', 'map_search_list' , 'shop_search_list'])
    # @pytest.mark.parametrize('page', [None, 500, 1000, 2000])
    # 扣除流量额度，仅转移手机or手机+固话，全部号码or仅一条号码, 加入已有外呼计划
    @pytest.mark.parametrize('way', ['search_list'])
    # 转移号码数量
    @pytest.mark.parametrize('page', [None])
    # 转移号码类型
    @pytest.mark.parametrize('dataColumns', [[0], [0, 1]])
    # 转移号码方式
    @pytest.mark.parametrize('numberCounts', [0, 1])
    # 重复是否转移
    @pytest.mark.parametrize('canCover', [False, True])
    # 是否创建外呼计划方式
    @pytest.mark.parametrize('needCallPlan', [False, True])
    # 是否扣点
    @pytest.mark.parametrize('useQuota', [True])
    def test_sync_robot(self, way, page, dataColumns, numberCounts, canCover, needCallPlan, useQuota, ES):
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        sync_config_Api = Sync_robot(host=test_host, way=way, useQuota=useQuota, pages=page, canCover=canCover,
                                     dataColumns=dataColumns,
                                     numberCounts=numberCounts,
                                     )
        userinfo = sync_config_Api.userinfo_skb_Api().json()
        quantity_start = userinfo['data']['uRemainQuota']  # 获取初始额度
        hasSmartSyncRobot = userinfo['data']['hasSmartSyncRoobot']  # 获取账户类型是否灰测
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

        resp_out_sync = sync_config_Api.robot_out_call_plan().json()  # 获取外呼计划列表
        if resp_out_sync["data"]["list"]:  # and needCallPlan is True
            out_ids = resp_out_sync["data"]["list"][0]["id"]
            out_gatewayId = resp_out_sync["data"]["list"][0]["gatewayId"]
            out_surveyId = resp_out_sync["data"]["list"][0]["surveyId"]
            out_jobGroupName = resp_out_sync["data"]["list"][0]["jobGroupName"]
            out_callCount = resp_out_sync["data"]["list"][0]["callCount"]
            out_id = random.choices([out_ids, None])
            print("外呼计划id", out_id)
        else:
            print("外呼计划列表为空", resp_out_sync["data"])
            out_id = None
            out_gatewayId = None
            out_surveyId = None
            out_jobGroupName = None
            out_callCount = None
        # sync_robot_start_verdicts_dicde = {}
        # for pid_companyName_starts in search_values["pid_companyName_list"]:
        #     print(search_values["payloads_request"])
        #     print(pid_companyName_starts)
        #     # sync_robot_start_verdicts_value = sync_config_Api.sync_robot_start_verdicts(
        #     #     list_pid_company_name=pid_companyName_starts, search_payloads_values=search_values["payloads_request"])
        #     # sync_robot_start_verdicts_dicde.update({str(pid_companyName_starts["pid"]): sync_robot_start_verdicts_value})
        # print(sync_robot_start_verdicts_dicde)

        unfoldStatistics_Api_value = sync_config_Api.unfoldStatistics_Api(
            search_payload=search_values["payloads_request"], pid_list=pid, page=pages, way=way).json()
        if unfoldStatistics_Api_value["error_code"] == 0:
            unfoldNum = unfoldStatistics_Api_value["data"]["unfoldNum"]
            print("查看状态查询", unfoldStatistics_Api_value)
        else:
            unfoldNum = 0
            print("查看状态查询失败", unfoldStatistics_Api_value)
        print(unfoldStatistics_Api_value)

        resp_syn = sync_config_Api.robot_sync(pids=pid, pages=pages,
                                              seach_value=search_values["payloads_request"], canCover=canCover,
                                              way=way, out_id=out_id, needCallPlan=needCallPlan,
                                              dataColumns=dataColumns,
                                              numberCount=numberCounts, gatewayId=out_gatewayId, surveyId=out_surveyId,
                                              gatewaysname=out_jobGroupName, useQuota=useQuota)
        print(resp_syn.request.body.decode(encoding="utf-8", errors="unicode_escape"))
        print(resp_syn.request.url)
        print(resp_syn.request.headers)
        resp_sync = resp_syn.json()
        quantity_rebate = 0
        if resp_sync['error_code'] == 0:
            quantity_stop = sync_config_Api.userinfo_skb_Api().json()['data']['uRemainQuota']
            start_time = time.time()
            sync_config_Api.search_elapsed_time()
            end_time = time.time()
            print("转移耗时", end_time - start_time)
            for i in search_values["pid_companyName_list"]:
                # 获取联系方式
                list_contact_Api = sync_config_Api.list_contact(pid=i['pid'], entName=i['company_name'])
                # 获取转机器人结果
                sync_robot_value = sync_config_Api.sync_robot_verdicts(Mobile=list_contact_Api["Mobile"],
                                                                       Fixed=list_contact_Api["Fixed"],
                                                                       company_name=i['company_name'])
                #  已转未转筛选判断
                ES_search_value = ES.get(index="company_info_prod", id=i['pid'])['_source']
                if test_host == "lxcrm":
                    transferredRobotOrgs = "transferredRobotOrgs"
                else:
                    transferredRobotOrgs = "transferredRobotOrgsNonProd"
                if sync_robot_value["resp_robot_verdicts"] is True:
                    # print(ES(host="staging"))
                    assert transferredRobotOrgs in ES_search_value.keys()
                    assert str(oid) in ES_search_value[transferredRobotOrgs]
                else:
                    assert transferredRobotOrgs not in ES_search_value.keys() or str(oid) not in ES_search_value[
                        transferredRobotOrgs]
                # 执行转移判断
                quantity_rebate += sync_config_Api.sync_robot_value_verdicts_assert(
                    # sync_robot_start_value=sync_robot_start_verdicts_dicde,
                    sync_robot_value=sync_robot_value,
                    company_name_pid_list=i,
                    list_contact_all=list_contact_Api,
                    hasSmartSyncRobot=hasSmartSyncRobot)
            # resp_out_query = sync_config_Api.robot_out_call_plan().json()["data"]["list"]  # 获取外呼计划列表
            # resp_out_query_value_sum = 0
            # resp_out_query_value_value = None
            # for resp_out_query_value in resp_out_query:
            #     if resp_out_query_value["id"] == out_id:
            #         resp_out_query_value_sum += 1
            #         resp_out_query_value_value = resp_out_query_value
            #         # assert resp_out_query_value["callCount"] > resp_out_sync_value["callCount"]
            #         assert resp_out_query_value["jobGroupName"] == out_jobGroupName
            #         break
            # assert resp_out_query_value_sum > 0
        else:
            quantity_stop = sync_config_Api.userinfo_skb_Api().json()['data']['uRemainQuota']
            quantity_rebate = 0
        # 执行扣点判断
        sync_config_Api.sync_robot_quantity_verdicts(quantity_start=quantity_start,
                                                     quantity_stop=quantity_stop, quantity_rebate=quantity_rebate,
                                                     hasSmartSyncRobot=hasSmartSyncRobot, unfoldNum=unfoldNum,
                                                     pid_companyName_list_sum=search_values["pid_companyName_list"])

        return '测试结束，扣除流量额度，仅转移手机，全部号码,加入已有外呼计划'
