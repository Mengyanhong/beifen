# @Time : 2021/9/9 18:56
# @Author : 孟艳红
# @File : sync_advanced_libs.py 高级搜索转移操作

import time
from pprint import pprint

import requests, json
from API_project.Configs.config_API import user
from API_project.Libs.robot_libs import Robotlist
from API_project.Libs.sync_robot_libs import Sync_robot

test_host = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境


class Sync_robot_test:
    def __init__(self, test_host):
        self.user = user(test_host)
        self.Robotlist = Robotlist(test_host)
        self.Sync_robot = Sync_robot(test_host)

    def case01(self): #扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划
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
        response = requests.post(url, headers=header, json=payload, verify=False) #搜索未查看，未转机器人的数据
        request_payload = response.request.body.decode("unicode_escape")
        request_payloa = json.loads(request_payload)
        resp_items = response.json()['data']['items']
        pid = []
        companyName = []
        # pprint(response.json())
        if resp_items != []:
            for i in range(len(resp_items)):
                pid.append(resp_items[i]['id'])
                companyName.append(resp_items[i]['companyName'])
        resp_sync = self.Sync_robot.sync(pids=pid, dataColumns=[0, 1], numberCount=1, seach_value=request_payloa,
                                         way='search_list').json()
        if resp_sync['error_code'] == 0:
            for i in range(20):
                time.sleep(2.2)
                response = requests.post(url, headers=header, json=payload, verify=False)
                if response.json()['data'] != {}:
                    break
            sync_sum = 0
            for i in companyName:
                resp_robot = self.Sync_robot.robot_uncalled(query_name=i)
                if resp_robot.json()['data']['list'] == []:
                    sync_sum+=1
                    print(i,'\n',resp_robot.json())
                assert len(resp_robot.json()['data']['list']) ==1
            if sync_sum >= len(companyName):
                print('转移失败')
        else:
            print('转移失败')
        return '测试结束'


if __name__ == '__main__':
    re = Sync_robot_test(test_host).case01()
    print(re)
    # print(re.request.body.decode("unicode_escape"))
    # print(re.request.url)
    # print(re.request.headers)
