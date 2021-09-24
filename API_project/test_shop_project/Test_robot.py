# @Time : 2021/9/9 18:56
# @Author : 孟艳红

import time,pytest,requests, json,os
from pprint import pprint
from API_project.Configs.config_API import user
from API_project.Configs.search_API import search
from API_project.Libs.sync_robot_libs import Sync_robot
from API_project.Libs.sync_robot_search_libs import Sync_robot_test

test_host = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
user = user(test_host)
Sync_robot = Sync_robot(test_host)
search = search(test_host)
Sync_robot_test = Sync_robot_test(test_host)

class Test_Sync_robot:
    # @pytest.mark.parametrize('way', ['search_list', 'advanced_search_list', None,shop_search_list])
    # @pytest.mark.parametrize('page', [None, 500, 1000, 2000])

    @pytest.mark.parametrize('way',['shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def test_case01(self,way,page):  # 扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划
        Sync_robot_test.case01(way = way,page=page)


    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None, 500])
    def test_case02(self,way,page):  # 不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
        Sync_robot_test.case02(way = way,page=page)

    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None, 500])
    def test_case03(self,way,page):  # 仅转移已查看数据，不扣除流量额度，转移手机和固话，仅1条号码,不创建外呼计划，
        Sync_robot_test.case03(way = way,page=page)

    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None])
    def test_case04(self,way,page):  #，转移手机和固话，全部号码,扣除流量额度，不创建外呼计划，
        Sync_robot_test.case04(way = way,page=page)

    @pytest.mark.parametrize('way', ['shop_search_list'])
    @pytest.mark.parametrize('page', [None, 500])
    def test_case05(self, way,page):  # 扣除流量额度，转移手机，全部号码,不创建外呼计划，
        Sync_robot_test.case05(way=way,page=page)

if __name__ == '__main__':
    pytest.main(["Test_robot.py::Test_Sync_robot::test_case05", "-sq", "--alluredir", "../report/test_case05"])  # -s 打印输出,-sq简化打印
    # os.system("allure serve ../report/temp")
    os.system("allure generate ../report/test_case05 -o ../report/test_case05_html --clean")
"""f   用例失败
   E   ERROR
   。  成功的
"""


