# -*- coding: utf-8 -*-
# @Time    : 2021/9/8—18:14
# @Author  : 孟艳红
# @File    : robot_libs.py 机器人数据获取
import requests
from pprint import pprint
from API_project.Configs.config_API import user


class Robotlist:
    def __init__(self, environment):
        self.User = user(environment)

    def robot_uncalled(self, query_name=None):  # 查询号码管理内号码是否存在
        url = f'https://{self.User.robot_Host()}/api/v1/customers/uncalled'
        headers = self.User.robot_headers()
        payload = {
            'page': 1,
            'per_page': 10,
        }
        if query_name is not None:
            payload.update({'query': query_name, 'queryType': 2})
        response = requests.get(url, params=payload, headers=headers)
        return response

    def robot_outcallplan(self, query_name=None):  # 查询外呼计划
        url = f'https://{self.User.robot_Host()}/api/v1/plan/list'
        headers = self.User.robot_headers()
        payload = {"page": 1, "per_page": 10}
        response = requests.post(url, json=payload, headers=headers)
        return response


if __name__ == '__main__':
    a = Robotlist('lxcrm').robot_outcallplan()
    pprint(a.request.url)
    pprint(a.json())
