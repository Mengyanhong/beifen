# @Time : 2021/9/9 18:56
# @Author : 孟艳红
# @File : sync_robot_search_libs.py 高级搜索转移操作

import time
from pprint import pprint

import requests, json
from API_project.Configs.config_API import user
# from API_project.Libs.robot_libs import Robotlist
from API_project.Configs.search_API import search
from API_project.Libs.sync_robot_libs import Sync_robot

test_host = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环

class Sync_robot_test:
    def __init__(self, test_host):
        self.user = user(test_host)
        # self.Robotlist = Robotlist(test_host)
        self.Sync_robot = Sync_robot(test_host)
        self.search = search(test_host)

    def case01(self, way='search_list'):  # 扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划
        if way == 'search_list':
            response = self.search.skb_search()  # 搜索未查看，未转机器人的数据
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        resp_items = response.json()['data']['items']
        pid = []
        companyName = []
        resp_companyName_list =[]
        if resp_items != []:
            for i in range(len(resp_items)):
                pid.append(resp_items[i]['id'])
                companyName.append(resp_items[i]['companyName'])
                resp_companyName_list.append({'pid':resp_items[i]['id'],'company_name':resp_items[i]['companyName']})
        resp_sync = self.Sync_robot.sync(pids=pid, dataColumns=[0, 1],canCover=True, numberCount=1, seach_value=request_payloa,
                                         way=way).json()
        if resp_sync['error_code'] == 0:
            for i_value in range(20):
                time.sleep(2.2)
                if way == 'search_list':
                    response_sum = self.search.skb_search()
                print(response_sum.json()['data'])
                if response_sum.json()['data'] != {}:
                    break
            sync_sum = 0
            for i in resp_companyName_list:
                resp_robot = self.Sync_robot.robot_uncalled(query_name=i['company_name'])
                resp_robot_phone_list =resp_robot.json()['data']['list']
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
        assert user_Qu == user_Quota - len(resp_items)
        return '测试结束，未查看数据选择扣点且仅转移一条号码case'

    def case02(self):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
        url = f'https://{self.user.skb_Host()}/api_skb/v1/search'
        payload = {"keyword": "北京",
                   "filter": {"location": [], "industryshort": [], "secindustryshort": [], "registercapital": [],
                              "establishment": [], "entstatus": [], "contact": [], "sortBy": "0", "companysource": [],
                              "enttype": [0], "employees": [0], "hasrecruit": "0", "hassem": "0", "haswebsite": "0",
                              "hastrademark": "0", "haspatent": "0", "hastender": "0", "haswechataccnt": "0",
                              "filterUnfold": 2, "filterSync": 0, "filterSyncRobot": 1, "hasBuildingCert": "0",
                              "isHighTech": "0", "hasFinanceInfo": "0", "hasAbnormalInfo": "0",
                              "syncRobotRangeDate": []}, "scope": "companyname", "matchType": "most_fields",
                   "pagesize": 10, "page": 1}
        header = self.user.shop_headers()
        response = requests.post(url, headers=header, json=payload, verify=False)  # 搜索未查看，未转机器人的数据
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        resp_items = response.json()['data']['items']
        pid = []
        companyName = []
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        if resp_items != []:
            for i in range(len(resp_items)):
                pid.append(resp_items[i]['id'])
                companyName.append(resp_items[i]['companyName'])
        resp_sync = self.Sync_robot.sync(pids=pid, dataColumns=[0, 1], Quota=False, numberCount=1,
                                         seach_value=request_payloa,
                                         way='search_list').json()
        if resp_sync['error_code'] == 0:
            for i in range(20):
                time.sleep(2.2)
                response = requests.post(url, headers=header, json=payload, verify=False)
                if response.json()['data'] != {}:
                    break
            sync_sum = 0
            user_Qu = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
            assert user_Qu == user_Quota
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
        return '测试结束,未查看数据选择不扣除流量额度测试'

    def case03(self):  # 扣除流量额度，转移手机和固话，全部号码,不创建外呼计划，
        url = f'https://{self.user.skb_Host()}/api_skb/v1/search'
        payload = {"keyword": "上海",
                   "filter": {"location": [], "industryshort": [], "secindustryshort": [], "registercapital": [],
                              "establishment": [], "entstatus": [], "contact": [2], "sortBy": "0", "companysource": [],
                              "enttype": [0], "employees": [0], "hasrecruit": "0", "hassem": "0", "haswebsite": "0",
                              "hastrademark": "0", "haspatent": "0", "hastender": "0", "haswechataccnt": "0",
                              "filterUnfold": 2, "filterSync": 1, "filterSyncRobot": 1, "hasBuildingCert": "0",
                              "isHighTech": "0", "hasFinanceInfo": "0", "hasAbnormalInfo": "0",
                              "syncRobotRangeDate": []}, "scope": "companyname", "matchType": "most_fields",
                   "pagesize": 10, "page": 1}
        header = self.user.shop_headers()
        response = requests.post(url, headers=header, json=payload, verify=False)  # 搜索未查看，未转机器人的数据，有固话
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        resp_items = response.json()['data']['items']
        pid = []
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        if resp_items != []:
            for i in range(len(resp_items)):
                pid.append(resp_items[i]['id'])
        resp_sync = self.Sync_robot.sync(pids=pid, dataColumns=[0, 1],
                                         seach_value=request_payloa,
                                         way='search_list').json()
        if resp_sync['error_code'] == 0:
            for i_value in range(20):
                time.sleep(2.2)
                response = requests.post(url, headers=header, json=payload, verify=False)
                if response.json()['data'] != {}:
                    break

            user_Qu = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
            assert user_Qu == user_Quota - len(resp_items)
            for i in pid:
                contacts_num = self.search.skb_contacts_num(pid=i)
                contacts_num_list = contacts_num.json()['data']['contacts']
                content_list = []
                for j in contacts_num_list:
                    if j['type'] == 2 or j['type'] == 1:
                        content_list.append(j['content'])
                sync_sum = 0
                for q in content_list:
                    time.sleep(1)
                    resp_robot = self.Sync_robot.robot_uncalled(query_name=q, queryType=3)
                    if resp_robot.json()['data']['list'] == []:
                        sync_sum += 1
                        print(i + '，转移失败' + q + '\n')
                    else:
                        # print(i + '，转移成功\n', resp_robot.json())
                        # print(len(resp_robot.json()['data']['list']))
                        assert len(resp_robot.json()['data']['list']) >= 1
                if sync_sum != 0:
                    print(i + '测试失败')
        else:
            print('转移失败')
        return '测试结束，全部号码，手机加固话，扣除流量额度，测试固话转移case'

    def case04(self):  # 扣除流量额度，转移手机和固话，全部号码,不创建外呼计划，
        url = f'https://{self.user.skb_Host()}/api_skb/v1/search'
        payload = {"keyword": "上海",
                   "filter": {"location": [], "industryshort": [], "secindustryshort": [], "registercapital": [],
                              "establishment": [], "entstatus": [], "contact": [1], "sortBy": "0", "companysource": [],
                              "enttype": [0], "employees": [0], "hasrecruit": "0", "hassem": "0", "haswebsite": "0",
                              "hastrademark": "0", "haspatent": "0", "hastender": "0", "haswechataccnt": "0",
                              "filterUnfold": 2, "filterSync": 0, "filterSyncRobot": 1, "hasBuildingCert": "0",
                              "isHighTech": "0", "hasFinanceInfo": "0", "hasAbnormalInfo": "0",
                              "syncRobotRangeDate": []}, "scope": "companyname", "matchType": "most_fields",
                   "pagesize": 10, "page": 1}
        header = self.user.shop_headers()
        response = requests.post(url, headers=header, json=payload, verify=False)  # 搜索未查看，未转机器人的数据，有固话
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        resp_items = response.json()['data']['items']
        pid = []
        company_name_list_pid = []
        user_Quota = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
        if resp_items != []:
            for i in range(len(resp_items)):
                pid.append(resp_items[i]['id'])
                company_name_list_pid.append({'pid':resp_items[i]['id'],'company_name':resp_items[i]['companyName']})
        resp_sync = self.Sync_robot.sync(pids=pid, dataColumns=[0],
                                         seach_value=request_payloa,canCover=True,
                                         way='search_list').json()
        user_Qu_type1 = 0
        if resp_sync['error_code'] == 0:
            for data_value in range(20):
                time.sleep(2.2)
                response = requests.post(url, headers=header, json=payload, verify=False)
                if response.json()['data'] != {}:
                    break
            for i in company_name_list_pid:
                contacts_num = self.search.skb_contacts_num(pid=i['pid'])
                contacts_num_list = contacts_num.json()['data']['contacts']
                content_list = []
                content_list_type1 = []
                for j in contacts_num_list:
                    if j['type'] == 2:
                        content_list.append(j['content'])
                    elif j['type'] == 1:
                        content_list_type1.append(j['content'])
                sync_sum = 0
                for q in content_list:
                    time.sleep(1)
                    resp_robot = self.Sync_robot.robot_uncalled(query_name=q, queryType=3)
                    resp_robot_phone_list = resp_robot.json()['data']['list']
                    if resp_robot_phone_list == []:
                        sync_sum += 1
                        # print(i + '，转移失败'+q+'\n')
                    else:
                        company_name_sum =0
                        for company_name in resp_robot_phone_list:
                            if company_name['company_name'] == i['company_name']:
                                company_name_sum +=1
                            else:
                                continue
                        if company_name_sum == 0:
                            sync_sum += 1
                        else:
                            print(i , '，转移失败' + q + '\n', resp_robot.json())
                if sync_sum != len(content_list):
                    print(i ,'测试失败')
                if content_list_type1 == []:
                    user_Qu_type1+=1
            user_Qu = self.user.skb_userinfo(headers=self.user.shop_headers()).json()['data']['uRemainQuota']
            # print(user_Qu)
            # print(user_Quota)
            # print(len(resp_items))
            assert user_Qu == (user_Quota - len(resp_items) + user_Qu_type1)
        else:
            print('转移失败')
        return '测试结束，全部号码，手机，扣除流量额度，测试仅手机转移case'


if __name__ == '__main__':
    re = Sync_robot_test(test_host).case01()
    print(re)
    # print(re.request.body.decode("unicode_escape"))
    # print(re.request.url)
    # print(re.request.headers)
