# -*- coding: utf-8 -*-
# @Time : 2021/9/9 11:40
# @Author : 孟艳红
# @File : sync_robot_libs.py 转机器人接口
import requests, json, time
from API_project.Configs.config_API import user


class Sync_robot:
    def __init__(self, environment):
        self.User = user(environment)

    def sync(self,out_id=None, headers=None, pids=None, pages=None, seach_value=None, Quota=True, dataColumns=None,
             phoneStatus=None,
             numberCount=0, needCallPlan=False, canCover=False, way=None,gatewayId = None):
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

        payload = {
            "from": "syncRobot",
            "useQuota": Quota,  # 是否使用额度
            "dataColumns": dataColumn,  # 数据字段[0, 1] // 0: 手机，1：固话
            "phoneStatus": phone,  # 手机过滤 [0, 1, 2 , 3] //[0, 1, 3]: 过滤疑似代理记账号码 [0, 1, 2]: 过滤异常号码
            "numberCount": numberCount,  # 号码数量 0: 全部,1: 第一条
            "canCover": canCover,  # 重复号码是否导入 true / false
            "needCallPlan": needCallPlan,  # 是否需要创建外呼计划 true / false
        }
        out_payload = {
            "id": out_id,
            "need_push": 0,
            "retry_interval": None,
            "max_retry": None,
            "gatewayNumberId": None,
            "start_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "hangup_message_rules": [],
            "call_type": 0,
            "customers_ids": [],
            "platform": "IK"
        }
        # if gatewayId == None:
        #     gatewayId = self.User.user_key()["gatewayId"]
        #     surveyId
        # else:
        #     gatewayId = gatewayId
        #     surveyId = surveyId
        # {
        #     "plan_name": "测试",
        #     "survey_id": surveyId,
        #     "gatewayId": gatewayId,
        #     "strategy": 1,
        #     "need_push": 1,
        #     "need_finish_message": true,
        #     "need_hangup_message": false,
        # }
        payload.update(seach_value)
        if pids is None:
            payload.update({"page": 1, "pagesize": pages})
        else:
            payload.update({"pids": pids, })
            payload.pop('page')
            payload.pop('pagesize')
        if way is not None:
            payload.update({"way": way})
        if way == 'shop_search_list':
            payload.pop("from")
            clues = 'shopClues'
            header = self.User.headers()
        elif headers is None:
            clues = 'clues'
            header = self.User.shop_headers()
        else:
            clues = 'clues'
            header = self.User.headers()
        if out_id == None:
            pass
        else:
            payload.update({"payload": out_payload })
        url = f'https://{self.User.skb_Host()}/api_skb/v1/{clues}/sync_robot'
        response = requests.post(url=url, headers=header, json=payload)
        return response

    def robot_uncalled(self, query_name=None, queryType=2):
        """
         # 查询号码管理内号码是否存在
        :param query_name: 查询内容，str型
        :param queryType:  查询字段，int型，1：姓名，2：公司名，3：号码
        :return:
        """
        url = f'https://{self.User.robot_Host()}/api/v1/customers/uncalled'
        headers = self.User.robot_headers()
        payload = {
            'page': 1,
            'per_page': 10,
        }
        if query_name is not None:
            payload.update({'query': query_name, 'queryType': queryType})
        response = requests.get(url, params=payload, headers=headers)
        return response

    def robot_outcallplan(self, gatewayId=None):
        """
         # 查询外呼计划
        :param gatewayId: 计划线路，str类型
        :return:
        """
        if gatewayId == None:
            gatewayId = self.User.user_key()["gatewayId"]
        else:
            gatewayId = gatewayId
        url = f'https://{self.User.robot_Host()}/api/v1/plan/list'
        headers = self.User.robot_headers()
        payload = {"page": 1, "per_page": 10,"gatewayId": gatewayId}
        response = requests.post(url, json=payload, headers=headers)
        return response
