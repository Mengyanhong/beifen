# recruitPlatform:招聘平台高级搜索+详情页筛选

import pytest, openpyxl, time
# from distutils import version
# from collections import Counter  # 导入表格统计模块
from API_project.Configs.config_API import configuration_file
from API_project.Configs.search_API import search, getCompanyBaseInfo

HOST = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
recruitPlatform_config = configuration_file(HOST).conditionConfig()  # 实例化高级搜索配置并返回配置信息
recruitPlatformOption_config = configuration_file(HOST).staticConfig_recruitPlatformOption()  # 实例化经营情况详情页筛选项配置并返回配置信息
staticConfig_IPR_config = configuration_file(HOST).staticConfig_IPR()  # 实例化知识产权详情页筛选项配置并返回配置信息
recruitPlatformOption_config_list = recruitPlatformOption_config['recruitPlatformOption']  # 返回企业详情-经营情况-招聘平台筛选配置信息
templateSuppilerOption_config_list = staticConfig_IPR_config['templateSuppilerOption']  # 返回企业详情-知识产权-建站方筛选配置信息
getEntSectionInfo_search = getCompanyBaseInfo(HOST)  # 实例化高级搜索搜索接口
staticConfig = configuration_file(HOST).staticConfig()['contactSiteSourceMap']  # 实例化高级搜索配置withLevels并返回配置信息
staticConfig_list = []
for staticConfig_value in staticConfig:
    staticConfig_list = staticConfig_list + staticConfig_value['sub']


class Test_recruitPlatform_search:  # 招聘平台高级搜索+详情页筛选case
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('recruitPlatform_config_value',
                             recruitPlatform_config['recruitPlatform']['cv']['options'])  # 返回高级搜索招聘平台配置列表
    def test_recruitPlatform_search(self, recruitPlatform_config_value, cr):
        recruitPlatformOption_config_list_sum = len(recruitPlatformOption_config_list)
        sourceName_sum = 0
        for sourceName in recruitPlatformOption_config_list:
            if recruitPlatform_config_value['label'] == sourceName['label']:
                sourceName_value = sourceName['value']
                break
            else:
                sourceName_sum += 1
                if sourceName_sum == recruitPlatformOption_config_list_sum:
                    print('高级搜索配置和详情页配置不一致\n', recruitPlatformOption_config_list, '\n',
                          recruitPlatform_config_value['label'])
                    assert sourceName_sum != recruitPlatformOption_config_list_sum
                else:
                    continue
        cv = [{"cn": "recruitPlatform", "cr": cr, "cv": [recruitPlatform_config_value['value']]}]
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append(pid['id'])
        else:
            print('筛选结果：', pid_responst, '\n招聘平台:', recruitPlatform_config_value)
            assert pid_responst != []
        for i in pid_list:
            sourceName_search = getEntSectionInfo_search.getEntSectionInfo_ManageInfo(pid=i,
                                                                                      sourceName=sourceName_value).json()
            print(sourceName_search, '\n', i, sourceName_value, '\n', recruitPlatform_config_value)
            if cr == "IN":
                assert sourceName_search['data']['RecruitmentDetail']['total'] != 0
                for item in sourceName_search['data']['RecruitmentDetail']['items']:
                    assert item['sourceName'] == recruitPlatform_config_value['label']
            elif cr == "NOT_IN":
                assert sourceName_search['data']['RecruitmentDetail']['total'] == 0


class Test_templateSuppiler_search:  # 建站方高级搜索+详情页筛选case
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('templateSuppiler_config_value',
                             recruitPlatform_config['templateSuppiler']['cv']['options'])  # 返回高级搜索建站方搜索配置列表
    def test_recruitPlatform_search(self, templateSuppiler_config_value, cr):
        templateSuppilerOption_config_list_sum = len(templateSuppilerOption_config_list)
        template_sum = 0
        for template in templateSuppilerOption_config_list:
            if templateSuppiler_config_value['label'] == template['label']:
                templateSuppiler_value = template['value']
                break
            else:
                template_sum += 1
                if template_sum == templateSuppilerOption_config_list_sum:
                    print('高级搜索配置和详情页配置不一致\n', templateSuppilerOption_config_list, '\n',
                          templateSuppiler_config_value['label'])
                    templateSuppiler_value = None
                else:
                    continue
                assert template_sum != templateSuppilerOption_config_list_sum
        cv = [{"cn": "templateSuppiler", "cr": cr, "cv": [templateSuppiler_config_value['value']]}]
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append(pid['id'])
        else:
            print('筛选结果：', pid_responst, '\n建站方:', templateSuppiler_config_value)
            assert pid_responst != []
        for i in pid_list:
            template_search = getEntSectionInfo_search.getEntSectionInfo_IPR(pid=i,
                                                                             templateSuppiler=templateSuppiler_value).json()
            print(template_search, '\n', i, templateSuppiler_value, '\n', templateSuppiler_config_value)
            if cr == "IN":
                assert template_search['data']['WebsiteInformation']['total'] != 0
                id_value_list = []
                for item in template_search['data']['WebsiteInformation']['items']:
                    id_value_list.append(item['_id'])
                for id_value in id_value_list:
                    getWebsiteInfo_templateSuppiler = getEntSectionInfo_search.getWebsiteInfo(_id=id_value).json()
                    if getWebsiteInfo_templateSuppiler['data'] != {}:
                        assert getWebsiteInfo_templateSuppiler['data']['webModule'][
                                   'templateSuppiler'] == templateSuppiler_value
                    else:
                        print('pid', i, '建站方', templateSuppiler_value, '网址id', id_value, '\n网址详情',
                              getWebsiteInfo_templateSuppiler)
                        assert getWebsiteInfo_templateSuppiler['data'] != {}

            elif cr == "NOT_IN":
                assert template_search['data']['WebsiteInformation']['total'] == 0


