#有无搜索条件自动化case
import pytest, openpyxl, time
# from distutils import version
# from collections import Counter  # 导入表格统计模块
# from API_project.Configs.config_API import configuration_file
from API_project.Configs.search_API import search, getCompanyBaseInfo
from API_project.tools.get_yaml_set import get_yaml_data
HOST = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
RiskInfo_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['RiskInfo']
InterpersonalRelations_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')[
    'InterpersonalRelations']
Development_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['Development']



class Test_have_or_not_search:
    @pytest.mark.parametrize('cv_key', [False,True])
    @pytest.mark.parametrize('Development_search_conditions_value', Development_search_conditions)
    def test_Development_search(self, cv_key,Development_search_conditions_value): # 企业发展页面有无搜索+详情页数据对比case
        cv = [{"cn": Development_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append(pid['id'])
        else:
            print('搜索结果：',pid_responst,'\n搜索条件:',cv,'\n')
            assert pid_responst != []
        for i in pid_list:
            time.sleep(2.1)
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i, section='Development').json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            if cv_key == True:
                assert details_response['data'][Development_search_conditions_value['detail_data']]['total'] != 0
                assert details_response['data'][Development_search_conditions_value['detail_data']]['items'] != []
            elif cv_key == False:
                assert details_response['data'][Development_search_conditions_value['detail_data']]['total'] == 0
                assert details_response['data'][Development_search_conditions_value['detail_data']]['items'] == []

    @pytest.mark.parametrize('cv_key', [False, True])
    @pytest.mark.parametrize('RiskInfo_search_conditions_value', RiskInfo_search_conditions)
    def test_RiskInfo_search(self, cv_key, RiskInfo_search_conditions_value):  # 风险信息页面相关有无搜索条件+详情页数据对比case
        cv = [{"cn": RiskInfo_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
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
            time.sleep(2.1)
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i, section='RiskInfo').json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            if cv_key == True:
                assert details_response['data'][RiskInfo_search_conditions_value['detail_data']]['total'] != 0
                assert details_response['data'][RiskInfo_search_conditions_value['detail_data']]['items'] != []
            elif cv_key == False:
                assert details_response['data'][RiskInfo_search_conditions_value['detail_data']]['total'] == 0
                assert details_response['data'][RiskInfo_search_conditions_value['detail_data']]['items'] == []

    @pytest.mark.parametrize('cv_key', [False, True])
    @pytest.mark.parametrize('InterpersonalRelations_search_conditions_value', InterpersonalRelations_search_conditions)
    def test_InterpersonalRelations_search(self, cv_key,
                                           InterpersonalRelations_search_conditions_value):  # 员工人脉页面相关有无搜索条件+详情页数据对比case
        cv = [{"cn": InterpersonalRelations_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
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
            time.sleep(2.1)
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i, section='InterpersonalRelations').json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            if cv_key == True:
                assert details_response['data'][InterpersonalRelations_search_conditions_value['detail_data']][
                           'total'] != 0
                assert details_response['data'][InterpersonalRelations_search_conditions_value['detail_data']][
                           'items'] != []
            elif cv_key == False:
                assert details_response['data'][InterpersonalRelations_search_conditions_value['detail_data']][
                           'total'] == 0
                assert details_response['data'][InterpersonalRelations_search_conditions_value['detail_data']][
                           'items'] == []


if __name__ == '__main__':
    # print(Test_templateSuppiler_search().test_RiskInfo_search())
    print(Test_have_or_not_search().test_InterpersonalRelations_search())
    # @pytest.mark.parametrize('cv_key', [False,True])
    # # @pytest.mark.parametrize('cn', ['hasLinkedin', 'hasMaimai','hasPersonalBlog'])
    # def test_hasLinkedin_search(self, cn,cv_key): #有无终本案件+详情页数据对比case
    #     cv = [{"cn": 'hasLinkedin', "cr": 'IS', "cv": cv_key}]
    #     time.sleep(2.2)
    #     pid_list = []
    #     pid_responst = search(HOST).advanced_search(cv=cv).json()['data']['items']
    #     if pid_responst:
    #         for pid in pid_responst:
    #             pid_list.append(pid['id'])
    #     else:
    #         print('搜索结果：',pid_responst,'\n搜索条件:',cv,'\n')
    #         assert pid_responst != []
    #     for i in pid_list:
    #         time.sleep(2.1)
    #         details_response = getCompanyBaseInfo(HOST).getEntSectionInfo_RiskInfo_subset(pid=i, subset='LinkedinUserInfo').json()
    #         print('pid:',i,'查询结果\n',details_response, '\n搜索条件',cv,'\n')
    #         if cv_key == True:
    #             assert details_response['data']['LinkedinUserInfo']['total'] != 0
    #         elif cv_key == False:
    #             assert details_response['data']['LinkedinUserInfo']['total'] == 0

# if __name__ == '__main__':
#     print(getCompanyBaseInfo(HOST).getEntSectionInfo_RiskInfo_subset(
#         pid='90c2f9836fe55b385f877f629bc59aee', subset='Executor').json())
