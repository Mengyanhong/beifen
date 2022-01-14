# 有无搜索条件自动化case
import pytest, openpyxl, time
# from distutils import version
# from collections import Counter  # 导入表格统计模块
# from API_project.Configs.config_API import configuration_file
from API_project.Configs.search_API import search, getCompanyBaseInfo
from API_project.Configs.config_API import configuration_file
from API_project.tools.get_yaml_set import get_yaml_data
from API_project.tools.install_Excel import install_Excel

file_name = time.strftime("%Y年%m月%d日%H时%M分")

HOST = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
recruitPlatform_config = configuration_file(HOST).conditionConfig()  # 实例化高级搜索配置并返回配置信息
contacts_num_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['contacts_num']
staticConfig = configuration_file(HOST).staticConfig()['contactSiteSourceMap']  # 实例化高级搜索配置withLevels并返回配置信息
staticConfig_list = []
for staticConfig_value in staticConfig:
    staticConfig_list = staticConfig_list + staticConfig_value['sub']


class Test_contact:
    @pytest.mark.parametrize('cv_key', [True, False])  # 联系方式
    @pytest.mark.parametrize('contacts_num_search_conditions_value', contacts_num_search_conditions)
    def test_contacts_num_search(self, cv_key,
                                 contacts_num_search_conditions_value, ES):  # 联系方式有无搜索条件+详情页数据对比case
        cv = [{"cn": contacts_num_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
        pid_list = []
        time.sleep(2.2)
        pid_responst = search(HOST).advanced_search(cv=cv, page=2, pagesize=20).json()['data']['items']
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
        pid_responst = search(HOST).advanced_search(cv=cv).json()['data']['items']
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
        pid_responst = search(HOST).advanced_search(cv=cv).json()['data']['items']
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

    @pytest.mark.parametrize('host', [HOST])
    @pytest.mark.parametrize('cn_key', ["contactSource", "mobileSource",
                                        "fixedSource"])  # 联系方式渠道"contactSource", "mobileSource", "fixedSource"
    @pytest.mark.parametrize('cv_key', recruitPlatform_config['contactSource']['cr']['options'])  # 联系方式渠道
    @pytest.mark.parametrize('contactSiteSourceMap_search_value', staticConfig_list)
    def test_contacts_channel(self, host, cn_key, cv_key,
                              contactSiteSourceMap_search_value):  # 联系方式渠道+详情页数据对比case
        install_files = install_Excel(file_name="0102迭代联系方式渠道", file_title_name=file_name)  # 实例化测试报告文件
        if install_files.read_sum() == 1 and install_files.read_one_value() is None:
            install_files.install(row=1, column=1, value='pid')
            install_files.install(row=1, column=2, value='entName')
            install_files.install(row=1, column=3, value='搜索条件')
            install_files.install(row=1, column=4, value='搜索渠道')
            install_files.install(row=1, column=5, value='过滤条件')
            install_files.install(row=1, column=6, value='测试结果')
        cv = [{"cn": cn_key, "cr": cv_key["value"], "cv": [contactSiteSourceMap_search_value["name"]]}]
        pid_list = []
        time.sleep(2.2)
        pid_responst = search(host).advanced_search(cv=cv, page=2, pagesize=1).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        else:
            row_sum = install_files.read_sum() + 1
            install_files.install(row=row_sum, column=3, value=cn_key)
            install_files.install(row=row_sum, column=4, value=contactSiteSourceMap_search_value["value"])
            install_files.install(row=row_sum, column=5, value=cv_key["value"])
            install_files.install(row=row_sum, column=6, value='搜索结果为空')
            print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
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
                details_response_contacts = detail_response.json()['data']['contacts']
                detail_response.close()
                contact_way_response = details_response_contacts
            else:
                contact_way_response = []
                row_sum = install_files.read_sum() + 1
                install_files.install(row=row_sum, column=3, value=cn_key)
                install_files.install(row=row_sum, column=4, value=contactSiteSourceMap_search_value["value"])
                install_files.install(row=row_sum, column=5, value=cv_key["value"])
                install_files.install(row=row_sum, column=6, value='联系方式为空')
                print('pid:', i, '搜索条件', cv, '\n该企业联系方式有误查询结果为', details_response)
                assert details_response_contacts_num != [] and details_response_contactNum != 0
            assert contact_way_response is not None and contact_way_response != []
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
                    row_sum = install_files.read_sum() + 1
                    install_files.install(row=row_sum, column=1, value=i['pid'])
                    install_files.install(row=row_sum, column=2, value=i['entName'])
                    install_files.install(row=row_sum, column=3, value=cn_key)
                    install_files.install(row=row_sum, column=4,
                                          value=contactSiteSourceMap_search_value["value"])
                    install_files.install(row=row_sum, column=5, value=cv_key["value"])
                    install_files.install(row=row_sum, column=6, value='详情页没有该渠道但是ES有该渠道')
                    print('pid:', i, '搜索条件', cv, '\n')
                assert sources_sum != 0
            elif cv_key["value"] == "NOT_IN":
                if sources_sum != 0:
                    row_sum = install_files.read_sum() + 1
                    install_files.install(row=row_sum, column=1, value=i['pid'])
                    install_files.install(row=row_sum, column=2, value=i['entName'])
                    install_files.install(row=row_sum, column=3, value=cn_key)
                    install_files.install(row=row_sum, column=4,
                                          value=contactSiteSourceMap_search_value["value"])
                    install_files.install(row=row_sum, column=5, value=cv_key["value"])
                    install_files.install(row=row_sum, column=6, value='详情页有该渠道但是ES没有该渠道')
                    print('pid:', i, '搜索条件', cv, '\n')
                assert sources_sum == 0
            else:
                print('判断条件出错', cv_key)


