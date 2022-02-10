# @Time : 2021/9/9 17:31
# @Author : 孟艳红
# @File : sync_robot_test.py

from pprint import pprint
import requests, json, time, pytest, os, random
from API_project.Configs.config_API import user
from API_project.Configs.search_API import search
from API_project.Configs.shop_API import shop
from API_project.Libs.sync_robot_libs import Sync_robot

test_host = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境

user = user(test_host)
Sync_robot = Sync_robot(test_host)
search = search(test_host)
shop = shop(test_host)


class Test_sync_robot:
    # @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', 'map_search_list' , 'shop_search_list'])
    # @pytest.mark.parametrize('page', [None, 500, 1000, 2000])

    # 扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划
    @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', 'map_search_list', 'shop_search_list'])
    @pytest.mark.parametrize('page', [None, 500])
    def testcase01(self, way, page):
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
        if way == 'search_list':
            response = search.skb_search()
            list_companyName_add = 'companyName'
        elif way == 'advanced_search_list':
            response = search.advanced_search()
            list_companyName_add = 'companyName'
        elif way == 'shop_search_list':
            response = shop.search_shop()
            list_companyName_add = 'name'
        else:
            response = search.skb_address_search()
            list_companyName_add = 'companyName'
        request_payloa = json.loads(response.request.body.decode("unicode_escape"))
        # print(request_payloa)
        # print(response.request.headers)
        response_value = response.json()
        response.close()
        if response_value['error_code'] != 0:
            print('搜索结果有误\n', response_value)
            assert response_value['error_code'] == 0
        if response_value['data']['total'] == 0:
            print('搜索结果为空\n', response_value)
            assert response_value['data']['total'] != 0
        pid_list = []
        resp_companyName_list = []
        resp_items = response_value['data']['items']
        if page is None:
            pid = pid_list
            pages = None
        else:
            pid = None
            pages = page
        for i in resp_items:
            pid_list.append(i['id'])
            resp_companyName_list.append(
                {'pid': i['id'], 'company_name': i[list_companyName_add]})
        resp_sync = Sync_robot.sync(pids=pid, pages=pages, dataColumns=[0, 1], numberCount=1,
                                    seach_value=request_payloa,
                                    way=way)
        # print(resp_sync.request.body.decode("utf-8"))
        if resp_sync.json()['error_code'] == 0:
            for i_value in range(200):
                time.sleep(2.1)
                if way == 'search_list':
                    response_sum = search.skb_search().json()
                elif way == 'advanced_search_list':
                    response_sum = search.advanced_search().json()
                elif way == 'shop_search_list':
                    response_sum = shop.search_shop().json()
                else:
                    response_sum = search.skb_address_search().json()
                # print(response_sum['data'])
                if response_sum['data'] != {}:
                    break
            sync_sum = 0
            for i in resp_companyName_list:
                resp_robot_phone_list = Sync_robot.robot_uncalled(query_name=i['company_name']).json()['data'][
                    'list']
                # print(i)
                # print(resp_robot_phone_list.request.url)
                # print(resp_robot_phone_list.request.headers)
                # print(resp_robot_phone_list.json())
                if not resp_robot_phone_list:
                    sync_sum += 1
                    contacts_num_list = search.skb_contacts_num(id=i['pid'], module=way).json()['data'][
                        'contacts']
                    content_list = []
                    content_list_type1 = []
                    for j in contacts_num_list:
                        if j['type'] == 2:
                            content_list.append(j['content'])
                        elif j['type'] == 1:
                            content_list_type1.append(j['content'])
                    if content_list or content_list_type1:
                        print(i, '转移失败,该企业有联系方式\n固话', content_list, '\n手机', content_list_type1)
                        # assert not content_list and not content_list_type1
                    else:
                        print(i, '搜索出错，该企业无联系方式')
                else:
                    company_name_sum = 0
                    for company_name in resp_robot_phone_list:
                        if company_name['company_name'] == i['company_name']:
                            company_name_sum += 1
                    if company_name_sum != 1:
                        print(i, '，转移号码数量错误\n', resp_robot_phone_list)
            # assert sync_sum < len(resp_companyName_list)
        user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
        if pages is not None:
            print(user_Qu, user_Quota, len(resp_companyName_list))
            print('转移的企业', resp_companyName_list)
            assert user_Qu == (user_Quota - pages) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            if user_Qu != (user_Quota - len(resp_companyName_list)):
                print(user_Qu, user_Quota, len(resp_companyName_list))
                print('转移的企业', resp_companyName_list)
            assert user_Qu == (user_Quota - len(resp_companyName_list))
        return '测试结束，未查看数据选择扣点且仅转移一条号码case'

    # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
    @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', 'map_search_list', 'shop_search_list'])
    @pytest.mark.parametrize('page', [None, 500])
    def testcase02(self, way, page):
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
        if way == 'search_list':
            response = search.skb_search()
            list_companyName_add = 'companyName'
        elif way == 'advanced_search_list':
            response = search.advanced_search()
            list_companyName_add = 'companyName'
        elif way == 'shop_search_list':
            response = shop.search_shop()
            list_companyName_add = 'name'
        else:
            response = search.skb_address_search()
            list_companyName_add = 'companyName'

        request_payloa = json.loads(response.request.body.decode("utf-8"))
        # request_payloa = json.loads(response.request.body.decode("unicode_escape"))
        response_value = response.json()
        response.close()
        if response_value['error_code'] != 0:
            print('搜索结果有误\n', response_value)
            assert response_value['error_code'] == 0
        if response_value['data']['total'] == 0:
            print('搜索结果为空\n', response_value)
            assert response_value['data']['total'] != 0

        pid_list = []
        resp_companyName_list = []
        resp_items = response_value['data']['items']
        if way is None:
            pid = None
            pages = 500
        elif page is None:
            pid = pid_list
            pages = None
        else:
            pid = None
            pages = page
        for i in resp_items:
            pid_list.append(i['id'])
            resp_companyName_list.append(
                {'pid': i['id'], 'company_name': i[list_companyName_add]})
        resp_sync = Sync_robot.sync(pids=pid, pages=pages, dataColumns=[0, 1], Quota=False, numberCount=1,
                                    seach_value=request_payloa,
                                    way=way)
        # print(resp_sync.request.body.decode("utf-8"))
        # print(resp_sync.request.url)
        # print(resp_sync.request.headers)
        if resp_sync.json()['error_code'] == 0:
            for i in range(200):
                time.sleep(2.2)
                if way == 'search_list':
                    response_sum = search.skb_search().json()
                elif way == 'advanced_search_list':
                    response_sum = search.advanced_search().json()
                elif way == 'shop_search_list':
                    response_sum = shop.search_shop().json()
                else:
                    response_sum = search.skb_address_search().json()
                # print(response_sum['data'])
                if response_sum['data'] != {}:
                    break
            sync_sum = 0
            for i in resp_companyName_list:
                resp_robot = Sync_robot.robot_uncalled(query_name=i['company_name']).json()['data']['list']
                if resp_robot:
                    sync_sum += 1
                    print(i, '企业被成功转移，测试失败\n', resp_robot)
            user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
            if sync_sum == len(resp_companyName_list):
                if user_Qu == user_Quota:
                    print('测试失败,数据全部被转移,且没有扣点')
                else:
                    print('测试失败,数据被转移,且进行了扣点')
            elif sync_sum != 0:
                if user_Qu == user_Quota:
                    print('测试失败,数据被转移,且没有扣点')
                else:
                    print('测试失败,数据被转移,且进行了扣点')
            assert user_Qu == user_Quota
            assert sync_sum == 0
        return '测试结束,未查看数据选择不扣除流量额度测试'

    # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，仅转移已查看数据
    @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', 'map_search_list', 'shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def testcase03(self, way, page):
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客,'shop_search_list':找店铺
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
        if way == 'search_list':
            response = search.skb_search(filterUnfold=1, filterSync=0)
            list_companyName_add = 'companyName'
        elif way == 'advanced_search_list':
            response = search.advanced_search(hasUnfolded=1, hasSyncClue=0, page=2)
            list_companyName_add = 'companyName'
        elif way == 'shop_search_list':
            response = shop.search_shop(hasSyncClue=0, hasUnfolded=1)
            list_companyName_add = 'name'
        else:
            response = search.skb_address_search(filterUnfold=1, filterSync=0)
            list_companyName_add = 'companyName'

        request_payloa = json.loads(response.request.body.decode("utf-8"))
        response_value = response.json()
        response.close()
        if response_value['error_code'] != 0:
            print('搜索结果有误\n', response_value)
            assert response_value['error_code'] == 0
        if response_value['data']['total'] == 0:
            print('搜索结果为空\n', response_value)
            assert response_value['data']['total'] != 0

        pid_list = []
        resp_companyName_list = []
        resp_items = response_value['data']['items']
        if page is None:
            pid = pid_list
            pages = None
        else:
            pid = None
            pages = page
        for i in resp_items:
            pid_list.append(i['id'])
            resp_companyName_list.append(
                {'pid': i['id'], 'company_name': i[list_companyName_add]})
        resp_sync = Sync_robot.sync(pids=pid, pages=pages, canCover=True, dataColumns=[0, 1], Quota=False,
                                    numberCount=1,
                                    seach_value=request_payloa,
                                    way=way)
        # print(resp_sync.json())
        if resp_sync.json()['error_code'] == 0:
            for i in range(200):
                time.sleep(2.2)
                if way == 'search_list':
                    response_sum = search.skb_search(filterUnfold=1)  # 搜索未查看，未转机器人的数据
                elif way == 'advanced_search_list':
                    response_sum = search.advanced_search(hasUnfolded=1)
                elif way == 'shop_search_list':
                    response_sum = shop.search_shop(hasSyncClue=0, hasUnfolded=1, cv=[
                        {"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": []}, "cr": "IN"},
                        {"cn": "contactType", "cv": ["1", "2"], "cr": "IN"}])
                else:
                    response_sum = search.skb_address_search(filterUnfold=1)
                # print(response_sum.json()['data'])
                if response_sum.json()['data'] != {}:
                    break
                response_sum.close()
            sync_sum = 0
            for i in resp_companyName_list:
                resp_robot = Sync_robot.robot_uncalled(query_name=i['company_name']).json()
                if not resp_robot['data']['list']:
                    sync_sum += 1
                else:
                    print(resp_robot)
                    assert len(resp_robot['data']['list']) >= 1
            if sync_sum == len(resp_companyName_list):
                print('测试失败,没有转移成功的企业\n', resp_companyName_list)
                assert sync_sum != len(resp_companyName_list)
            else:
                assert 0 <= sync_sum < len(resp_companyName_list)
        else:
            print('转移失败')
        user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
        assert user_Qu == user_Quota
        return '测试结束,仅转移已查看数据选择不扣除流量额度测试仅1条号码'

    # 扣除流量额度，转移手机和固话，全部号码,不创建外呼计划，
    @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', 'map_search_list', 'shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def test_case04(self, way, page):
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
        if way == 'search_list':
            response = search.skb_search()
            list_companyName_add = 'companyName'
        elif way == 'advanced_search_list':
            response = search.advanced_search()
            list_companyName_add = 'companyName'
        elif way == 'shop_search_list':
            response = shop.search_shop()
            list_companyName_add = 'name'
        else:
            response = search.skb_address_search(contact=2)
            list_companyName_add = 'companyName'
        # 搜索未查看，未转机器人的数据，有固话
        request_payloa = json.loads(response.request.body.decode("unicode_escape"))
        response_value = response.json()
        response.close()
        if response_value['data'] == {}:
            print(response_value['data'])
            assert response_value['data'] != {}
        elif response_value['data']['total'] == 0:
            print(response_value['data'])
            assert response_value['total'] != 0
        else:
            response_value = response_value
        pid_list = []
        company_name_list_pid = []
        if way is None:
            pid = None
            pages = 500
        elif page is None:
            pid = pid_list
            pages = None
        else:
            pid = None
            pages = page

        resp_items = response_value['data']['items']
        if resp_items:
            for i in resp_items:
                pid_list.append(i['id'])
                company_name_list_pid.append(
                    {'pid': i['id'], 'company_name': i[list_companyName_add]})

        resp_syn = Sync_robot.sync(pids=pid, pages=pages, canCover=True, dataColumns=[0, 1],
                                   seach_value=request_payloa,
                                   way=way)
        resp_sync = resp_syn.json()
        if resp_sync['error_code'] == 0:
            stattime = time.time()
            for i_value in range(200):
                time.sleep(2.2)
                if way == 'search_list':
                    response_list = search.skb_search().json()
                elif way == 'advanced_search_list':
                    response_list = search.advanced_search().json()
                elif way == 'shop_search_list':
                    response_list = shop.search_shop().json()
                else:
                    response_list = search.skb_address_search(contact=2).json()
                if response_list['data'] != {}:
                    print('转移耗时', time.time() - stattime, 's')
                    break
            for i in company_name_list_pid:
                contacts_num = search.skb_contacts_num(id=i['pid'], module=way)
                contacts_num_list = contacts_num.json()['data']['contacts']
                content_list = []
                for j in contacts_num_list:
                    if j['type'] == 2 or j['type'] == 1:
                        content_list.append(j['content'])
                resp_robot_com = Sync_robot.robot_uncalled(query_name=i['company_name'], queryType=2).json()['data'][
                    'list']
                if resp_robot_com:
                    if len(content_list) == len(resp_robot_com):
                        pass
                    elif content_list:
                        sync_robot_list = []
                        for q in content_list:
                            time.sleep(1)
                            resp_robot = Sync_robot.robot_uncalled(query_name=q, queryType=3).json()['data'][
                                'list']
                            if not resp_robot:
                                sync_robot_list.append(q)
                        if len(sync_robot_list) == len(content_list):
                            print(i, content_list, '号码转移错误')
                        elif 0 < len(sync_robot_list) < len(content_list):
                            print(i, '部分号码转移出错', sync_robot_list)
                        elif 0 == len(sync_robot_list):
                            pass
                        else:
                            print('号码出错''\n', contacts_num.request.body)
                    else:
                        print(i, '联系方式为空', contacts_num_list, '\n', contacts_num.request.url)
                else:
                    print(i, '企业转移失败', contacts_num_list, '\n', contacts_num.json())
        else:
            pprint(resp_syn.request.body)
            pprint(resp_syn.request.headers)
            pprint(resp_syn.request.url)
        user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']

        if pages is not None:
            print(user_Qu, user_Quota, pages)
            if user_Quota < pages:
                print(user_Qu, user_Quota, pages)
                pprint(user.skb_userinfo().json())
            assert user_Qu == (user_Quota - pages) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            print(user_Qu, user_Quota, len(resp_items))
            if user_Quota < len(resp_items):
                print(user_Qu, user_Quota, len(resp_items))
                pprint(user.skb_userinfo().json())
            assert user_Qu == (user_Quota - len(resp_items))
        return '测试结束，全部号码，手机加固话，扣除流量额度，测试全部号码/固话转移case'

    # 扣除流量额度，仅转移手机or手机+固话，全部号码or仅一条号码, 加入已有外呼计划
    @pytest.mark.parametrize('way', ['search_list'])  # 转移号码模块
    @pytest.mark.parametrize('page', [None])  # 转移号码数量
    @pytest.mark.parametrize('dataColumns', [None, [0, 1]])  # 转移号码类型
    @pytest.mark.parametrize('numberCounts', [0, 1])  # 转移号码方式
    def testcase05(self, way, page, dataColumns, numberCounts):
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
        if way == 'search_list':
            response = search.skb_search()
            list_companyName_add = 'companyName'
        elif way == 'advanced_search_list':
            response = search.advanced_search()
            list_companyName_add = 'companyName'
        elif way == 'shop_search_list':
            response = shop.search_shop()
            list_companyName_add = 'name'
        else:
            response = search.skb_address_search(contact=2)
            list_companyName_add = 'companyName'
        # 搜索未查看，未转机器人的数据，有固话
        request_payloa = json.loads(response.request.body.decode("unicode_escape"))
        response_value = response.json()
        response.close()
        if response_value['data'] == {}:
            print(response_value['data'])
            assert response_value['data'] != {}
        elif response_value['data']['total'] == 0:
            print(response_value['data'])
            assert response_value['total'] != 0
        else:
            response_value = response_value
        pid_list = []
        company_name_list_pid = []
        if way is None:
            pid = None
            pages = 500
        elif page is None:
            pid = pid_list
            pages = None
        else:
            pid = None
            pages = page

        resp_items = response_value['data']['items']
        if resp_items:
            for i in resp_items:
                pid_list.append(i['id'])
                company_name_list_pid.append(
                    {'pid': i['id'], 'company_name': i[list_companyName_add]})

        resp_out_sync = Sync_robot.robot_outcallplan().json()  # 获取外呼计划列表
        resp_out_sync_value = None
        if resp_out_sync["data"]["list"]:
            for gatewayId_re in resp_out_sync["data"]["list"]:
                if gatewayId_re["gatewayId"] == user.user_key()["gatewayId"]:
                    resp_out_sync_value = gatewayId_re
                    break
            # print("计划id", resp_out_sync_value["id"], "计划号码数量", resp_out_sync_value["callCount"], "计划名称",
            #       resp_out_sync_value["jobGroupName"])
        if resp_out_sync_value is None:
            print("外呼计划列表内没有假线路", resp_out_sync["data"])
            assert resp_out_sync["data"]["list"] != []
        out_id = resp_out_sync_value["id"]

        resp_syn = Sync_robot.sync(pids=pid, pages=pages,
                                   seach_value=request_payloa, canCover=True,
                                   way=way, out_id=out_id, needCallPlan=True, dataColumns=dataColumns,
                                   numberCount=numberCounts)
        resp_sync = resp_syn.json()
        resp_syn.close()
        user_Qu_test = 0
        if resp_sync['error_code'] == 0:
            for data_value in range(200):
                stattime = time.time()
                time.sleep(2.2)
                if way == 'search_list':
                    response_list = search.skb_search().json()
                elif way == 'advanced_search_list':
                    response_list = search.advanced_search().json()
                elif way == 'shop_search_list':
                    response_list = shop.search_shop().json()
                else:
                    response_list = search.skb_address_search().json()
                if response_list['data'] != {}:
                    # print('转移耗时', int(time.time() - stattime), 's')
                    break
            for i in company_name_list_pid:
                contacts_num = search.skb_contacts_num(id=i['pid'], module=way)
                # print(contacts_num.request.headers)
                contacts_num_list = contacts_num.json()['data']['contacts']

                content_list_type2 = []
                content_list_type1 = []
                for j in contacts_num_list:
                    if j['type'] == 2:
                        content_list_type2.append(j['content'])
                    elif j['type'] == 1:
                        content_list_type1.append(j['content'])
                resp_robot_com = Sync_robot.robot_uncalled(query_name=i['company_name'], queryType=2).json()['data'][
                    'list']
                if resp_robot_com:
                    numberCounts_value = 0
                    if len(content_list_type1) != len(resp_robot_com):
                        # print(i,"转移成功，固话未被转移")
                        sync_robot_list_type1 = []
                        if content_list_type1:
                            for q_type1 in content_list_type1:
                                resp_robot_type1 = \
                                    Sync_robot.robot_uncalled(query_name=q_type1, queryType=3).json()['data'][
                                        'list']
                                if resp_robot_type1:
                                    for company_name_phone1 in resp_robot_type1:
                                        if company_name_phone1["company_name"] == i['company_name']:
                                            sync_robot_list_type1.append(q_type1)
                                            break
                            if len(sync_robot_list_type1) == len(content_list_type1):
                                if numberCounts == 1:
                                    if len(sync_robot_list_type1) == 1:
                                        numberCounts_value += 1
                                # print(i, "转移成功，手机转移完成")
                            elif len(sync_robot_list_type1) < len(content_list_type1):
                                if numberCounts == 1:
                                    if len(sync_robot_list_type1) == 1:
                                        numberCounts_value += 1
                                else:
                                    print(i, '转移出错仅转移部分手机号码\n条件', way, page, dataColumns, numberCounts,
                                          '\n号码', sync_robot_list_type1)
                            elif len(sync_robot_list_type1) <= 0:
                                if numberCounts == 0:
                                    print(i, '手机转移失败\n企业手机号为', content_list_type1, '\n条件', way, page, dataColumns,
                                          numberCounts)
                            else:
                                print(i, '手机获取错误\n', sync_robot_list_type1)
                        sync_robot_list_type2 = []
                        if content_list_type2:
                            for q_type2 in content_list_type2:
                                resp_robot_type2 = \
                                    Sync_robot.robot_uncalled(query_name=q_type2, queryType=3).json()['data'][
                                        'list']
                                if resp_robot_type2:
                                    for company_name_phone2 in resp_robot_type2:
                                        if company_name_phone2["company_name"] == i['company_name']:
                                            sync_robot_list_type2.append(q_type2)
                                            break

                            if len(sync_robot_list_type2) == len(content_list_type2):
                                if dataColumns is None:
                                    print(i, '转移出错固话进行了转移\n', content_list_type2, '\n条件', way, page, dataColumns,
                                          numberCounts)
                                else:
                                    if numberCounts == 1:
                                        if len(sync_robot_list_type2) == 1:
                                            numberCounts_value += 1
                                    # print(i, '固话转移成功\n', content_list_type2)
                            elif 0 < len(sync_robot_list_type2) < len(content_list_type2):
                                if dataColumns is None:
                                    print(i, '转移出错部分固话进行了转移\n', sync_robot_list_type2, '\n条件', way, page, dataColumns,
                                          numberCounts)
                                else:
                                    if numberCounts == 1:
                                        if len(sync_robot_list_type2) == 1:
                                            numberCounts_value += 1
                                    else:
                                        print(i, '转移出错仅部分固话进行了转移\n', content_list_type2, '\n条件', way, page, dataColumns,
                                              numberCounts)
                            elif 0 == len(sync_robot_list_type2):
                                pass
                                # if dataColumns is not None:
                                #     print(i, '转移出错固话未转移\n', content_list_type2)
                                # else:
                                #     print(i, '测试成功固话未转移\n', content_list_type2)
                            else:
                                print(i, '固话获取错误\n', sync_robot_list_type2)
                    if numberCounts == 1:
                        if numberCounts_value != 1:
                            print(i, '仅转移一条号码出错\n实际转移', numberCounts_value, "条", '\n条件', way, page, dataColumns,
                                  numberCounts)
                    else:
                        if numberCounts_value != 0:
                            print(i, '仅转移一条号码出错\n实际转移', numberCounts_value, "条", '\n条件', way, page, dataColumns,
                                  numberCounts)
                else:
                    if len(content_list_type1) != 0:
                        print(i, '企业有手机但是转移失败\n', content_list_type1, '\n条件', way, page, dataColumns,
                              numberCounts)
                    elif len(content_list_type1) == 0 and len(content_list_type2) == 0:
                        print(i, '企业联系方式为空\n', contacts_num_list, '\n条件', way, page, dataColumns,
                              numberCounts)
                    else:
                        print(i, '该企业未转移该企业仅有固话\n', content_list_type2, '\n条件', way, page, dataColumns,
                              numberCounts)

            resp_out_query = Sync_robot.robot_outcallplan().json()["data"]["list"]  # 获取外呼计划列表
            resp_out_query_value_sum = 0
            resp_out_query_value_value = None
            for resp_out_query_value in resp_out_query:
                if resp_out_query_value["id"] == resp_out_sync_value["id"]:
                    resp_out_query_value_sum += 1
                    resp_out_query_value_value = resp_out_query_value
                    assert resp_out_query_value["callCount"] > resp_out_sync_value["callCount"]
                    assert resp_out_query_value["jobGroupName"] == resp_out_sync_value["jobGroupName"]
                    break
            assert resp_out_query_value_sum > 0
            # if resp_out_query_value_sum > 0:
            #     print("加入外呼计划成功，加入前", resp_out_sync_value["callCount"], "\n加入后",
            #           resp_out_query_value_value["callCount"])
            # else:
            #     print("加入计划失败，加入前", resp_out_sync_value["callCount"], "\n加入后", resp_out_query_value_value["callCount"])

        user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
        if pages is not None:
            print(user_Qu, user_Quota, pages)
            if user_Quota < pages:
                pprint(user.skb_userinfo().json())
                print(resp_items)
            assert user_Qu == (user_Quota - pages + user_Qu_test) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            print(user_Qu, user_Quota, len(resp_items))
            if user_Quota < len(resp_items):
                pprint(user.skb_userinfo().json())
                print(resp_items)
            assert user_Qu == (user_Quota - len(resp_items) + user_Qu_test)

        return '测试结束，扣除流量额度，仅转移手机，全部号码,加入已有外呼计划'
    #
    # @pytest.mark.parametrize('way', ['shop_search_list'])
    # @pytest.mark.parametrize('page', [None])
    # def testcase06(self, way, page):  # 扣除流量额度，仅转移手机，全部号码,创建外呼计划，
    #     """
    #     :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
    #     :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
    #     :return:
    #     """
    #     user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
    #     if way == 'search_list':
    #         response = search.skb_search()
    #         list_companyName_add = 'companyName'
    #     elif way == 'advanced_search_list':
    #         response = search.advanced_search()
    #         list_companyName_add = 'companyName'
    #     elif way == 'shop_search_list':
    #         response = shop.search_shop()
    #         list_companyName_add = 'name'
    #     else:
    #         response = search.skb_address_search(contact=2)
    #         list_companyName_add = 'companyName'
    #     # 搜索未查看，未转机器人的数据，有固话
    #     request_payloa = json.loads(response.request.body.decode("unicode_escape"))
    #     response_value = response.json()
    #     response.close()
    #     if response_value['data'] == {}:
    #         print(response_value['data'])
    #         assert response_value['data'] != {}
    #     elif response_value['data']['total'] == 0:
    #         print('搜索结果为空', response_value['data'])
    #         assert response_value['total'] != 0
    #     else:
    #         response_value = response_value
    #     pid_list = []
    #     company_name_list_pid = []
    #     if way is None:
    #         pid = None
    #         pages = 500
    #     elif page is None:
    #         pid = pid_list
    #         pages = None
    #     else:
    #         pid = None
    #         pages = page
    #     resp_items = response_value['data']['items']
    #     if resp_items:
    #         for i in resp_items:
    #             pid_list.append(i['id'])
    #             company_name_list_pid.append(
    #                 {'pid': i['id'], 'company_name': i[list_companyName_add]})
    #
    #     resp_out_sync = Sync_robot.robot_outcallplan(gateway_HOT=test_host).json()  # 获取外呼计划列表
    #     if resp_out_sync["data"]["list"]:
    #         resp_out_sync_value = resp_out_sync["data"]["list"][0]
    #         print(resp_out_sync_value["id"], resp_out_sync_value["callCount"], resp_out_sync_value["jobGroupName"])
    #     else:
    #         resp_out_sync_value = None
    #         print(resp_out_sync["data"])
    #         assert resp_out_sync["data"]["list"] != []
    #     gatewayname = f"自动化测试{str(random.randint(10,100))}"
    #
    #     resp_syn = Sync_robot.sync(pids=pid, pages=pages,
    #                                seach_value=request_payloa, canCover=True,
    #                                way=way,gatewayname=gatewayname, gatewayId=resp_out_sync_value["gatewayId"],surveyId=resp_out_sync_value["surveyId"], needCallPlan=True)
    #     resp_sync = resp_syn.json()
    #     resp_syn.close()
    #     user_Qu_test = 0
    #     if resp_sync['error_code'] == 0:
    #         for data_value in range(200):
    #             stattime = time.time()
    #             time.sleep(2.2)
    #             if way == 'search_list':
    #                 response_list = search.skb_search().json()
    #             elif way == 'advanced_search_list':
    #                 response_list = search.advanced_search().json()
    #             elif way == 'shop_search_list':
    #                 response_list = shop.search_shop().json()
    #             else:
    #                 response_list = search.skb_address_search().json()
    #             if response_list['data'] != {}:
    #                 print('转移耗时', int(time.time() - stattime), 's')
    #                 break
    #         for i in company_name_list_pid:
    #             user_Qu_type2 = 0
    #             user_Qu_type1 = 0
    #             contacts_num = search.skb_contacts_num(id=i['pid'], module=way)
    #             contacts_num_list = contacts_num.json()['data']['contacts']
    #             content_list_type2 = []
    #             content_list_type1 = []
    #             for j in contacts_num_list:
    #                 if j['type'] == 2:
    #                     content_list_type2.append(j['content'])
    #                 elif j['type'] == 1:
    #                     content_list_type1.append(j['content'])
    #             resp_robot_com = Sync_robot.robot_uncalled(query_name=i['company_name'], queryType=2).json()['data'][
    #                 'list']
    #             if resp_robot_com:
    #                 if len(content_list_type2) + len(content_list_type1) == len(resp_robot_com):
    #                     pass
    #                 else:
    #                     if content_list_type1:
    #                         sync_robot_list_type1 = []
    #                         for q_type1 in content_list_type1:
    #                             time.sleep(1)
    #                             resp_robot_type1 = \
    #                             Sync_robot.robot_uncalled(query_name=q_type1, queryType=3).json()['data'][
    #                                 'list']
    #                             if not resp_robot_type1:
    #                                 sync_robot_list_type1.append(q_type1)
    #                         if len(sync_robot_list_type1) == len(content_list_type1):
    #                             print(i, content_list_type1, '手机转移失败')
    #                         elif 0 < len(sync_robot_list_type1) < len(content_list_type1):
    #                             print(i, '部分手机号码转移出错', sync_robot_list_type1)
    #                         elif 0 == len(sync_robot_list_type1):
    #                             pass
    #                         else:
    #                             print('手机获取错误\n', contacts_num.request.body)
    #                     else:
    #                         user_Qu_type1 += 1
    #                         print(i, '手机为空', contacts_num_list, '\n', contacts_num.request.url)
    #
    #                     if content_list_type2:
    #                         sync_robot_list_type2 = []
    #                         for q_type2 in content_list_type2:
    #                             time.sleep(1)
    #                             resp_robot_type2 = \
    #                             Sync_robot.robot_uncalled(query_name=q_type2, queryType=3).json()['data'][
    #                                 'list']
    #                             if not resp_robot_type2:
    #                                 sync_robot_list_type2.append(q_type2)
    #                         if len(sync_robot_list_type2) == len(content_list_type2):
    #                             print(i, content_list_type2, '固话转移失败')
    #                         elif 0 < len(sync_robot_list_type2) < len(content_list_type2):
    #                             print(i, '部分固话号码转移出错', sync_robot_list_type2)
    #                         elif 0 == len(sync_robot_list_type2):
    #                             pass
    #                         else:
    #                             print('固话获取错误\n', contacts_num.request.body)
    #                     else:
    #                         user_Qu_type2 += 1
    #                         print(i, '固话为空', contacts_num_list, '\n', contacts_num.request.url)
    #             else:
    #                 user_Qu_test += 1
    #                 print(i, '企业转移失败', contacts_num_list, '\n', contacts_num.json())
    #             if user_Qu_type2 != 0 and user_Qu_type1 != 0:
    #                 user_Qu_test += 1
    #                 print(i, '该企业无联系方式', contacts_num_list, '\n', contacts_num.json())
    #             elif user_Qu_type1 != 0 and user_Qu_type2 == 0:
    #                 print(i, '该企业无手机号码但是有固话', contacts_num_list, '\n', contacts_num.json())
    #             elif user_Qu_type2 != 0:
    #                 print(i, '该企业无固话号码', contacts_num_list, '\n', contacts_num.json())
    #         resp_out_query = Sync_robot.robot_outcallplan(gatewayId=resp_out_sync_value["gatewayId"],gateway_HOT="lxcrm").json()["data"]["list"]  # 获取外呼计划列表
    #         resp_out_query_value_sum = 0
    #         resp_out_query_value_value = None
    #         for resp_out_query_value in resp_out_query:
    #             if resp_out_query_value["jobGroupName"] == gatewayname and \
    #                     resp_out_query_value["gatewayId"] == resp_out_sync_value["gatewayId"] and \
    #                     resp_out_query_value["surveyId"] == resp_out_sync_value["surveyId"]:
    #                 resp_out_query_value_sum += 1
    #                 resp_out_query_value_value = resp_out_query_value
    #                 break
    #         if resp_out_query_value_sum > 0:
    #             print("创建外呼计划成功，外呼计划为", resp_out_query_value_value)
    #         else:
    #             print("创建外呼计划失败，计划名", gatewayname, "创建后列表", resp_out_query)
    #     else:
    #         pprint(resp_syn.request.body)
    #         pprint(resp_syn.request.headers)
    #         pprint(resp_syn.request.url)
    #     user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
    #     if pages is not None:
    #         print(user_Qu, user_Quota, pages)
    #         if user_Quota < pages:
    #             pprint(user.skb_userinfo().json())
    #             print(resp_items)
    #         assert user_Qu == (user_Quota - pages + user_Qu_test) or user_Quota > user_Qu > (user_Quota - pages)
    #     else:
    #         print(user_Qu, user_Quota, len(resp_items))
    #         if user_Quota < len(resp_items):
    #             pprint(user.skb_userinfo().json())
    #             print(resp_items)
    #         assert user_Qu == (user_Quota - len(resp_items) + user_Qu_test)
    #
    #     return '测试结束，全部号码，手机，扣除流量额度，测试仅手机转移case'
    #
    # def testbeifen(self, way, page):  # 扣除流量额度，仅转移手机，全部号码,加入已有外呼计划，
    #     """
    #     :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
    #     :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
    #     :return:
    #     """
    #     user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
    #     if way == 'search_list':
    #         response = search.skb_search()
    #         list_companyName_add = 'companyName'
    #     elif way == 'advanced_search_list':
    #         response = search.advanced_search()
    #         list_companyName_add = 'companyName'
    #     elif way == 'shop_search_list':
    #         response = shop.search_shop()
    #         list_companyName_add = 'name'
    #     else:
    #         response = search.skb_address_search(contact=2)
    #         list_companyName_add = 'companyName'
    #     # 搜索未查看，未转机器人的数据，有固话
    #     request_payloa = json.loads(response.request.body.decode("unicode_escape"))
    #     response_value = response.json()
    #     response.close()
    #     if response_value['data'] == {}:
    #         print(response_value['data'])
    #         assert response_value['data'] != {}
    #     elif response_value['data']['total'] == 0:
    #         print('搜索结果为空', response_value['data'])
    #         assert response_value['total'] != 0
    #     else:
    #         response_value = response_value
    #     pid_list = []
    #     company_name_list_pid = []
    #     if way is None:
    #         pid = None
    #         pages = 500
    #     elif page is None:
    #         pid = pid_list
    #         pages = None
    #     else:
    #         pid = None
    #         pages = page
    #     resp_items = response_value['data']['items']
    #     if resp_items:
    #         for i in resp_items:
    #             pid_list.append(i['id'])
    #             company_name_list_pid.append(
    #                 {'pid': i['id'], 'company_name': i[list_companyName_add]})
    #
    #     resp_out_sync = Sync_robot.robot_outcallplan().json()  # 获取外呼计划列表
    #     if resp_out_sync["data"]["list"]:
    #         resp_out_sync_value = resp_out_sync["data"]["list"][0]
    #         pprint(resp_out_sync_value["id"], resp_out_sync_value["callCount"], resp_out_sync_value["jobGroupName"])
    #     else:
    #         resp_out_sync_value = None
    #         print(resp_out_sync["data"])
    #         assert resp_out_sync["data"]["list"] != []
    #
    #     resp_syn = Sync_robot.sync(pids=pid, pages=pages,
    #                                seach_value=request_payloa, canCover=True,
    #                                way=way, out_payload=True, out_id=resp_out_sync_value["id"])
    #     resp_sync = resp_syn.json()
    #     resp_syn.close()
    #     user_Qu_test = 0
    #     if resp_sync['error_code'] == 0:
    #         for data_value in range(200):
    #             stattime = time.time()
    #             time.sleep(2.2)
    #             if way == 'search_list':
    #                 response_list = search.skb_search().json()
    #             elif way == 'advanced_search_list':
    #                 response_list = search.advanced_search().json()
    #             elif way == 'shop_search_list':
    #                 response_list = shop.search_shop().json()
    #             else:
    #                 response_list = search.skb_address_search().json()
    #             if response_list['data'] != {}:
    #                 print('转移耗时', int(time.time() - stattime), 's')
    #                 break
    #         for i in company_name_list_pid:
    #             user_Qu_type2 = 0
    #             user_Qu_type1 = 0
    #             contacts_num = search.skb_contacts_num(id=i['pid'], module=way)
    #             contacts_num_list = contacts_num.json()['data']['contacts']
    #             content_list_type2 = []
    #             content_list_type1 = []
    #             for j in contacts_num_list:
    #                 if j['type'] == 2:
    #                     content_list_type2.append(j['content'])
    #                 elif j['type'] == 1:
    #                     content_list_type1.append(j['content'])
    #             resp_robot_com = Sync_robot.robot_uncalled(query_name=i['company_name'], queryType=2).json()['data'][
    #                 'list']
    #             if resp_robot_com:
    #                 if len(content_list_type2) + len(content_list_type1) == len(resp_robot_com):
    #                     pass
    #                 else:
    #                     if content_list_type1:
    #                         sync_robot_list_type1 = []
    #                         for q_type1 in content_list_type1:
    #                             time.sleep(1)
    #                             resp_robot_type1 = \
    #                             Sync_robot.robot_uncalled(query_name=q_type1, queryType=3).json()['data'][
    #                                 'list']
    #                             if not resp_robot_type1:
    #                                 sync_robot_list_type1.append(q_type1)
    #                         if len(sync_robot_list_type1) == len(content_list_type1):
    #                             print(i, content_list_type1, '手机转移失败')
    #                         elif 0 < len(sync_robot_list_type1) < len(content_list_type1):
    #                             print(i, '部分手机号码转移出错', sync_robot_list_type1)
    #                         elif 0 == len(sync_robot_list_type1):
    #                             pass
    #                         else:
    #                             print('手机获取错误\n', contacts_num.request.body)
    #                     else:
    #                         user_Qu_type1 += 1
    #                         print(i, '手机为空', contacts_num_list, '\n', contacts_num.request.url)
    #
    #                     # if content_list_type2:
    #                     #     sync_robot_list_type2 = []
    #                     #     for q_type2 in content_list_type2:
    #                     #         time.sleep(1)
    #                     #         resp_robot_type2 = Sync_robot.robot_uncalled(query_name=q_type2, queryType=3).json()['data'][
    #                     #             'list']
    #                     #         if not resp_robot_type2:
    #                     #             sync_robot_list_type2.append(q_type2)
    #                     #     if len(sync_robot_list_type2) == len(content_list_type2):
    #                     #         print(i, content_list_type2, '固话转移失败')
    #                     #     elif 0 < len(sync_robot_list_type2) < len(content_list_type2):
    #                     #         print(i, '部分固话号码转移出错', sync_robot_list_type2)
    #                     #     elif 0 == len(sync_robot_list_type2):
    #                     #         pass
    #                     #     else:
    #                     #         print('固话获取错误\n', contacts_num.request.body)
    #                     # else:
    #                     #     user_Qu_type2 += 1
    #                     #     print(i, '固话为空', contacts_num_list, '\n', contacts_num.request.url)
    #             else:
    #                 user_Qu_test += 1
    #                 print(i, '企业转移失败', contacts_num_list, '\n', contacts_num.json())
    #             if user_Qu_type2 != 0 and user_Qu_type1 != 0:
    #                 user_Qu_test += 1
    #                 print(i, '该企业无联系方式', contacts_num_list, '\n', contacts_num.json())
    #             elif user_Qu_type1 != 0:
    #                 user_Qu_test += 1
    #                 print(i, '该企业无手机号码', contacts_num_list, '\n', contacts_num.json())
    #             elif user_Qu_type2 != 0:
    #                 print(i, '该企业无固话号码', contacts_num_list, '\n', contacts_num.json())
    #     else:
    #         pprint(resp_syn.request.body)
    #         pprint(resp_syn.request.headers)
    #         pprint(resp_syn.request.url)
    #     user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
    #     if pages is not None:
    #         print(user_Qu, user_Quota, pages)
    #         if user_Quota < pages:
    #             pprint(user.skb_userinfo().json())
    #         assert user_Qu == (user_Quota - pages + user_Qu_test) or user_Quota > user_Qu > (user_Quota - pages)
    #     else:
    #         print(user_Qu, user_Quota, len(resp_items))
    #         if user_Quota < len(resp_items):
    #             pprint(user.skb_userinfo().json())
    #         assert user_Qu == (user_Quota - len(resp_items) + user_Qu_test)
    #
    #     return '测试结束，全部号码，手机，扣除流量额度，测试仅手机转移case'

#
# if __name__ == '__main__':
#     pytest.main(["sync_robot_test.py::Test_sync_robot::test_case04", "-sq", "--alluredir",
#                  "../report/test_case05"])  # -s 打印输出,-sq简化打印
#     # os.system("allure serve ../report/temp")
#     os.system("allure generate ../report/test_case04 -o ../report/test_case04_html --clean")
# """f   用例失败
#    E   ERROR
#    。  成功的
# """
