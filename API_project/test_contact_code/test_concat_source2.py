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
    staticConfig_lists = staticConfig_lists + staticConfig_value['sub']
# staticConfig_list = []
# staticConfig_sum = 0
# for staticConfig_value in staticConfig_lists:
#     staticConfig_sum += 1
#     if staticConfig_sum <= 72:
#         continue
#     elif staticConfig_sum <= 90:
#         staticConfig_list.append(staticConfig_value)

 # 联系方式渠道
@pytest.mark.parametrize('cn_key', ["fixedSource"])  # 联系方式渠道"contactSource", "mobileSource", "fixedSource"
@pytest.mark.parametrize('cv_key', ["IN", "NOT_IN"])
@pytest.mark.parametrize('contactSiteSourceMap_search_value', staticConfig_lists)
def test_contacts_channels(cn_key, cv_key,
                          contactSiteSourceMap_search_value):  # 联系方式渠道+详情页数据对比case
    install_files = install_Excel(file_name="迭代联系方式渠道测试结果03", file_title_name=file_name)  # 实例化测试报告文件
    if install_files.read_sum() == 1 and install_files.read_one_value() is None:
        install_files.install(row=1, column=1, value='pid')
        install_files.install(row=1, column=2, value='entName')
        install_files.install(row=1, column=3, value='搜索条件')
        install_files.install(row=1, column=4, value='搜索渠道')
        install_files.install(row=1, column=5, value='过滤条件')
        install_files.install(row=1, column=6, value='测试结果')
    cv = [{"cn": cn_key, "cr": cv_key, "cv": [contactSiteSourceMap_search_value["name"]]}]
    pid_list = []
    time.sleep(2.2)
    pid_responst = search(HOST).advanced_search(cv=cv, page=1, pagesize=2).json()['data']['items']
    if pid_responst:
        for pid in pid_responst:
            pid_list.append({'pid': pid['id'], 'entName': pid['name']})
    else:
        row_sum = install_files.read_sum() + 1
        install_files.install(row=row_sum, column=3, value=cn_key)
        install_files.install(row=row_sum, column=4, value=contactSiteSourceMap_search_value["value"])
        install_files.install(row=row_sum, column=5, value=cv_key)
        install_files.install(row=row_sum, column=6, value='搜索结果为空')
        print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
        assert pid_responst != []
    for i in pid_list:
        details_response = search(HOST).skb_contacts_num(id=i['pid'], module='advance_search_detail').json()
        details_response_contacts_num = details_response['data']['contacts']
        details_response_contactNum = details_response['data']['contactNum']
        if details_response_contacts_num:
            contact_way_response = details_response_contacts_num
        elif int(details_response_contactNum) > 0:
            detail_response = search(HOST).skb_contacts(id=i['pid'], entName=i['entName'],
                                                        module='advance_search_detail').json()
            if detail_response['data']['contacts'] != []:
                contact_way_response = detail_response['data']['contacts']
            else:
                print('pid:', i, '搜索条件', cv, '\n该企业联系方式获取失败', detail_response)
        else:
            contact_way_response = []
            row_sum = install_files.read_sum() + 1
            install_files.install(row=row_sum, column=3, value=cn_key)
            install_files.install(row=row_sum, column=4, value=contactSiteSourceMap_search_value["value"])
            install_files.install(row=row_sum, column=5, value=cv_key)
            install_files.install(row=row_sum, column=6, value='联系方式为空')
            print('pid:', i, '搜索条件', cv, '\n该企业联系方式有误查询结果为', details_response)
            assert details_response_contacts_num != [] and details_response_contactNum != 0
        assert contact_way_response != []
        sources_sum = 0
        for contact_response_value in contact_way_response:
            if cn_key == "contactSource":
                for sources in contact_response_value["sources"]:
                    if contactSiteSourceMap_search_value["value"] == sources["sourceName"] or \
                            contactSiteSourceMap_search_value["value"] in sources["sourceName"]:
                        sources_sum += 1
                        break
                    else:
                        continue
            elif cn_key == "mobileSource":
                if contact_response_value["type"] == 1:
                    for sources in contact_response_value["sources"]:
                        if contactSiteSourceMap_search_value["value"] == sources["sourceName"] or \
                                contactSiteSourceMap_search_value["value"] in sources["sourceName"]:
                            sources_sum += 1
                            break
                        else:
                            continue
                else:
                    continue
            else:
                if contact_response_value["type"] == 2:
                    for sources in contact_response_value["sources"]:
                        if contactSiteSourceMap_search_value["value"] == sources["sourceName"] or \
                                contactSiteSourceMap_search_value["value"] in sources["sourceName"]:
                            sources_sum += 1
                            break
                        else:
                            continue
                else:
                    continue
        if cv_key == "IN":
            if sources_sum == 0:
                row_sum = install_files.read_sum() + 1
                install_files.install(row=row_sum, column=1, value=i['pid'])
                install_files.install(row=row_sum, column=2, value=i['entName'])
                install_files.install(row=row_sum, column=3, value=cn_key)
                install_files.install(row=row_sum, column=4,
                                      value=contactSiteSourceMap_search_value["value"])
                install_files.install(row=row_sum, column=5, value=cv_key)
                install_files.install(row=row_sum, column=6, value='详情页没有该渠道但是ES有该渠道')
                print('pid:', i, '搜索条件', cv, '\n')
            assert sources_sum != 0
        elif cv_key == "NOT_IN":
            if sources_sum != 0:
                row_sum = install_files.read_sum() + 1
                install_files.install(row=row_sum, column=1, value=i['pid'])
                install_files.install(row=row_sum, column=2, value=i['entName'])
                install_files.install(row=row_sum, column=3, value=cn_key)
                install_files.install(row=row_sum, column=4,
                                      value=contactSiteSourceMap_search_value["value"])
                install_files.install(row=row_sum, column=5, value=cv_key)
                install_files.install(row=row_sum, column=6, value='详情页有该渠道但是ES没有该渠道')
                print('pid:', i, '搜索条件', cv, '\n')
            assert sources_sum == 0
        else:
            print('判断条件出错', cv_key)