# -*- coding: utf-8 -*-
# @Time : 2021/9/9 11:40
# @Author : 孟艳红
# @File : sync_robot_libs.py 转机器人接口
import requests
from API_project.Configs.config_API import user

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

