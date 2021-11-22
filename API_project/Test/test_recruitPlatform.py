# recruitPlatform:招聘平台高级搜索+详情页筛选

import pytest,openpyxl,time
from distutils import version
from collections import Counter  # 导入表格统计模块
from API_project.Configs.config_API import configuration_file
from API_project.Configs.search_API import search, getCompanyBaseInfo

HOST = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
recruitPlatform_config = configuration_file(HOST).conditionConfig()  # 实例化高级搜索配置并返回配置信息
recruitPlatformOption_config = configuration_file(HOST).staticConfig_recruitPlatformOption()  # 实例化详情页筛选项配置并返回配置信息
recruitPlatform_config_list = recruitPlatform_config['recruitPlatform']['cv']['options']  # 返回高级搜索招聘平台配置信息
recruitPlatformOption_config_list = recruitPlatformOption_config['recruitPlatformOption']  # 返回企业详情招聘平台筛选配置信息
getEntSectionInfo_search = getCompanyBaseInfo(HOST)
print(recruitPlatform_config_list, '\n', recruitPlatformOption_config_list)


class Test_recruitPlatform_search:
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('recruitPlatform_config_value', recruitPlatform_config_list)
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
        cv = [{"cn": "recruitPlatform", "cr": cr, "cv": [recruitPlatform_config_value['value']]}]
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append(pid['id'])
        else:
            print('筛选结果：',pid_responst,'\n招聘平台:',recruitPlatform_config_value)
            assert pid_responst != []
        for i in pid_list:
            sourceName_search = getEntSectionInfo_search.getEntSectionInfo(pid=i, sourceName=sourceName_value).json()
            print(sourceName_search, '\n', i, sourceName_value, '\n', recruitPlatform_config_value)
            if cr == "IN":
                assert sourceName_search['data']['RecruitmentDetail']['total'] != 0
            elif cr == "NOT_IN":
                assert sourceName_search['data']['RecruitmentDetail']['total'] == 0


if __name__ == '__main__':
    Test_recruitPlatform_search().test_recruitPlatform_search()
