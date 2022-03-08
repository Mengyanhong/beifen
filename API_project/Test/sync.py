# -*- coding: utf-8 -*-
# @Time : 2021/9/9 15:11
# @Author : 孟艳红
# @File : sync.py
# -*- coding: utf-8 -*-
import requests
from API_project.Configs.Configuration import user


class Sync_robot:
    def __init__(self, environment):
        self.User = user(environment)

    def sync(self, pids=None, pages=None, seach_value=None, Quota=True, dataColumns=None, phoneStatus=None,
             numberCount=0, needCallPlan=False, way=None):
        true = True
        false = False
        if phoneStatus is None:
            phone = [0, 1, 2, 3]
        else:
            phone = phoneStatus
        if dataColumns is None:
            dataColumn = [0]
        else:
            dataColumn = dataColumns
        url = f'https://{self.User.robot_Host()}/api_skb/v1/clues/sync_robot'
        payload = {
            "from": "syncRobot",
            "useQuota": Quota,  # 是否使用额度
            "dataColumns": dataColumn,  # 数据字段[0, 1] // 0: 手机，1：固话
            "phoneStatus": phone,  # 手机过滤 [0, 1, 2 , 3] //[0, 1, 3]: 过滤疑似代理记账号码 [0, 1, 2]: 过滤异常号码
            "numberCount": numberCount,  # 号码数量 0: 全部,1: 第一条
            "canCover": false,
            "needCallPlan": needCallPlan,  # 是否需要创建外呼计划 true / false
        }
        if way is not None:
            payload.update({"way": way})
        payload.update(seach_value)
        if pids is None:
            payload.update({"page": 1, "pagesize": pages})
        else:
            payload.update({"pids": pids, })
            payload.pop('page', 'pagesize')

        heade = self.User.shop_headers()
        response = requests.post(url=url, headers=heade, json=payload)
        return response


if __name__ == '__main__':
    a = Sync_robot('lxcrm').sync()
    print(a.json())



class Sync_robot:
    def __init__(self, environment):
        self.heard = user(environment)
        self.test = environment

    def sync_robot_Host(self):
        if self.test == 'test':
            host = 'skb-test.weiwenjia.com'
        elif self.test == 'staging':
            host = 'skb-staging.weiwenjia.com'
        elif self.test == 'lxcrm':
            host = 'skb.weiwenjia.com'
        else:
            print('传参错误')
            host = None
        return host

    def sync(self,pids=None,pages=None):
        url = f'https://{Sync_robot(self.test).sync_robot_Host()}/api_skb/v1/clues/sync_robot'
        payload = {
            "condition": {
                "cn": "composite",
                "cr": "MUST",
                "cv": [
                    {
                        "cn": "wechatCount",
                        "cr": "BETWEEN",
                        "cv": [
                            "1,"
                        ],
                        "id": "16311655696638"
                    }
                ]
            },
            "hasSyncClue": 0,
            "hasSyncRobot": 0,
            "hasUnfolded": 0,
            "sortBy": 0,
            "syncRobotRangeDate": [],
            "pids": pids,
            "way": "advanced_search_list", #所属模块
            "templateType": 0, #是否使用模板
            "templateName": "", #模板名称
            "userClick": 1,
            "from": "syncRobot",
            "useQuota": True, #是否使用额度
            "dataColumns": [
                0
            ], # 数据字段[0, 1] // 0: 手机，1：固话
            "phoneStatus": [
                0,
                1,
                2,
                3
            ], #手机过滤 [0, 1, 2 , 3] //[0, 1, 3]: 过滤疑似代理记账号码 [0, 1, 2]: 过滤异常号码
            "numberCount": 0, #	号码数量 0: 全部,1: 第一条
            "canCover": False,
            "needCallPlan": False, #是否需要创建外呼计划 True / False
        }
        if pids is None:
            payload.pop('pids')
            payload.update({"page": 1, "pagesize": pages})

        heade = self.heard.shop_headers()
        response = requests.post(url=url, headers=heade, json=payload)
        return response


if __name__ == '__main__':
    a = Sync_robot('lxcrm').sync()
    print(a.json())
