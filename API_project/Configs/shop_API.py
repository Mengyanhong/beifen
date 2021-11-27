# -*- coding: utf-8 -*-
# @Time : 2021/7/14 13:01
# @Author : 孟艳红
# @File : shop_API.py,找店铺接口
import requests, json, urllib3

urllib3.disable_warnings()

from API_project.Configs.config_API import user


class shop:
    def __init__(self, test):
        self.user = user(test)

    def search_shop(self,headers = None,shopName="", hasUnfolded=2, hasSyncClue=1, hasSyncRobot=1, cv=None):
        if cv == None:
            cv = [{"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": []}, "cr": "IN"},
                  {"cn": "contactType", "cv": ["1", "2"], "cr": "IN"}]
        else:
            cv = cv
        if hasUnfolded != 2:
            hasUnfolded = hasUnfolded
        if hasSyncClue != 1:
            hasSyncClue = hasSyncClue
        if hasSyncRobot != 1:
            hasSyncRobot = hasSyncRobot
        url = f'https://{self.user.skb_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": shopName, "hasUnfolded": hasUnfolded, "hasSyncClue": hasSyncClue,
                           "hasSyncRobot": hasSyncRobot,
                           "syncRobotRangeDate": [], "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": cv}}
        if headers is None:
            header = self.user.shop_headers()
        else:
            header=headers
        response = requests.post(url, headers=header, json=Request_payload)
        return response

    def categoryL1(self, categoryL1):
        url = f'https://{self.user.skb_Host()}/api_skb/v1/shop_search'
        Request_payload = {'shopName': '', 'hasUnfolded': 0, 'hasSyncClue': 0, 'page': 1, 'pagesize': 10,
                           'condition': {'cn': 'composite', 'cr': 'MUST', 'cv': [
                               {'cn': 'category', 'cv': {'categoryL1': [categoryL1], 'categoryL2': []}, 'cr': 'IN'}]}}
        response = requests.post(url, headers=self.user.headers(), json=Request_payload)
        return response.json()

    def categoryL2(self, categoryL2):
        url = f'https://{self.user.skb_Host()}/api_skb/v1/shop_search'
        Request_payload = {'shopName': '', 'hasUnfolded': 0, 'hasSyncClue': 0, 'page': 1, 'pagesize': 10,
                           'condition': {'cn': 'composite', 'cr': 'MUST', 'cv': [
                               {'cn': 'category', 'cv': {'categoryL1': [], 'categoryL2': [categoryL2]}, 'cr': 'IN'}]}}
        response = requests.post(url, headers=self.user.headers(), json=Request_payload).json()
        # if response['error_code'] != 0:
        #     print('搜索接口报错', '\n', response['error_code'], response['message'])
        # else:
        #     return response
        return response

    def area_province(self, province):
        url = f'https://{self.user.skb_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [province], "city": [], "district": []}, "cr": "IN"}]}}
        response = requests.post(url, headers=self.user.headers(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()

    def area_city(self, city):
        url = f'https://{self.user.skb_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [], "city": [city], "district": []}, "cr": "IN"}]}}
        response = requests.post(url, headers=self.user.headers(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()

    def area_district(self, district):
        url = f'https://{self.user.skb_Host()}/api_skb/v1/shop_search'
        Request_payload = {"shopName": "", "hasUnfolded": 0, "hasSyncClue": 0, "page": 1, "pagesize": 10,
                           "condition": {"cn": "composite", "cr": "MUST", "cv": [
                               {"cn": "area", "cv": {"province": [], "city": [], "district": [district]}, "cr": "IN"}]}}
        response = requests.post(url, headers=self.user.headers(), json=Request_payload)
        if response.json()['error_code'] != 0:
            print('搜索接口报错', '\n', response.json()['error_code'], response.json()['message'])
        else:
            return response.json()
