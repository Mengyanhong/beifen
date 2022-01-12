import json, sys
import pytest
import requests
import time
from pprint import pprint
from API_project.Configs.config_API import user
from API_project.Configs.search_API import search
from API_project.tools.Excelread import Excel_Files
from API_project.tools.install_Excel import install_Excel

HOST = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
skb_search_configs = search(HOST)

excel_file = Excel_Files(file_name="search_keyword.xlsx", sheel="search_keyword")
# print(excel_file.open_file_rows("keyword"))


class case:
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

    def prod_staging(self):
        for keyword_value in excel_file.open_file_rows("keyword"):
            time.sleep(2.2)
            test_value = case().search_api(HOST_eve="test", keyword=keyword_value, scope="semkeyword").json()
            staging_value = case().search_api(HOST_eve="staging", keyword=keyword_value, scope="semkeyword").json()
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
                print(test_value, "\n", staging_value, "\n", keyword_value)
                assert test_value == staging_value
            else:
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
                        test_value = case().search_api(HOST_eve="test", keyword=keyword_value, scope=scope_value,
                                                       matchType=match).json()
                        staging_value = case().search_api(HOST_eve="staging", keyword=keyword_value, scope=scope_value,
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
                        # if test_items:
                        #     test_value["data"].pop("items")
                        #     staging_value["data"].pop("items")
                        #     if test_value != staging_value:
                        #         install_files.install(row=row_sum, column=4, value='False')
                        #     else:
                        #         items_sum = 0
                        #         for value in range(len(test_items)):
                        #             test_items[value].pop("contact")
                        #             test_items[value].pop("hasUnfold")
                        #             staging_items[value].pop("contact")
                        #             staging_items[value].pop("hasUnfold")
                        #             test_items[value].pop("hasSyncedRobot")
                        #             staging_items[value].pop("hasSyncedRobot")
                        #             test_items[value].pop("hasSynced")
                        #             staging_items[value].pop("hasSynced")
                        #             if staging_items[value] != test_items[value]:
                        #                 items_sum += 1
                        #         if items_sum == 0:
                        #             install_files.install(row=row_sum, column=4, value='测试结束')
                        #         else:
                        #             install_files.install(row=row_sum, column=4, value='False')
                        else:
                            if test_value != staging_value:
                                install_files.install(row=row_sum, column=4, value='False')
                            else:
                                install_files.install(row=row_sum, column=4, value='测试结束')
                print(time.strftime("%Y年%m月%d日%H时%M分"))
                print(scope_value, keyword_value, "测试结束")
            print(time.strftime("%Y年%m月%d日%H时%M分"))
            print(scope_value, "测试结束")
if __name__ == '__main__':
    case().prod_staging()

    # @pytest.mark.parametrize('contact', [1, 2, 3, 4, 5])  # 联系方式
    # def test_contacts_num_search(self, contact):  # 联系方式搜索条件+详情页数据对比case
    #     pid_list = []
    #     time.sleep(2.2)
    #     pid_responst = Test_search().search_api(contact).json()['data']['items']
    #     if pid_responst:
    #         for pid in pid_responst:
    #             pid_list.append({'pid': pid['id'], 'entName': pid['name']})
    #     assert pid_list != []
    #     for i in pid_list:
    #         details_response = skb_search_configs.skb_contacts_num(id=i['pid'], module='advance_search_detail')
    #         details_response_contacts = details_response.json()['data']['contacts']
    #         details_response_contactNum = details_response.json()['data']['contactNum']
    #         details_response.close()
    #         details_response_contacts_value = None
    #         hasMobile_sum = 0
    #         hasFixed_sum = 0
    #         hasEmail_sum = 0
    #         hasQq_sum = 0
    #         if details_response_contacts:
    #             details_response_contacts_value = details_response_contacts
    #         elif details_response_contacts == [] and details_response_contactNum != 0:
    #             detail_response = skb_search_configs.skb_contacts(id=i['pid'], entName=i['entName'],
    #                                                               module='advance_search_detail')
    #             detail_response_contacts = detail_response.json()['data']['contacts']
    #             detail_response.close()
    #             details_response_contacts_value = detail_response_contacts
    #         else:
    #             if contact == 5:
    #                 if details_response_contacts != [] or details_response_contactNum != 0:
    #                     print('pid:', i, '搜索条件', contact, '\n该企业联系方式有误查询结果为', details_response)
    #                 assert details_response_contacts == [] and details_response_contactNum == 0
    #             else:
    #                 if contact != 5:
    #                     print('pid:', i, '搜索条件', contact, '\n该企业联系方式有误查询结果为', details_response)
    #                 assert contact == 5
    #         if details_response_contacts_value:
    #             for details_response_value in details_response_contacts_value:
    #                 if contact == 1:
    #                     if details_response_value['type'] == 1:
    #                         hasMobile_sum += 1
    #                         break
    #                     else:
    #                         continue
    #                 elif contact == 2:
    #                     if details_response_value['type'] == 2:
    #                         hasFixed_sum += 1
    #                         break
    #                     else:
    #                         continue
    #                 elif contact == 3:
    #                     if details_response_value['type'] == 4:
    #                         hasEmail_sum += 1
    #                         break
    #                     else:
    #                         continue
    #                 elif contact == 4:
    #                     if details_response_value['type'] == 3:
    #                         hasQq_sum += 1
    #                         break
    #                     else:
    #                         continue
    #                 else:
    #                     continue
    #         else:
    #             continue
    #         if contact == 1:
    #             if hasMobile_sum == 0:
    #                 print('pid:', i, '搜索条件', contact, '\n')
    #             assert hasMobile_sum != 0
    #         elif contact == 2:
    #             if hasFixed_sum == 0:
    #                 print('pid:', i, '搜索条件', contact, '\n')
    #             assert hasFixed_sum != 0
    #         elif contact == 3:
    #             if hasEmail_sum == 0:
    #                 print('pid:', i, '搜索条件', contact, '\n')
    #             assert hasEmail_sum != 0
    #         elif contact == 4:
    #             if hasQq_sum == 0:
    #                 print('pid:', i, '搜索条件', contact, '\n')
    #             assert hasQq_sum != 0
    #         else:
    #             if details_response_contacts != [] or details_response_contactNum != 0:
    #                 print('pid:', i, '搜索条件', contact, '\n')
    #             assert details_response_contacts == [] and details_response_contactNum == 0

# print(json.loads(case().search_api(HOST_eve="test", keyword=i).request.body))
# if __name__ == '__main__':
#     for i in excel_file.open_file_rows("keyword"):
#         a = case().search_api(HOST_eve="test", keyword=i).json()
#         b = case().search_api(HOST_eve="staging", keyword=i).json()
#         if a == b:
#             print(True)
#             print(a,"\n",b)
#             break
#         else:
#             print(a,"\n",b)
#             print(False)
#             # pprint(case().search_api(HOST_eve="test", keyword=i).json())
#             # pprint(case().search_api(HOST_eve="lxcrm", keyword=i).json())
#             break
