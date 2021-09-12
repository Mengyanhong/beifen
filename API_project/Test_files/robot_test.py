# @Time : 2021/9/9 18:56
# @Author : 孟艳红

import time
from pprint import pprint

import requests, json
from API_project.Configs.config_API import user
# from API_project.Libs.robot_libs import Robotlist
from API_project.Configs.search_API import search
from API_project.Libs.sync_robot_libs import Sync_robot

from API_project.Libs.sync_robot_search_libs import Sync_robot_test

test_host = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
user = user(test_host)
# self.Robotlist = Robotlist(test_host)
Sync_robot = Sync_robot(test_host)
search = search(test_host)

Sync_robot_test = Sync_robot_test(test_host)

class Test_Sync_robot:
    def test_case01(self):  # 扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划
        Sync_robot_test.case01()

    def test_case02(self):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
        Sync_robot_test.case02()

    def test_case03(self):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
        Sync_robot_test.case03()

    def test_case04(self):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
        Sync_robot_test.case04()



if __name__ == '__main__':
    re = Test_Sync_robot(test_host).test_case04()
    print(re)
    # print(re.request.body.decode("unicode_escape"))
    # print(re.request.url)
    # print(re.request.headers)
