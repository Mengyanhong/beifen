import json, sys
import pytest
import requests
import time, sys, json
from pprint import pprint
from API_project.Configs.config_API import user
from API_project.tools.Excelread import Excel_Files
from API_project.Configs.search_API import search

from API_project.tools.install_Excel import install_Excel

HOST = "test"
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
            "pagesize": 5,
            "page": 1
        }
        time.sleep(3)
        response = requests.post(url, headers=user_configs.headers(), json=payload,
                                 verify=False)
        return response

    @pytest.mark.parametrize('keyword_value', excel_file.open_file_rows("keyword"))  # 联系方式
    def test_prod_staging(self, keyword_value, ES):
        install_files = install_Excel(file_name="联系方式ES对比", file_title_name=file_name)  # 实例化测试报告文件
        row_sum = install_files.read_sum() + 1
        if row_sum == 2 and install_files.read_one_value() is None:
            install_files.install(row=1, column=1, value='keyword')  # 写入表头
            install_files.install(row=1, column=2, value='pid')  # 写入表头
            install_files.install(row=1, column=3, value='entname')  # 写入表头
            install_files.install(row=1, column=4, value='测试结果')  # 写入表头
        time.sleep(2.2)
        pid_resp_value = Test_case().search_api(HOST_eve=HOST, keyword=keyword_value).json()['data']['items']
        pid_list = []
        if pid_resp_value:
            for pid in pid_resp_value:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        else:
            print('搜索结果：', pid_resp_value, '\n搜索条件:', keyword_value, '\n')
            assert pid_resp_value != []
        for i in pid_list:
            es_result = ES.get(index="company_info_prod", id=i['pid'])['_source']
            details_response = search(HOST).skb_contacts_num(id=i['pid'], module='advance_search_detail')
            details_response_contacts = details_response.json()['data']['contacts']
            details_response_contactNum = details_response.json()['data']['contactNum']
            details_response.close()
            mobilePhone_list = []
            fixedPhone_list = []
            email_list = []
            if details_response_contacts:
                details_response_contacts_value = details_response_contacts
            elif details_response_contacts == [] and details_response_contactNum != 0:
                detail_response = search(HOST).skb_contacts(id=i['pid'], entName=i['entName'],
                                                            module='advance_search_detail')
                detail_response_contacts = detail_response.json()['data']['contacts']
                detail_response.close()
                details_response_contacts_value = detail_response_contacts
            else:
                details_response_contacts_value = []
            if details_response_contacts_value:
                for details_response_value in details_response_contacts_value:
                    if details_response_value['type'] == 1:
                        mobilePhone_list.append(details_response_value['content'])
                    elif details_response_value['type'] == 2:
                        fixedPhone_list.append(details_response_value['content'])
                    elif details_response_value['type'] == 4:
                        email_list.append(details_response_value['content'])
                eSn_list = set(mobilePhone_list).difference(set(es_result["mobilePhone"]))
                eSnf_list = set(fixedPhone_list).difference(set(es_result["fixedPhone"]))
                ESn_list = set(email_list).difference(set(es_result["email"]))
                ESm_list = set(es_result["mobilePhone"]).difference(set(mobilePhone_list))
                ESf_list = set(es_result["fixedPhone"]).difference(set(fixedPhone_list))
                ESe_list = set(es_result["email"]).difference(set(email_list))
                if len(list(eSn_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=keyword_value)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES没有详情页有，手机')  #
                    install_files.install(row=row_sum, column=5, value=str(eSn_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(eSnf_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=keyword_value)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES没有详情页有，固话')  #
                    install_files.install(row=row_sum, column=5, value=str(eSnf_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(ESn_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=keyword_value)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES没有详情页有，邮箱')  #
                    install_files.install(row=row_sum, column=5, value=str(ESn_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(ESm_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=keyword_value)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES有详情页没有，手机')  #
                    install_files.install(row=row_sum, column=5, value=str(ESm_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(ESf_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=keyword_value)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES有详情页没有，固话')  #
                    install_files.install(row=row_sum, column=5, value=str(ESf_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(ESe_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=keyword_value)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES有详情页没有，邮箱')  #
                    install_files.install(row=row_sum, column=5, value=str(ESe_list))  # 写入表头
                assert len(list(ESe_list)) == 0 and len(list(ESf_list)) == 0 and len(list(ESm_list)) == 0 and len(
                    list(ESn_list)) == 0 and len(list(eSnf_list)) == 0 and len(list(eSn_list)) == 0


