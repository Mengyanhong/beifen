import time
from API_project.Configs.config_API import configuration_file
from API_project.Configs.search_API import search
from API_project.tools.install_Excel import install_Excel

HOST = "lxcrm"
recruitPlatform_config = configuration_file(HOST).conditionConfig()['contactSource']['cr']['options']
staticConfig = configuration_file(HOST).staticConfig()['contactSiteSourceMap']  # 实例化高级搜索配置withLevels并返回配置信息
staticConfig_list = []
for staticConfig_value in staticConfig:
    staticConfig_list = staticConfig_list + staticConfig_value['sub']
cn_search_list = ["contactSource", "mobileSource", "fixedSource"]


def contacts_channel(host, cn_search, cv_search,
                     search_value):  # 联系方式渠道
    # file_name = time.strftime("%Y-%m-%d %H:%M:%S").split(":")[0].replace("-", "_").replace(" ", "_")
    file_name = time.strftime("%Y年%m月%d日%H时%M分")
    install_files = install_Excel(file_name="联系方式渠道", file_title_name=file_name)
    install_files.install(row=1, column=1, value='pid')
    install_files.install(row=1, column=2, value='entName')
    install_files.install(row=1, column=3, value='搜索条件')
    install_files.install(row=1, column=4, value='搜索渠道')
    install_files.install(row=1, column=5, value='过滤条件')
    install_files.install(row=1, column=6, value='测试结果')
    row_sum = 1
    for contactSiteSourceMap_search_value in search_value:
        for cv_key in cv_search:
            for cn_key in cn_search:
                cv = [{"cn": cn_key, "cr": cv_key["value"], "cv": [contactSiteSourceMap_search_value["name"]]}]
                pid_list = []
                time.sleep(2.2)
                pid_responst = search(host).advanced_search(cv=cv, page=2, pagesize=10).json()['data']['items']
                # print(pid_responst)
                if pid_responst:
                    for pid in pid_responst:
                        pid_list.append({'pid': pid['id'], 'entName': pid['name']})
                else:
                    row_sum = row_sum + 1
                    install_files.install(row=row_sum, column=3, value=cn_key)
                    install_files.install(row=row_sum, column=4, value=contactSiteSourceMap_search_value["value"])
                    install_files.install(row=row_sum, column=5, value=cv_key["value"])
                    install_files.install(row=row_sum, column=6, value='搜索结果为空')
                    # print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
                for i in pid_list:
                    details_response = search(host).skb_contacts_num(id=i['pid'], module='advance_search_detail')
                    details_response_contacts_num = details_response.json()['data']['contacts']
                    details_response_contactNum = details_response.json()['data']['contactNum']
                    details_response.close()
                    if details_response_contacts_num:
                        contact_way_response = details_response_contacts_num
                    elif details_response_contacts_num == [] and details_response_contactNum != 0:
                        detail_response = search(host).skb_contacts(id=i['pid'], entName=i['entName'],
                                                                    module='advance_search_detail')
                        contact_way_response = detail_response.json()['data']['contacts']
                        detail_response.close()
                    else:
                        contact_way_response = []
                        row_sum = row_sum + 1
                        install_files.install(row=row_sum, column=3, value=cn_key)
                        install_files.install(row=row_sum, column=4, value=contactSiteSourceMap_search_value["value"])
                        install_files.install(row=row_sum, column=5, value=cv_key["value"])
                        install_files.install(row=row_sum, column=6, value='联系方式为空')
                        # print('pid:', i, '搜索条件', cv, '\n该企业联系方式有误查询结果为', details_response)
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
                    if cv_key["value"] == "IN":
                        if sources_sum == 0:
                            row_sum = row_sum + 1
                            install_files.install(row=row_sum, column=1, value=i['pid'])
                            install_files.install(row=row_sum, column=2, value=i['entName'])
                            install_files.install(row=row_sum, column=3, value=cn_key)
                            install_files.install(row=row_sum, column=4,
                                                  value=contactSiteSourceMap_search_value["value"])
                            install_files.install(row=row_sum, column=5, value=cv_key["value"])
                            install_files.install(row=row_sum, column=6, value='详情页没有该渠道但是ES有该渠道')
                            # print('pid:', i, '搜索条件', cv, '\n')
                    elif cv_key["value"] == "NOT_IN":
                        if sources_sum != 0:
                            row_sum = row_sum + 1
                            install_files.install(row=row_sum, column=1, value=i['pid'])
                            install_files.install(row=row_sum, column=2, value=i['entName'])
                            install_files.install(row=row_sum, column=3, value=cn_key)
                            install_files.install(row=row_sum, column=4,
                                                  value=contactSiteSourceMap_search_value["value"])
                            install_files.install(row=row_sum, column=5, value=cv_key["value"])
                            install_files.install(row=row_sum, column=6, value='详情页有该渠道但是ES没有该渠道')
                            # print('pid:', i, '搜索条件', cv, '\n')
                    else:
                        print('判断条件出错', cv_key)


if __name__ == '__main__':
    contacts_channel(host=HOST, cn_search=cn_search_list, cv_search=recruitPlatform_config,
                     search_value=staticConfig_list)
