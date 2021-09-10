# @Time : 2021/9/9 18:56
# @Author : 孟艳红
# @File : sync_advanced_libs.py 高级搜索转移操作
# def __init__(self, environment):
#     self.User = user(environment)
#
# def sync(self, pids=None, pages=None, seach_value=None, Quota=True, dataColumns=None, phoneStatus=None,
#          numberCount=0, needCallPlan=False, way=None):
#     true = True
#     false = False
#     if phoneStatus is None:
#         phone = [0, 1, 2, 3]
#     else:
#         phone = phoneStatus
#     if dataColumns is None:
#         dataColumn = [0]
#     else:
#         dataColumn = dataColumns
#     url = f'https://{self.User.robot_Host()}/api_skb/v1/clues/sync_robot'
#     payload = {
#         "from": "syncRobot",
#         "useQuota": Quota,  # 是否使用额度
#         "dataColumns": dataColumn,  # 数据字段[0, 1] // 0: 手机，1：固话
#         "phoneStatus": phone,  # 手机过滤 [0, 1, 2 , 3] //[0, 1, 3]: 过滤疑似代理记账号码 [0, 1, 2]: 过滤异常号码
#         "numberCount": numberCount,  # 号码数量 0: 全部,1: 第一条
#         "canCover": false,
#         "needCallPlan": needCallPlan,  # 是否需要创建外呼计划 true / false
#     }
#     if way is not None:
#         payload.update({"way": way})
#     payload.update(seach_value)
#     if pids is None:
#         payload.update({"page": 1, "pagesize": pages})
#     else:
#         payload.update({"pids": pids, })
#         payload.pop('page', 'pagesize')
#
#     heade = self.User.shop_headers()
#     response = requests.post(url=url, headers=heade, json=payload)
#     return response
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
        response = requests.post(url, headers=header, json=payload, verify=False)
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
