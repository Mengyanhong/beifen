# -*- coding: utf-8 -*-
# @Time : 2021/7/14 13:01
# @Author : 孟艳红
# @File : shop_API.py,找店铺接口
import requests, json, urllib3
from API_project.Configs.config_API import user

urllib3.disable_warnings()


class shop_api:
    def __init__(self, test):
        self.user = user(test)

    def search_shop(self, headers=None, shopName="", hasUnfolded=2, hasSyncClue=1, hasSyncRobot=1, cv=None):
        if cv is None:
            cv = [{"cn": "category", "cv": {"categoryL1": ["10"], "categoryL2": ["1030"]}, "cr": "IN"},
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
            header = self.user.headers()
        else:
            header = headers
        response = requests.post(url, headers=header, json=Request_payload)
        return response

    def category(self, shopName="", hasUnfolded=0, hasSyncClue=0, hasSyncRobot=0, cv=None, categoryL1=None,
                 categoryL2=None, headers=None, page=1, pagesize=10):
        '''

        :param shopName: 关键词
        :param hasUnfolded: 查看状态，0：全部，1：已查，2：未查
        :param hasSyncClue: 转线索状态，0：全部，1：未转，2：已转
        :param hasSyncRobot: 转机器人状态，0：全部，1：未转，2：已转
        :param cv: 筛选条件
        :param categoryL1: 一级分类筛选
        :param categoryL2: 二级分类筛选
        :param headers: 用户信息
        :param page: 页码
        :param pagesize: 结果数
        :return: 搜索结果
        '''
        if categoryL1 is None:
            categoryL1 = []
        else:
            categoryL1 = [categoryL1]
        if categoryL2 is None:
            categoryL2 = []
        else:
            categoryL2 = [categoryL2]
        if cv is None:
            cv = [{'cn': 'category', 'cv': {'categoryL1': categoryL1, 'categoryL2': categoryL2}, 'cr': 'IN'}]
        if hasUnfolded != 2:
            hasUnfolded = hasUnfolded
        if hasSyncClue != 1:
            hasSyncClue = hasSyncClue
        if hasSyncRobot != 1:
            hasSyncRobot = hasSyncRobot
        if shopName != "":
            shopName = shopName
        if headers is None:
            headers = self.user.headers()
        if page != 1:
            page = page
        if pagesize != 10:
            pagesize = pagesize

        url = f'https://{self.user.skb_Host()}/api_skb/v1/shop_search'
        Request_payload = {'shopName': shopName, 'hasUnfolded': hasUnfolded, 'hasSyncClue': hasSyncClue,
                           'hasSyncRobot': hasSyncRobot, 'syncRobotRangeDate': [], 'page': page, 'pagesize': pagesize,
                           'condition': {'cn': 'composite', 'cr': 'MUST', 'cv': cv}}
        response = requests.post(url=url, headers=headers, json=Request_payload)
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
