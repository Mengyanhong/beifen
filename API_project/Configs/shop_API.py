# -*- coding: utf-8 -*-
# @Time : 2021/7/14 13:01
# @Author : 孟艳红
# @File : shop_API.py,找店铺接口
import requests, json,urllib3
urllib3.disable_warnings()

from API_project.Configs.config_API import user


class shop:
    def __init__(self, test):
        self.test = test
        self.user = user(test)

    def url(self):  # url环境配置
        if self.test == 'test':
            URL = 'https://skb-test.weiwenjia.com/api_skb/v1/shop_search'
        elif self.test == 'staging':
            URL = 'https://skb-staging.weiwenjia.com/api_skb/v1/shop_search'
        elif self.test == 'lxcrm':
            URL = 'https://skb.weiwenjia.com/api_skb/v1/shop_search'
        else:
            print('传参错误')
            URL = None
        return URL

    def categoryL1(self, categoryL1):
        Request_payload = {'shopName': '', 'hasUnfolded': 0, 'hasSyncClue': 0, 'page': 1, 'pagesize': 10,
                           'condition': {'cn': 'composite', 'cr': 'MUST', 'cv': [
                               {'cn': 'category', 'cv': {'categoryL1': [categoryL1], 'categoryL2': []}, 'cr': 'IN'}]}}
        response = requests.post(url=shop(self.test).url(), headers=self.user.headers(), json=Request_payload)
        # if response.json()['error_code'] != 0:
        #     print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        # else:
        #     return response.json()
        return response.json()


    def categoryL2(self, categoryL2):
        Request_payload = {'shopName': '', 'hasUnfolded': 0, 'hasSyncClue': 0, 'page': 1, 'pagesize': 10,
                           'condition': {'cn': 'composite', 'cr': 'MUST', 'cv': [
                               {'cn': 'category', 'cv': {'categoryL1': [], 'categoryL2': [categoryL2]}, 'cr': 'IN'}]}}
        response = requests.post(url=shop(self.test).url(), headers=self.user.headers(), json=Request_payload).json()
        # if response['error_code'] != 0:
        #     print('搜索接口报错', '\n', response['error_code'], response['message'])
        # else:
        #     return response
        return response

    def area_province(self, province):
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [province], "city": [], "district": []}, "cr": "IN"}]}}
        response = requests.post(url=shop(self.test).url(), headers=self.user.headers(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()
    def area_city(self, city):
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [], "city": [city], "district": []}, "cr": "IN"}]}}
        response = requests.post(url=shop(self.test).url(), headers=self.user.headers(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()
    def area_district(self, district):
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [], "city": [], "district": [district]}, "cr": "IN"}]}}
        response = requests.post(url=shop(self.test).url(), headers=self.user.headers(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()