class Test_techTypeCompany:  # 企业发展
    @pytest.mark.parametrize('cv_key', recruitPlatform_config['techTypeCompany']['cr']['options'])  # 企业发展-企业标签搜索
    @pytest.mark.parametrize('techTypeCompany_search_value', recruitPlatform_config['techTypeCompany']['cv']['options'])
    def test_techTypeCompany_search(self, cv_key,
                                    techTypeCompany_search_value):  # 企业发展-科技型企业+详情页数据对比case
        cv = [{"cn": "techTypeCompany", "cr": cv_key["value"], "cv": [techTypeCompany_search_value['value']]}]
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append(pid['id'])
        else:
            print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
        for i in pid_list:
            time.sleep(2.2)
            details_response = getCompanyBaseInfo(HOST).getCompanyBase(pid=i).json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            order_sum = 0
            if details_response['data']['tags']:
                for order in details_response['data']['tags']:
                    if 'tagName' in order.keys():
                        if order["category"] == "科技型企业标签":
                            if order['tagName'] == techTypeCompany_search_value['label']:
                                order_sum += 1
                            else:
                                continue
                    elif 'tag_name' in order.keys():
                        if order["category"] == "科技型企业标签":
                            if order['tag_name'] == techTypeCompany_search_value['label']:
                                order_sum += 1
                            else:
                                continue
                    else:
                        continue
            else:
                print('pid:', i, '搜索结果错误\n搜索条件', cv, '\n')
                continue
            if cv_key["value"] == "IN":
                assert order_sum != 0
            elif cv_key["value"] == "NOT_IN":
                assert order_sum == 0
            else:
                print('判断条件错误', cv_key)


class Test_contact_way:  # 联系方式
    @pytest.mark.parametrize('host', [HOST])
    @pytest.mark.parametrize('cn_key', ["contactSource", "mobileSource", "fixedSource"])  # 联系方式渠道"contactSource", "mobileSource", "fixedSource"
    @pytest.mark.parametrize('cv_key', recruitPlatform_config['contactSource']['cr']['options'])  # 联系方式渠道
    @pytest.mark.parametrize('contactSiteSourceMap_search_value', staticConfig_list)
    def test_contacts_channel(self, host, cn_key, cv_key,
                              contactSiteSourceMap_search_value):  # 联系方式渠道+详情页数据对比case
        cv = [{"cn": cn_key, "cr": cv_key["value"], "cv": [contactSiteSourceMap_search_value["name"]]}]
        pid_list = []
        time.sleep(2.2)
        pid_responst = search(host).advanced_search(cv=cv, page=2, pagesize=1).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        else:
            print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
        for i in pid_list:
            details_response = search(host).skb_contacts_num(id=i['pid'], module='advance_search_detail')
            details_response_contacts_num = details_response.json()['data']['contacts']
            details_response_contactNum = details_response.json()['data']['contactNum']
            details_response.close()
            contact_way_response = None
            if details_response_contacts_num:
                contact_way_response = details_response_contacts_num
            elif details_response_contacts_num == [] and details_response_contactNum != 0:
                detail_response = search(host).skb_contacts(id=i['pid'], entName=i['entName'],
                                                            module='advance_search_detail')
                details_response_contacts = detail_response.json()['data']['contacts']
                detail_response.close()
                contact_way_response = details_response_contacts
            else:
                print('pid:', i, '搜索条件', cv, '\n该企业联系方式有误查询结果为', details_response)
                assert details_response_contacts_num != [] and details_response_contactNum != 0
            assert contact_way_response is not None and contact_way_response != []
            sources_sum = 0
            for contact_response_value in contact_way_response:
                if cn_key == "contactSource":
                    for sources in contact_response_value["sources"]:
                        if contactSiteSourceMap_search_value["value"] == sources["sourceName"]:
                            sources_sum += 1
                            break
                        else:
                            continue
                elif cn_key == "mobileSource":
                    if contact_response_value["type"] == 1:
                        for sources in contact_response_value["sources"]:
                            if contactSiteSourceMap_search_value["value"] == sources["sourceName"]:
                                sources_sum += 1
                                break
                            else:
                                continue
                    else:
                        continue
                else:
                    if contact_response_value["type"] == 2:
                        for sources in contact_response_value["sources"]:
                            if contactSiteSourceMap_search_value["value"] == sources["sourceName"]:
                                sources_sum += 1
                                break
                            else:
                                continue
                    else:
                        continue
            if cv_key["value"] == "IN":
                if sources_sum == 0:
                    print('pid:', i, '搜索条件', cv, '\n')
                assert sources_sum != 0
            elif cv_key["value"] == "NOT_IN":
                if sources_sum != 0:
                    print('pid:', i, '搜索条件', cv, '\n')
                assert sources_sum == 0
            else:
                print('判断条件出错', cv_key)

# if __name__ == '__main__':
#     Test_recruitPlatform_search().test_recruitPlatform_search()
