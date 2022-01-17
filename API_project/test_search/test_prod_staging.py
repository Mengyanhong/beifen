import json, sys
import pytest
import requests
import time, sys, json
from pprint import pprint
from API_project.Configs.config_API import user
from API_project.tools.Excelread import Excel_Files
from API_project.tools.install_Excel import install_Excel

excel_file = Excel_Files(file_name="search_keyword.xlsx", sheel="search_keyword")  # 实例化Excel用例文件
file_name = time.strftime("%Y年%m月%d日%H时%M分")  # 实例化测试报告工作表名称


class Test_case:
    # @pytest.mark.parametrize('contact', [1, 2, 3, 4, 5])  # 基本信息
    def search_api(self, HOST_eve=None, keyword='', contact=None, scope=None, matchType="most_fields"):
        user_configs = user(HOST_eve)
        if contact is None or contact == "None":
            contact = []
        if scope is None or scope == "None":
            scope = ''
        url = f'https://{user_configs.skb_Host()}/api_skb/v1/search'
        payload = {
            "keyword": keyword,
            "filter": {
                "location": [],
                "industryshort": [],
                "secindustryshort": [],
                "registercapital": [],
                "establishment": [],
                "entstatus": [],
                "contact": contact,
                "sortBy": "0",
                "companysource": [],
                "enttype": [
                    0
                ],
                "employees": [
                    0
                ],
                "hasrecruit": "0",
                "hassem": "0",
                "haswebsite": "0",
                "hastrademark": "0",
                "haspatent": "0",
                "hastender": "0",
                "haswechataccnt": "0",
                "filterUnfold": 0,
                "filterSync": 0,
                "filterSyncRobot": 0,
                "hasBuildingCert": "0",
                "isHighTech": "0",
                "hasFinanceInfo": "0",
                "hasAbnormalInfo": "0",
                "syncRobotRangeDate": []
            },
            "scope": scope,
            "matchType": matchType,
            "pagesize": 10,
            "page": 1
        }
        time.sleep(3)
        response = requests.post(url, headers=user_configs.headers(), json=payload,
                                 verify=False)
        return response

    @pytest.mark.parametrize('keyword_value', excel_file.open_file_rows("keyword"))  # 关键词
    @pytest.mark.parametrize('scope', excel_file.open_file_rows("scope"))  # 维度
    def test_prod_staging(self, keyword_value, scope):
        install_files = install_Excel(file_name="test_prod_staging", file_title_name=file_name)  # 实例化测试报告文件
        row_sum = install_files.read_sum() + 1
        if row_sum == 2 and install_files.read_one_value() is None:
            install_files.install(row=1, column=1, value='keyword')  # 写入表头
            install_files.install(row=1, column=2, value='scope')  # 写入表头
            install_files.install(row=1, column=3, value='matchType')  # 写入表头
            install_files.install(row=1, column=4, value='测试结果')  # 写入表头
        install_files.install(row=row_sum, column=1, value=keyword_value)  # 写入测试条件
        time.sleep(2.2)
        test_value = Test_case().search_api(HOST_eve="test", keyword=keyword_value, scope=scope).json()
        staging_value = Test_case().search_api(HOST_eve="staging", keyword=keyword_value, scope=scope).json()
        test_items = test_value["data"]["items"]
        if test_items:
            for value in range(len(test_items)):
                test_value["data"]["items"][value].pop("contact")
                staging_value["data"]["items"][value].pop("contact")
                test_value["data"]["items"][value].pop("hasUnfold")
                staging_value["data"]["items"][value].pop("hasUnfold")
                test_value["data"]["items"][value].pop("hasSyncedRobot")
                staging_value["data"]["items"][value].pop("hasSyncedRobot")
                test_value["data"]["items"][value].pop("hasSynced")
                staging_value["data"]["items"][value].pop("hasSynced")
            # print(test_value, "\n", staging_value, "\n", keyword_value)
            if test_value != staging_value:
                install_files.install(row=row_sum, column=4, value='False')
            else:
                install_files.install(row=row_sum, column=4, value='True')
            assert test_value == staging_value
        else:
            if test_value != staging_value:
                install_files.install(row=row_sum, column=4, value='False')
            else:
                install_files.install(row=row_sum, column=4, value='True')
            assert test_value == staging_value
        print(keyword_value, "测试结束")

    @pytest.mark.parametrize('keyword_value', excel_file.open_file_rows("contact"))  # 号码
    def test_prod_staging_contactWay(self, keyword_value):
        install_files = install_Excel(file_name="test_prod_staging", file_title_name=file_name)  # 实例化测试报告文件
        row_sum = install_files.read_sum() + 1
        if row_sum == 2 and install_files.read_one_value() is None:
            install_files.install(row=1, column=1, value='keyword')  # 写入表头
            install_files.install(row=1, column=2, value='scope')  # 写入表头
            install_files.install(row=1, column=3, value='matchType')  # 写入表头
            install_files.install(row=1, column=4, value='测试结果')  # 写入表头
        install_files.install(row=row_sum, column=1, value=keyword_value)  # 写入测试条件
        time.sleep(2.2)
        test_value = Test_case().search_api(HOST_eve="test", keyword=keyword_value, scope="contactWay").json()
        staging_value = Test_case().search_api(HOST_eve="staging", keyword=keyword_value, scope="contactWay").json()
        test_items = test_value["data"]["items"]
        if test_items:
            for value in range(len(test_items)):
                test_value["data"]["items"][value].pop("contact")
                staging_value["data"]["items"][value].pop("contact")
                test_value["data"]["items"][value].pop("hasUnfold")
                staging_value["data"]["items"][value].pop("hasUnfold")
                test_value["data"]["items"][value].pop("hasSyncedRobot")
                staging_value["data"]["items"][value].pop("hasSyncedRobot")
                test_value["data"]["items"][value].pop("hasSynced")
                staging_value["data"]["items"][value].pop("hasSynced")
            # print(test_value, "\n", staging_value, "\n", keyword_value)
            if test_value != staging_value:
                install_files.install(row=row_sum, column=4, value='False')
            else:
                install_files.install(row=row_sum, column=4, value='True')
            assert test_value == staging_value
        else:
            if test_value != staging_value:
                install_files.install(row=row_sum, column=4, value='False')
            else:
                install_files.install(row=row_sum, column=4, value='True')
            assert test_value == staging_value
        print(keyword_value, "测试结束")

    def prod_stagin(self):
        file_name = time.strftime("%Y年%m月%d日%H时%M分")
        install_files = install_Excel(file_name="prod_stagin", file_title_name=file_name)
        install_files.install(row=1, column=1, value='keyword')
        install_files.install(row=1, column=2, value='scope')
        install_files.install(row=1, column=3, value='matchType')
        install_files.install(row=1, column=4, value='测试结果')
        row_sum = 1
        keywordlist = excel_file.open_file_rows("keyword")
        contactlist = excel_file.open_file_rows("contact")
        scopelist = excel_file.open_file_rows("scope")
        scopelist.append("contactWay")
        for scope_value in scopelist:
            if scope_value == "contactWay":
                keywordlist_value = contactlist
            else:
                keywordlist_value = keywordlist
            keyword_value_sum = 0
            for keyword_value in keywordlist_value:
                keyword_value_sum += 1
                if keyword_value_sum > 10:
                    break
                for match in ["most_fields", "phrase_prefix"]:
                    if scope_value in ["contactWay", "companyname", "None"] and match == "phrase_prefix":
                        continue
                    else:
                        time.sleep(2.2)
                        test_value = Test_case().search_api(HOST_eve="test", keyword=keyword_value, scope=scope_value,
                                                            matchType=match).json()
                        staging_value = Test_case().search_api(HOST_eve="staging", keyword=keyword_value,
                                                               scope=scope_value,
                                                               matchType=match).json()
                        test_items = test_value["data"]["items"]
                        row_sum = row_sum + 1
                        install_files.install(row=row_sum, column=1, value=keyword_value)
                        install_files.install(row=row_sum, column=2, value=scope_value)
                        install_files.install(row=row_sum, column=3, value=match)
                        if test_items:
                            for value in range(len(test_items)):
                                test_value["data"]["items"][value].pop("contact")
                                staging_value["data"]["items"][value].pop("contact")
                                test_value["data"]["items"][value].pop("hasUnfold")
                                staging_value["data"]["items"][value].pop("hasUnfold")
                                test_value["data"]["items"][value].pop("hasSyncedRobot")
                                staging_value["data"]["items"][value].pop("hasSyncedRobot")
                                test_value["data"]["items"][value].pop("hasSynced")
                                staging_value["data"]["items"][value].pop("hasSynced")
                            if test_value != staging_value:
                                install_files.install(row=row_sum, column=4, value='False')
                            else:
                                install_files.install(row=row_sum, column=4, value='测试结束')
                        else:
                            if test_value != staging_value:
                                install_files.install(row=row_sum, column=4, value='False')
                            else:
                                install_files.install(row=row_sum, column=4, value='测试结束')
                print(time.strftime("%Y年%m月%d日%H时%M分"))
                print(scope_value, keyword_value, "测试结束")
            print(time.strftime("%Y年%m月%d日%H时%M分"))
            print(scope_value, "测试结束")
# if __name__ == '__main__':
#     Test_case().prod_staging()
