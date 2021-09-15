# @Time : 2021/9/9 18:56
# @Author : 孟艳红
# @File : sync_robot_search_libs.py 高级搜索转移操作


from pprint import pprint
import requests, json, time
from API_project.Configs.config_API import user
from API_project.Configs.search_API import search
from API_project.Libs.sync_robot_libs import Sync_robot

test_host = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环


class Sync_robot_test:
    def __init__(self, test_host):
        self.user = user(test_host)
        self.Sync_robot = Sync_robot(test_host)
        self.search = search(test_host)

    def case01(self, way=None, page=None):  # 扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """

        if way == 'search_list':
            response = self.search.skb_search()  # 搜索未查看，未转机器人的数据
        elif way == 'advanced_search_list':
            response = self.search.advanced_search()
        else:
            response = self.search.skb_address_search()
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        if response.json()['data'] == {}:
            print(response.json()['message'])
            assert response.json()['data'] != {}
        resp_items = response.json()['data']['items']
        pid_list = []
        companyName = []
        resp_companyName_list = []
        if resp_items != []:
            for i in range(len(resp_items)):
                pid_list.append(resp_items[i]['id'])
                companyName.append(resp_items[i]['companyName'])
                resp_companyName_list.append({'pid': resp_items[i]['id'], 'company_name': resp_items[i]['companyName']})
        if way is None:
            pid = None
            pages = 500
        elif page is None:
            pid = pid_list
            pages = None
        else:
            pid = None
            pages = page
        resp_sync = self.Sync_robot.sync(pids=pid, pages=pages, dataColumns=[0, 1], canCover=True, numberCount=1,
                                         seach_value=request_payloa,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
            for i_value in range(200):
                time.sleep(3)
                if way == 'search_list':
                    response_sum = self.search.skb_search()  # 搜索未查看，未转机器人的数据
                elif way == 'advanced_search_list':
                    response_sum = self.search.advanced_search()
                else:
                    response_sum = self.search.skb_address_search()
                print(response_sum.json()['data'])
                if response_sum.json()['data'] != {}:
                    break
            sync_sum = 0
            for i in resp_companyName_list:
                resp_robot = self.Sync_robot.robot_uncalled(query_name=i['company_name'])
                resp_robot_phone_list = resp_robot.json()['data']['list']
                if resp_robot_phone_list == []:
                    sync_sum += 1
                    print(i['company_name'], '，转移失败\n', resp_robot.json())
                else:
                    company_name_sum = 0
                    for company_name in resp_robot_phone_list:
                        if company_name['company_name'] == i['company_name']:
                            company_name_sum += 1
                        else:
                            continue
                    if company_name_sum != 1:
                        print(i['company_name'] + '，转移号码数量错误\n', resp_robot.json())
            assert sync_sum != len(companyName)
        else:
            print('转移失败')
        user_Qu = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        if pages is not None:
            assert user_Qu == (user_Quota - pages) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            assert user_Qu == user_Quota - len(resp_items)
        return '测试结束，未查看数据选择扣点且仅转移一条号码case'

    def case02(self, way=None, page=None):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        if way == 'search_list':
            response = self.search.skb_search()  # 搜索未查看，未转机器人的数据
        elif way == 'advanced_search_list':
            response = self.search.advanced_search()
        else:
            response = self.search.skb_address_search()
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        if response.json()['data'] == {}:
            print(response.json()['data'])
            assert response.json()['data'] != {}
        resp_items = response.json()['data']['items']
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
        if resp_items != []:
            for i in range(len(resp_items)):
                pid_list.append(resp_items[i]['id'])
                companyName.append(resp_items[i]['companyName'])
        resp_sync = self.Sync_robot.sync(pids=pid, pages=pages, dataColumns=[0, 1], Quota=False, numberCount=1,
                                         seach_value=request_payloa,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
            for i in range(200):
                time.sleep(2.2)
                if way == 'search_list':
                    response_sum = self.search.skb_search()  # 搜索未查看，未转机器人的数据
                elif way == 'advanced_search_list':
                    response_sum = self.search.advanced_search()
                else:
                    response_sum = self.search.skb_address_search()
                if response_sum.json()['data'] != {}:
                    break
            sync_sum = 0
            for i in companyName:
                resp_robot = self.Sync_robot.robot_uncalled(query_name=i)
                if resp_robot.json()['data']['list'] == []:
                    sync_sum += 1
                else:
                    print(i + '，转移成功\n', resp_robot.json())
                    assert len(resp_robot.json()['data']['list']) == 1
            if sync_sum == len(companyName):
                print('测试通过')
            else:
                print('测试失败')
                assert sync_sum == len(companyName)
        else:
            print('转移失败')
        user_Qu = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        assert user_Qu == user_Quota
        return '测试结束,未查看数据选择不扣除流量额度测试'

    def case03(self, way=None, page=None):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，仅转移已查看数据
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        if way == 'search_list':
            response = self.search.skb_search(filterUnfold=1)  # 搜索已查看，未转机器人的数据
        elif way == 'advanced_search_list':
            response = self.search.advanced_search(hasUnfolded=1)
        else:
            response = self.search.skb_address_search(filterUnfold=1)
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        if response.json()['data'] == {}:
            print(response.json()['data'])
            assert response.json()['data'] != {}
        resp_items = response.json()['data']['items']
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
        if resp_items != []:
            for i in range(len(resp_items)):
                pid_list.append(resp_items[i]['id'])
                companyName.append(resp_items[i]['companyName'])
        resp_sync = self.Sync_robot.sync(pids=pid, pages=pages, canCover=True, dataColumns=[0, 1], Quota=False,
                                         numberCount=1,
                                         seach_value=request_payloa,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
            for i in range(200):
                time.sleep(2.2)
                if way == 'search_list':
                    response_sum = self.search.skb_search(filterUnfold=1)  # 搜索未查看，未转机器人的数据
                elif way == 'advanced_search_list':
                    response_sum = self.search.advanced_search(hasUnfolded=1)
                else:
                    response_sum = self.search.skb_address_search(filterUnfold=1)
                print(response_sum.json()['data'])
                if response_sum.json()['data'] != {}:
                    break
            sync_sum = 0
            for i in companyName:
                resp_robot = self.Sync_robot.robot_uncalled(query_name=i)
                if resp_robot.json()['data']['list'] == []:
                    sync_sum += 1
                else:
                    # print(i + '，转移成功\n', resp_robot.json())
                    assert len(resp_robot.json()['data']['list']) >= 1
            if sync_sum == len(companyName):
                print('测试失败')
                assert sync_sum != len(companyName)
            else:
                assert 0 <= sync_sum < len(companyName)
        else:
            print('转移失败')
        user_Qu = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        assert user_Qu == user_Quota
        return '测试结束,仅转移已查看数据选择不扣除流量额度测试仅1条号码'

    def case04(self, way=None, page=None):  # 扣除流量额度，转移手机和固话，全部号码,不创建外呼计划，
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        if way == 'search_list':
            response = self.search.skb_search()
        elif way == 'advanced_search_list':
            response = self.search.advanced_search()
        else:
            response = self.search.skb_address_search(contact=2)
        # 搜索未查看，未转机器人的数据，有固话
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        if response.json()['data'] == {}:
            print(response.json()['data'])
            assert response.json()['data'] != {}
        resp_items = response.json()['data']['items']
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
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        if resp_items != []:
            for i in range(len(resp_items)):
                pid_list.append(resp_items[i]['id'])
                company_name_list_pid.append({'pid': resp_items[i]['id'], 'company_name': resp_items[i]['companyName']})
        resp_sync = self.Sync_robot.sync(pids=pid, pages=pages, canCover=True, dataColumns=[0, 1],
                                         seach_value=request_payloa,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
            for i_value in range(200):
                time.sleep(2.2)
                if way == 'search_list':
                    response_list = self.search.skb_search()
                elif way == 'advanced_search_list':
                    response_list = self.search.advanced_search()
                else:
                    response_list = self.search.skb_address_search(contact=2)
                if response_list.json()['data'] != {}:
                    break
            for i in company_name_list_pid:
                contacts_num = self.search.skb_contacts_num(pid=i['pid'])
                contacts_num_list = contacts_num.json()['data']['contacts']
                content_list = []
                for j in contacts_num_list:
                    if j['type'] == 2 or j['type'] == 1:
                        content_list.append(j['content'])
                if content_list != []:
                    sync_sum = 0
                    for q in content_list:
                        time.sleep(1.5)
                        resp_robot = self.Sync_robot.robot_uncalled(query_name=q, queryType=3)
                        if resp_robot.json()['data']['list'] == []:
                            resp_robot_com = self.Sync_robot.robot_uncalled(query_name=i['company_name'], queryType=2)
                            if resp_robot_com.json()['data']['list'] == []:
                                sync_sum += 1
                                print(i, '，转移失败' + q)
                        else:
                            assert len(resp_robot.json()['data']['list']) >= 1
                    assert sync_sum < len(content_list)
                else:
                    print(i, '无联系方式')
        else:
            print('转移失败')
        user_Qu = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        if pages is not None:
            assert user_Qu == (user_Quota - pages) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            assert user_Qu == (user_Quota - len(resp_items))
        return '测试结束，全部号码，手机加固话，扣除流量额度，测试全部号码/固话转移case'

    def case05(self, way=None, page=None):  # 扣除流量额度，转移手机和固话，全部号码,不创建外呼计划，
        """
        :param way: 测试模块'search_list'：找企业, 'advanced_search_list'：高级搜索, None：地图获客
        :param page: None：转移所选, 500：转前500, 1000：转前1000, 2000：转前2000
        :return:
        """
        if way == 'search_list':
            response = self.search.skb_search()
        elif way == 'advanced_search_list':
            response = self.search.advanced_search()
        else:
            response = self.search.skb_address_search()  # 搜索未查看，未转机器人的数据，有固话
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        if response.json()['data'] == {}:
            print(response.json()['data'])
            assert response.json()['data'] != {}
        resp_items = response.json()['data']['items']
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
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        if resp_items != []:
            for i in range(len(resp_items)):
                pid_list.append(resp_items[i]['id'])
                company_name_list_pid.append({'pid': resp_items[i]['id'], 'company_name': resp_items[i]['companyName']})
        resp_sync = self.Sync_robot.sync(pids=pid, pages=pages,
                                         seach_value=request_payloa, canCover=True,
                                         way='search_list').json()
        user_Qu_type1 = 0
        if resp_sync['error_code'] == 0:
            for data_value in range(200):
                time.sleep(2.2)
                if way == 'search_list':
                    response_list = self.search.skb_search()
                elif way == 'advanced_search_list':
                    response_list = self.search.advanced_search()
                else:
                    response_list = self.search.skb_address_search()
                if response_list.json()['data'] != {}:
                    break
            for i in company_name_list_pid:
                contacts_num = self.search.skb_contacts_num(id=i['pid'])
                contacts_num_list = contacts_num.json()['data']['contacts']
                content_list = []
                content_list_type1 = []
                for j in contacts_num_list:
                    if j['type'] == 2:
                        content_list.append(j['content'])
                    elif j['type'] == 1:
                        content_list_type1.append(j['content'])
                if content_list != []:
                    sync_sum = 0
                    for q in content_list:
                        time.sleep(1)
                        resp_robot = self.Sync_robot.robot_uncalled(query_name=q, queryType=3)
                        resp_robot_phone_list = resp_robot.json()['data']['list']
                        resp_robot_data = resp_robot.json()['data']
                        if resp_robot_phone_list == []:
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
                if content_list_type1 == []:
                    user_Qu_type1 += 1
                    print(i, '无手机号码')
                else:
                    phon_list = 0
                    for phon in content_list_type1:
                        time.sleep(1.5)
                        resp_robot = self.Sync_robot.robot_uncalled(query_name=phon, queryType=3)
                        resp_robot_phone_list = resp_robot.json()['data']['list']
                        resp_robot_data = resp_robot.json()['data']
                        if resp_robot_phone_list == []:
                            phon_list += 1
                            print(i, '，转移失败' + phon + '\n', resp_robot_data)

                    assert phon_list < len(content_list_type1)
        else:
            print('转移失败')
        user_Qu = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        # print(user_Qu)
        # print(user_Quota)
        # print(len(resp_items))
        if pages is not None:
            assert user_Qu == (user_Quota - pages + user_Qu_type1) or user_Quota > user_Qu > (user_Quota - pages)
        else:
            assert user_Qu == (user_Quota - len(resp_items) + user_Qu_type1)

        return '测试结束，全部号码，手机，扣除流量额度，测试仅手机转移case'


if __name__ == '__main__':
    re = Sync_robot_test(test_host).case01()
    print(re)
    # print(re.request.body.decode("unicode_escape"))
    # print(re.request.url)
    # print(re.request.headers)
