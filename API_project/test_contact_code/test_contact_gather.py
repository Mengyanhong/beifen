# 联系方式相关case
# from collections import Counter  # 导入表格统计模块
from API_project.Configs.config_API import configuration_file
from API_project.tools.get_yaml_set import get_yaml_data
import json, sys
import pytest
import requests
import time, sys, json, openpyxl
from pprint import pprint
from API_project.Configs.config_API import user
from API_project.tools.Excelread import Excel_Files
from API_project.Configs.search_API import search
from API_project.tools.install_Excel import install_Excel

# excel_file = Excel_Files(file_name="联系方式渠道配置.xlsx", sheel="联系方式渠道配置")  # 实例化Excel用例文件
file_name = time.strftime("%Y年%m月%d日%H时%M分")  # 实例化测试报告工作表名称

HOST = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境


recruitPlatform_config = configuration_file(HOST).conditionConfig()  # 实例化高级搜索配置并返回配置信息
staticConfig = configuration_file(HOST).staticConfig()['contactSiteSourceMap']  # 实例化高级搜索配置withLevels并返回配置信息
staticConfig_lists = []
for staticConfig_value in staticConfig:
    staticConfig_list = staticConfig_lists + staticConfig_value['sub']

staticConfig_list = []
staticConfig_sum = 0
for staticConfig_value in staticConfig_lists:
    staticConfig_sum += 1
    if staticConfig_sum <= 72:
        continue
    elif staticConfig_sum <= 90:
        staticConfig_list.append(staticConfig_value)


