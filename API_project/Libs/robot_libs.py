# -*- coding: utf-8 -*-
# @Time    : 2021/9/8—18:14
# @Author  : 孟艳红
# @File    : robot_libs.py
from pprint import pprint

import requests
from API_project.Configs.config_API import user


class Robotlist:
    def __init__(self, environment):
        self.test = environment
        self.header = user(environment).robot_headers()

    def Host(self):
        if self.test == 'test':
            host = 'jiqiren-test.weiwenjia.com'
        elif self.test == 'staging':
            host = 'jiqiren-staging.weiwenjia.com'
        elif self.test == 'lxcrm':
            host = 'jiqiren.weiwenjia.com'
        else:
            print('传参错误')
            host = None
        return host

    def robot_uncalled(self, query_name=None):  # 查询号码管理内号码是否存在
        url = f'https://{Robotlist(self.test).Host()}/api/v1/customers/uncalled'
        headers = self.header
        payload = {
            'page': 1,
            'per_page': 10,
        }
        if query_name != None:
            payload.update({'query': query_name, 'queryType': 2})
        response = requests.get(url, params=payload, headers=headers)
        return response

    def robot_outcallplan(self, query_name=None):  # 查询外呼计划
        url = f'https://{Robotlist(self.test).Host()}/api/v1/plan/list'
        headers = self.header
        payload = {"page": 1, "per_page": 10}
        response = requests.post(url, json=payload, headers=headers)
        return response


if __name__ == '__main__':
    a = Robotlist('lxcrm').robot_outcallplan()
    pprint(a.request.url)
    pprint(a.json())
