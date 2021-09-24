# @Time : 2021/9/9 17:31
# @Author : 孟艳红
# @File : sync_robot_test.py

from pprint import pprint
import requests, json, time,pytest,os
from API_project.Configs.config_API import user
from API_project.Configs.search_API import search
from API_project.Configs.shop_API import shop
from API_project.Libs.sync_robot_libs import Sync_robot

test_host = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环

user = user(test_host)
Sync_robot = Sync_robot(test_host)
search = search(test_host)
shop = shop(test_host)
class Test_sync_robot:
    # @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', None , 'shop_search_list'])
    # @pytest.mark.parametrize('page', [None, 500, 1000, 2000])

    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def testcase01(self, way, page):  # 扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划
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
        resp_companyName_list = []
        if resp_items:
            for i in range(len(resp_items)):
                pid_list.append(resp_items[i]['id'])
                resp_companyName_list.append(
                    {'pid': resp_items[i]['id'], 'company_name': resp_items[i][list_companyName_add]})
        resp_sync = Sync_robot.sync(pids=pid, pages=pages, dataColumns=[0, 1],  numberCount=1,
                                         seach_value=request_payloa,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
            for i_value in range(200):
                time.sleep(3)
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
                        print(i, '转移失败,该企业有联系方式\n', content_list, content_list_type1)
                        # assert not content_list and not content_list_type1
                    else:
                        print(i, '搜索出错，该企业无联系方式')
                else:
                    company_name_sum = 0
                    for company_name in resp_robot_phone_list:
                        if company_name['company_name'] == i['company_name']:
                            company_name_sum += 1
                        else:
                            continue
                    if company_name_sum != 1:
                        print(i, '，转移号码数量错误\n', resp_robot_phone_list)
            assert sync_sum < len(resp_companyName_list)
        user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
        if pages is not None:
            assert user_Qu == (user_Quota - pages) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            print(user_Qu, user_Quota, len(resp_companyName_list))
            assert user_Qu == (user_Quota - len(resp_companyName_list))
        return '测试结束，未查看数据选择扣点且仅转移一条号码case'

    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def testcase02(self, way, page):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
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
        resp_companyName_list = []
        if resp_items:
            for i in range(len(resp_items)):
                pid_list.append(resp_items[i]['id'])
                resp_companyName_list.append(
                    {'pid': resp_items[i]['id'], 'company_name': resp_items[i][list_companyName_add]})
        resp_sync = Sync_robot.sync(pids=pid, pages=pages, dataColumns=[0, 1], Quota=False, numberCount=1,
                                         seach_value=request_payloa,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
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
                print(response_sum['data'])
                if response_sum['data'] != {}:
                    break
            user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
            sync_sum = 0
            for i in resp_companyName_list:
                resp_robot = Sync_robot.robot_uncalled(query_name=i['company_name']).json()['data']['list']
                if resp_robot:
                    sync_sum += 1
                    print(i, '企业被成功转移，测试失败\n', resp_robot)
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

    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def testcase03(self, way, page):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，仅转移已查看数据
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客,'shop_search_list':找店铺
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        if way == 'search_list':
            response = search.skb_search(filterUnfold=1)
            list_companyName_add = 'companyName'
        elif way == 'advanced_search_list':
            response = search.advanced_search(hasUnfolded=1)
            list_companyName_add = 'companyName'
        elif way == 'shop_search_list':
            response = shop.search_shop(hasSyncClue=0, hasUnfolded=1, cv=[
                {"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": []}, "cr": "IN"},
                {"cn": "contactType", "cv": ["1", "2"], "cr": "IN"}])
            list_companyName_add = 'name'
        else:
            response = search.skb_address_search(filterUnfold=1)
            list_companyName_add = 'companyName'

        user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
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
        companyName = []
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
                companyName.append(i[list_companyName_add])
        resp_sync = Sync_robot.sync(pids=pid, pages=pages, canCover=True, dataColumns=[0, 1], Quota=False,
                                         numberCount=1,
                                         seach_value=request_payloa,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
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
                print(response_sum.json()['data'])
                if response_sum.json()['data'] != {}:
                    break
                response_sum.close()
            sync_sum = 0
            for i in companyName:
                resp_robot = Sync_robot.robot_uncalled(query_name=i).json()
                if not resp_robot['data']['list']:
                    sync_sum += 1
                else:
                    assert len(resp_robot['data']['list']) >= 1
            if sync_sum == len(companyName):
                print('测试失败')
                assert sync_sum != len(companyName)
            else:
                assert 0 <= sync_sum < len(companyName)
        else:
            print('转移失败')
        user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
        assert user_Qu == user_Quota
        return '测试结束,仅转移已查看数据选择不扣除流量额度测试仅1条号码'

    @pytest.mark.parametrize('way', ['advanced_search_list','shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def test_case04(self,way,page):  # 扣除流量额度，转移手机和固话，全部号码,不创建外呼计划，
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
        resp_sync=resp_syn.json()
        if resp_sync['error_code'] == 0:
            print(time.time())
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
                    print(time.time())
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
                            print(i,content_list,'号码转移错误')
                        elif 0 < len(sync_robot_list) < len(content_list):
                            print(i,'部分号码转移出错',sync_robot_list)
                        elif 0 == len(sync_robot_list):
                            pass
                        else:
                            print('号码出错''\n',contacts_num.request.body)
                    else:
                        print(i,'联系方式为空',contacts_num_list,'\n',contacts_num.request.url)
                else:
                    print(i, '企业转移失败',contacts_num_list,'\n',contacts_num.json())
        else:
            pprint(resp_syn.request.body)
            pprint(resp_syn.request.headers)
            pprint(resp_syn.request.url)
        user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']

        if pages is not None:
            print(user_Qu, user_Quota, pages)
            if user_Quota<pages:
                print(user_Qu, user_Quota, pages)
                pprint(user.skb_userinfo().json())
            assert user_Qu == (user_Quota - pages) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            print(user_Qu, user_Quota, len(resp_items))
            if user_Quota<len(resp_items):
                print(user_Qu, user_Quota, len(resp_items))
                pprint(user.skb_userinfo().json())
            assert user_Qu == (user_Quota - len(resp_items))
        return '测试结束，全部号码，手机加固话，扣除流量额度，测试全部号码/固话转移case'

    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def testcase05(self, way, page):  # 扣除流量额度，转移手机和固话，全部号码,不创建外呼计划，
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
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
            print('搜索结果为空', response_value['data'])
            assert response_value['total'] != 0
        else:
            response_value = response_value
        resp_items = response_value['data']['items']
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
        user_Quota = user.skb_userinfo().json()['data']['uRemainQuota']
        if resp_items:
            for i in range(len(resp_items)):
                pid_list.append(resp_items[i]['id'])
                company_name_list_pid.append(
                    {'pid': resp_items[i]['id'], 'company_name': resp_items[i][list_companyName_add]})
        resp_sync = Sync_robot.sync(pids=pid, pages=pages,
                                         seach_value=request_payloa, canCover=True,
                                         way='search_list').json()
        user_Qu_type1 = 0
        if resp_sync['error_code'] == 0:
            for data_value in range(200):
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
                    break
            for i in company_name_list_pid:
                contacts_num_list = search.skb_contacts_num(id=i['pid'], module=way).json()['data']['contacts']
                content_list = []
                content_list_type1 = []
                for j in contacts_num_list:
                    if j['type'] == 2:
                        content_list.append(j['content'])
                    elif j['type'] == 1:
                        content_list_type1.append(j['content'])
                if content_list:
                    sync_sum = 0
                    for q in content_list:
                        time.sleep(1)
                        resp_robot = Sync_robot.robot_uncalled(query_name=q, queryType=3).json()
                        resp_robot_phone_list = resp_robot['data']['list']
                        resp_robot_data = resp_robot['data']
                        if resp_robot_phone_list:
                            sync_sum += 1
                        else:
                            company_name_sum = 0
                            for company_name in resp_robot_phone_list:
                                if company_name['company_name'] == i['company_name']:
                                    company_name_sum += 1
                                else:
                                    continue
                            if company_name_sum == 0:
                                sync_sum += 1
                            else:
                                print(i, '，转移失败' + q, company_name_sum, '\n', resp_robot_data)
                    if sync_sum != len(content_list):
                        print(i, '测试失败')
                        print(len(content_list))
                        print(sync_sum)
                        assert sync_sum == len(content_list)
                if not content_list_type1:
                    user_Qu_type1 += 1
                    print(i, '无手机号码')
                else:
                    phon_list = 0
                    for phon in content_list_type1:
                        time.sleep(1.5)
                        resp_robot = Sync_robot.robot_uncalled(query_name=phon, queryType=3).json()
                        resp_robot_phone_list = resp_robot['data']['list']
                        resp_robot_data = resp_robot['data']
                        if not resp_robot_phone_list:
                            phon_list += 1
                            print(i, '，转移失败' + phon + '\n', resp_robot_data)

                    assert phon_list < len(content_list_type1)
        else:
            print('转移失败')
        user_Qu = user.skb_userinfo().json()['data']['uRemainQuota']
        # print(user_Qu)
        # print(user_Quota)
        # print(len(resp_items))
        if pages is not None:
            assert user_Qu == (user_Quota - pages + user_Qu_type1) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            assert user_Qu == (user_Quota - len(resp_items) + user_Qu_type1)

        return '测试结束，全部号码，手机，扣除流量额度，测试仅手机转移case'

    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def testcase06(self, way, page):  # 扣除流量额度，转移手机和固话，全部号码,创建外呼计划，
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        if way == 'search_list':
            response = search.skb_search()
            list_companyName_add = 'companyName'
        elif way == 'advanced_search_list':
            response = search.advanced_search()
            list_companyName_add = 'companyName'
        elif way == 'shop_search_list':
            response = shop.search_shop(cv=[
                {"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": []}, "cr": "IN"},
                {"cn": "contactType", "cv": ["1", "2"], "cr": "IN"}])
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
        user_Quota = user.skb_userinfo(headers=user.shop_headers()).json()['data']['uRemainQuota']
        resp_items = response_value['data']['items']
        if resp_items:
            for i in resp_items:
                pid_list.append(i['id'])
                company_name_list_pid.append(
                    {'pid': i['id'], 'company_name': i[list_companyName_add]})
        resp_sync = Sync_robot.sync(pids=pid, pages=pages, canCover=True, dataColumns=[0, 1],
                                         seach_value=request_payloa,needCallPlan=True,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
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
                    break
            for i in company_name_list_pid:
                contacts_num_list = search.skb_contacts_num(id=i['pid'], module=way).json()['data']['contacts']
                content_list = []
                for j in contacts_num_list:
                    if j['type'] == 2 or j['type'] == 1:
                        content_list.append(j['content'])
                if content_list:
                    sync_sum = 0
                    for q in content_list:
                        time.sleep(1.5)
                        resp_robot = Sync_robot.robot_uncalled(query_name=q, queryType=3).json()['data']['list']
                        if not resp_robot:
                            resp_robot_com = \
                            Sync_robot.robot_uncalled(query_name=i['company_name'], queryType=2).json()['data'][
                                'list']
                            if not resp_robot_com:
                                sync_sum += 1
                                print(i, '，转移失败' + q)
                        else:
                            assert len(resp_robot) >= 1
                    assert sync_sum < len(content_list)
                else:
                    print(i, '无联系方式')
        else:
            print('转移失败')
        user_Qu = user.skb_userinfo(headers=user.shop_headers()).json()['data']['uRemainQuota']
        if pages is not None:
            assert user_Qu == (user_Quota - pages) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            assert user_Qu == (user_Quota - len(resp_items))
        return '测试结束，全部号码，手机加固话，扣除流量额度，测试全部号码/固话转移case'



if __name__ == '__main__':
    pytest.main(["sync_robot_test.py::Test_sync_robot::test_case04", "-sq", "--alluredir",
                 "../report/test_case05"])  # -s 打印输出,-sq简化打印
    # os.system("allure serve ../report/temp")
    os.system("allure generate ../report/test_case04 -o ../report/test_case04_html --clean")
"""f   用例失败
   E   ERROR
   。  成功的
"""