class Test_contact:  # 联系方式
    @pytest.mark.parametrize('cv_key', [True, False])  # 联系方式有无
    @pytest.mark.parametrize('contacts_num_search_conditions_value',
                             get_yaml_data('../data/yaml/have_or_not_search.yaml')['contacts_num'])
    def test_contacts_num_search(self, cv_key,
                                 contacts_num_search_conditions_value, ES):  # 联系方式有无搜索条件+详情页数据对比case
        cv = [{"cn": contacts_num_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
        pid_list = []
        time.sleep(2.2)
        pid_responst = search(HOST).advanced_search(cv=cv, page=3, pagesize=20).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        else:
            print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
        for i in pid_list:
            details_response = search(HOST).skb_contacts_num(id=i['pid'], module='advance_search_detail')
            details_response_contacts = details_response.json()['data']['contacts']
            details_response_contactNum = details_response.json()['data']['contactNum']
            details_response.close()
            details_response_contacts_value = None
            hasMobile_sum = 0
            hasFixed_sum = 0
            hasEmail_sum = 0
            hasQq_sum = 0
            if details_response_contacts:
                details_response_contacts_value = details_response_contacts
            elif details_response_contacts == [] and details_response_contactNum != 0:
                detail_response = search(HOST).skb_contacts(id=i['pid'], entName=i['entName'],
                                                            module='advance_search_detail')
                detail_response_contacts = detail_response.json()['data']['contacts']
                detail_response.close()
                details_response_contacts_value = detail_response_contacts
            else:
                print('pid:', i, '搜索条件', cv, '\n该企业联系方式有误查询结果为', details_response)
                assert details_response_contacts != [] and details_response_contactNum != 0
            assert details_response_contacts_value is not None and details_response_contacts_value != []
            for details_response_value in details_response_contacts_value:
                if contacts_num_search_conditions_value['detail_data'] == 1:
                    if details_response_value['type'] == 1:
                        hasMobile_sum += 1
                        break
                    else:
                        continue
                elif contacts_num_search_conditions_value['detail_data'] == 2:
                    if details_response_value['type'] == 2:
                        hasFixed_sum += 1
                        break
                    else:
                        continue
                elif contacts_num_search_conditions_value['detail_data'] == 3:
                    if details_response_value['type'] == 3:
                        hasQq_sum += 1
                        break
                    else:
                        continue
                elif contacts_num_search_conditions_value['detail_data'] == 4:
                    if details_response_value['type'] == 4:
                        hasEmail_sum += 1
                        break
                    else:
                        continue
                else:
                    print('搜索条件号码类型错误', contacts_num_search_conditions_value)
                    assert contacts_num_search_conditions_value['detail_data'] == 1 or \
                           contacts_num_search_conditions_value['detail_data'] == 2 or \
                           contacts_num_search_conditions_value['detail_data'] == 3 or \
                           contacts_num_search_conditions_value['detail_data'] == 4
            if cv_key == True:
                if contacts_num_search_conditions_value['detail_data'] == 1:
                    if hasMobile_sum == 0:
                        print('pid:', i, '搜索条件', cv, '\n')
                    assert hasMobile_sum != 0
                elif contacts_num_search_conditions_value['detail_data'] == 2:
                    if hasFixed_sum == 0:
                        print('pid:', i, '搜索条件', cv, '\n')
                    assert hasFixed_sum != 0
                elif contacts_num_search_conditions_value['detail_data'] == 3:
                    if hasQq_sum == 0:
                        print('pid:', i, '搜索条件', cv, '\n')
                    assert hasQq_sum != 0
                elif contacts_num_search_conditions_value['detail_data'] == 4:
                    if hasEmail_sum == 0:
                        print('pid:', i, '搜索条件', cv, '\n')
                    assert hasEmail_sum != 0
                else:
                    print('pid:', i, '搜索条件有误', contacts_num_search_conditions_value)
                    assert contacts_num_search_conditions_value['detail_data'] == 1 or \
                           contacts_num_search_conditions_value['detail_data'] == 2 or \
                           contacts_num_search_conditions_value['detail_data'] == 3 or \
                           contacts_num_search_conditions_value['detail_data'] == 4
            elif cv_key == False:
                if contacts_num_search_conditions_value['detail_data'] == 1:
                    if hasMobile_sum != 0:
                        print('pid:', i, '搜索条件', cv, '\n')
                    assert hasMobile_sum == 0
                elif contacts_num_search_conditions_value['detail_data'] == 2:
                    if hasFixed_sum != 0:
                        print('pid:', i, '搜索条件', cv, '\n')
                    assert hasFixed_sum == 0
                elif contacts_num_search_conditions_value['detail_data'] == 3:
                    if hasQq_sum != 0:
                        print('pid:', i, '搜索条件', cv, '\n')
                    assert hasQq_sum == 0
                elif contacts_num_search_conditions_value['detail_data'] == 4:
                    if hasEmail_sum != 0:
                        print('pid:', i, '搜索条件', cv, '\n')
                    assert hasEmail_sum == 0
                else:
                    print('pid:', i, '搜索条件有误', contacts_num_search_conditions_value)
                    assert contacts_num_search_conditions_value['detail_data'] == 1 or \
                           contacts_num_search_conditions_value['detail_data'] == 2 or \
                           contacts_num_search_conditions_value['detail_data'] == 3 or \
                           contacts_num_search_conditions_value['detail_data'] == 4
            else:
                print('pid:', i, '判断条件错误', cv_key)
                assert cv_key == False or cv_key == True

    @pytest.mark.parametrize('cv_key', [True, False])  # 代理记账
    @pytest.mark.parametrize('cn_key', ["isAgency", "hasNonAgency"])  # 代理记账
    def test_contacts_Agency_search(self, cv_key, cn_key):  # 联系方式有无疑似代理记账+详情页数据对比case
        cv = [{"cn": cn_key, "cr": 'IS', "cv": cv_key}]
        print(cv)
        pid_list = []
        time.sleep(2.2)
        pid_responst = search(HOST).advanced_search(cv=cv, page=3, pagesize=20).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        else:
            print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
        for i in pid_list:
            details_response = search(HOST).skb_contacts_num(id=i['pid'], module='advance_search_detail')
            details_response_contacts = details_response.json()['data']['contacts']
            details_response_contactNum = details_response.json()['data']['contactNum']
            details_response.close()
            details_response_contacts_value = None
            isAgency_sum = 0
            if details_response_contacts:
                details_response_contacts_value = details_response_contacts
            elif details_response_contacts == [] and details_response_contactNum != 0:
                detail_response = search(HOST).skb_contacts(id=i['pid'], entName=i['entName'],
                                                            module='advance_search_detail')
                detail_response_contacts = detail_response.json()['data']['contacts']
                detail_response.close()
                details_response_contacts_value = detail_response_contacts
            else:
                print('pid:', i, '搜索条件', cv, '\n该企业联系方式有误查询结果为', details_response)
                assert details_response_contacts != [] and details_response_contactNum["sources"] != 0
            assert details_response_contacts_value is not None and details_response_contacts_value != []
            for details_response_value in details_response_contacts_value:
                if cn_key == "isAgency":
                    if 'suspectedAgent' in details_response_value.keys() and details_response_value[
                        'suspectedAgent'] == True and details_response_value['type'] not in [3, 4]:
                        isAgency_sum += 1
                        break
                    else:
                        continue
                else:
                    if 'suspectedAgent' not in details_response_value.keys() and details_response_value['type'] not in [
                        3, 4]:
                        isAgency_sum += 1
                        break
                    else:
                        continue
            if cv_key == True:
                if isAgency_sum == 0:
                    print('pid:', i, '搜索条件', cv, '\n')
                assert isAgency_sum != 0
            elif cv_key == False:
                if isAgency_sum != 0:
                    print('pid:', i, '搜索条件', cv, '\n')
                assert isAgency_sum == 0

            else:
                print('pid:', i, '判断条件错误', cv_key)
                assert cv_key == False or cv_key == True

    @pytest.mark.parametrize('cr_key', ["IN", "NOT_IN"])
    @pytest.mark.parametrize('cn_key', ["1", "2"])  # 非代理记账类型
    def test_contacts_notAgency_search(self, cr_key, cn_key):  # 联系方式非代理记账类型+详情页数据对比case
        cv = [{"cn": "nonAgencyType", "cr": cr_key, "cv": [cn_key]}]
        pid_list = []
        time.sleep(2.2)
        pid_responst = search(HOST).advanced_search(cv=cv, page=1, pagesize=20).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        else:
            print('搜索结果为空：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
        for i in pid_list:
            details_response = search(HOST).skb_contacts_num(id=i['pid'], module='advance_search_detail').json()
            details_response_contacts = details_response['data']['contacts']
            details_response_contactNum = details_response['data']['contactNum']
            isAgency_sum = 0
            if details_response_contacts:
                details_response_contacts_value = details_response_contacts
            elif int(details_response_contactNum) > 0:
                detail_response = search(HOST).skb_contacts(id=i['pid'], entName=i['entName'],
                                                            module='advance_search_detail').json()
                detail_response_contacts = detail_response['data']['contacts']
                # detail_response.close()
                details_response_contacts_value = detail_response_contacts
            else:
                details_response_contacts_value = []
                print('pid:', i, '搜索条件', cv, '\n该企业联系方式为空', details_response)
                assert details_response_contacts != [] and details_response_contactNum["sources"] != 0
            assert details_response_contacts_value is not None and details_response_contacts_value != []
            for details_response_value in details_response_contacts_value:
                if cn_key == "1":
                    if details_response_value['type'] == 1:
                        if 'suspectedAgent' not in details_response_value.keys():
                            isAgency_sum += 1
                            break
                        else:
                            continue
                else:
                    if details_response_value['type'] == 2:
                        if 'suspectedAgent' not in details_response_value.keys():
                            isAgency_sum += 1
                            break
                        else:
                            continue
            if cr_key == "IN":
                if isAgency_sum == 0:
                    print('pid:', i, '搜索条件', cv, '\n')
                assert isAgency_sum != 0
            elif cr_key == "NOT_IN":
                if isAgency_sum != 0:
                    print('pid:', i, '搜索条件', cv, '\n')
                assert isAgency_sum == 0
            else:
                print('pid:', i, '判断条件错误', cr_key)
                assert cr_key == "IN" or cr_key == "NOT_IN"


excel_file = Excel_Files(file_name="search_keyword.xlsx", sheel="search_keyword")
class Test_case:
    # @pytest.mark.parametrize('contact', [1, 2, 3, 4, 5])  # 基本信息
    def search_api(self, header=None, HOST_eve=None, keyword='', contact=None, scope=None, matchType="most_fields"):
        user_configs = user(HOST_eve)
        if contact is None or contact == "None":
            contact = []
        else:
            contact = [contact]
        # header = {
        #     'app_token': "a14cc8b00f84e64b438af540390531e4",
        #     'authorization': "Token token=4e15695de0bfe2273795e707fd602d46",
        #     'content-type': 'application/json',
        #     'crm_platform_type': "lixiaoyun"
        # }
        if header is None:
            headers = user_configs.headers()
        else:
            headers = header

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
            "pagesize": 100,
            "page": 2
        }
        time.sleep(3)

        response = requests.post(url, headers=headers, json=payload,
                                 verify=False)
        return response

    # 非联系方式维度测试
    @pytest.mark.parametrize('keyword_value', excel_file.open_file_rows("keyword"))  # 关键词
    # @pytest.mark.parametrize('scope', excel_file.open_file_rows("scope"))  # 维度
    def test_prod_ES(self, keyword_value, scope, ES):  # 非联系方式维度测试
        install_files = install_Excel(file_name="联系方式ES对比01", file_title_name=file_name)  # 实例化测试报告文件
        row_sum = install_files.read_sum() + 1
        if row_sum == 2 and install_files.read_one_value() is None:
            install_files.install(row=1, column=1, value='keyword')  # 写入表头
            install_files.install(row=1, column=2, value='pid')  # 写入表头
            install_files.install(row=1, column=3, value='entname')  # 写入表头
            install_files.install(row=1, column=4, value='测试结果')  # 写入表头
        time.sleep(2.2)
        pid_resp_value = Test_case().search_api(HOST_eve=HOST, keyword=keyword_value, scope=scope).json()['data'][
            'items']
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
                    list(ESn_list)) == 0 and len(list(eSnf_list)) == 0 and len(list(eSn_list)) == 0  # 联系方式维度测试

    # 联系方式维度测试
    @pytest.mark.parametrize('contact', excel_file.open_file_rows("contact"))  # 号码
    def test_ES_prod_contact(self, contact, ES):  # 联系方式维度测试
        install_files = install_Excel(file_name="联系方式ES对比02", file_title_name=file_name)  # 实例化测试报告文件
        row_sum = install_files.read_sum() + 1
        if row_sum == 2 and install_files.read_one_value() is None:
            install_files.install(row=1, column=1, value='keyword')  # 写入表头
            install_files.install(row=1, column=2, value='pid')  # 写入表头
            install_files.install(row=1, column=3, value='entname')  # 写入表头
            install_files.install(row=1, column=4, value='测试结果')  # 写入表头
        time.sleep(2.2)
        pid_resp_value = Test_case().search_api(HOST_eve=HOST, keyword=contact, scope="contactWay").json()['data'][
            'items']
        pid_list = []
        if pid_resp_value:
            for pid in pid_resp_value:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        else:
            print('搜索结果：', pid_resp_value, '\n搜索条件:', contact, '\n')
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
                    install_files.install(row=row_sum, column=1, value=contact)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES没有详情页有，手机')  #
                    install_files.install(row=row_sum, column=5, value=str(eSn_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(eSnf_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=contact)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES没有详情页有，固话')  #
                    install_files.install(row=row_sum, column=5, value=str(eSnf_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(ESn_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=contact)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES没有详情页有，邮箱')  #
                    install_files.install(row=row_sum, column=5, value=str(ESn_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(ESm_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=contact)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES有详情页没有，手机')  #
                    install_files.install(row=row_sum, column=5, value=str(ESm_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(ESf_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=contact)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES有详情页没有，固话')  #
                    install_files.install(row=row_sum, column=5, value=str(ESf_list))  # 写入表头
                    row_sum = row_sum + 1
                if len(list(ESe_list)) != 0:
                    install_files.install(row=row_sum, column=1, value=contact)  # 写入表头
                    install_files.install(row=row_sum, column=2, value=i['pid'])  # 写入表头
                    install_files.install(row=row_sum, column=3, value=i['entName'])  # 写入表头
                    install_files.install(row=row_sum, column=4, value='ES有详情页没有，邮箱')  #
                    install_files.install(row=row_sum, column=5, value=str(ESe_list))  # 写入表头
                assert len(list(ESe_list)) == 0 and len(list(ESf_list)) == 0 and len(list(ESm_list)) == 0 and len(
                    list(ESn_list)) == 0 and len(list(eSnf_list)) == 0 and len(list(eSn_list)) == 0

    # 联系方式筛选
    @pytest.mark.parametrize('contact', [1, 2, 3, 4, 5])
    def test_contacts_Sizer_search(self, contact):  # 联系方式搜索条件+详情页数据对比case
        # install_files = install_Excel(file_name="联系方式ES对比", file_title_name=file_name)  # 实例化测试报告文件
        #
        # if install_files.read_sum() == 1 and install_files.read_one_value() is None:
        #     install_files.install(row=1, column=1, value='keyword')  # 写入表头
        #     install_files.install(row=1, column=2, value='pid')  # 写入表头
        #     install_files.install(row=1, column=3, value='entname')  # 写入表头
        #     install_files.install(row=1, column=4, value='测试结果')  # 写入表头
        pid_list = []
        time.sleep(2.2)
        pid_responst = Test_case().search_api(HOST_eve=HOST, contact=contact, keyword="北京").json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        assert pid_list != []
        for i in pid_list:
            details_response = search(HOST).skb_contacts_num(id=i['pid'], module='search_detail').json()
            details_response_contacts = details_response['data']['contacts']
            details_response_contactNum = details_response['data']['contactNum']
            hasMobile_sum = 0
            hasFixed_sum = 0
            hasEmail_sum = 0
            hasQq_sum = 0
            if details_response_contacts:
                details_response_contacts_value = details_response_contacts
            elif int(details_response_contactNum) != 0:
                details_response = search(HOST).skb_contacts(id=i['pid'], entName=i['entName'],
                                                             module='search_detail').json()
                try:
                    details_response_contacts = details_response['data']['contacts']
                except:
                    details_response_contacts = []
                    print(i)
                    print('联系方式接口获取异常\n', details_response)
                details_response_contacts_value = details_response_contacts
            else:
                details_response_contacts_value = []
                if contact == 5:
                    assert details_response_contacts == [] and details_response_contactNum == 0
                else:
                    if contact != 5:
                        print('pid:', i, '搜索条件', contact, '\n联系方式搜索有误查询结果为', details_response)
            if details_response_contacts_value:
                for details_response_value in details_response_contacts_value:
                    if contact == 1:
                        if details_response_value['type'] == 1:
                            hasMobile_sum += 1
                            break
                    elif contact == 2:
                        if details_response_value['type'] == 2:
                            hasFixed_sum += 1
                            break
                    elif contact == 3:
                        if details_response_value['type'] == 4:
                            hasEmail_sum += 1
                            break
                    else:
                        if details_response_value['type'] == 3:
                            hasQq_sum += 1
                            break
            if contact == 1:
                if hasMobile_sum == 0:
                    print('pid:', i, '搜索条件', contact, '\n手机搜索有误')
                assert hasMobile_sum != 0
            elif contact == 2:
                if hasFixed_sum == 0:
                    print('pid:', i, '搜索条件', contact, '\n固话搜索有误')
                assert hasFixed_sum != 0
            elif contact == 3:
                if hasEmail_sum == 0:
                    print('pid:', i, '搜索条件', contact, '\n邮箱搜索有误')
                assert hasEmail_sum != 0
            elif contact == 4:
                if hasQq_sum == 0:
                    print('pid:', i, '搜索条件', contact, '\nQQ搜索有误')
                assert hasQq_sum != 0
            else:
                if details_response_contacts != [] or details_response_contactNum != 0:
                    print('pid:', i, '搜索条件', contact, '\n无联系方式搜索错误')
                assert details_response_contacts == [] and details_response_contactNum == 0
