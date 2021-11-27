import pytest, openpyxl, time
# from distutils import version
# from collections import Counter  # 导入表格统计模块
from API_project.Configs.config_API import configuration_file
from API_project.Configs.search_API import search, getCompanyBaseInfo

HOST = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
recruitPlatform_config = configuration_file(HOST).conditionConfig()  # 实例化高级搜索配置并返回配置信息
recruitPlatform_config_list = recruitPlatform_config['recruitPlatform']['cv']['options']  # 返回高级搜索招聘平台配置列表


class Test_templateSuppiler_search:  # 有无企业年报搜索+详情页数据对比case
    # @pytest.mark.parametrize('cv_key', [False,True])
    # def test_hasAnnu_search(self, cv_key):
    #     cv = [{"cn": "hasAnnu", "cr": 'IS', "cv": cv_key}]
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
    #         details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i, section='Development').json()
    #         print('pid:',i,'查询结果\n',details_response, '\n搜索条件',cv,'\n')
    #         if cv_key == True:
    #             assert details_response['data']['AnnualReport']['items']['total'] != 0
    #         elif cv_key == False:
    #             assert details_response['data']['AnnualReport']['items']['total'] == 0

    @pytest.mark.parametrize('cv_key', [False, True])
    def test_EndBookInfo_search(self, cv_key):  # 有无终本案件+详情页数据对比case
        cv = [{"cn": "hasEndBook", "cr": 'IS', "cv": cv_key}]
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
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo_RiskInfo_subset(pid=i,
                                                                                          subset='EndBookInfo').json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            if cv_key == True:
                assert details_response['data']['EndBookInfo']['total'] != 0
            elif cv_key == False:
                assert details_response['data']['EndBookInfo']['total'] == 0

    @pytest.mark.parametrize('cv_key', [False,True])
    # @pytest.mark.parametrize('cn', ['hasLinkedin', 'hasMaimai','hasPersonalBlog'])
    def test_hasLinkedin_search(self, cn,cv_key): #有无终本案件+详情页数据对比case
        cv = [{"cn": 'hasLinkedin', "cr": 'IS', "cv": cv_key}]
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
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo_RiskInfo_subset(pid=i, subset='LinkedinUserInfo').json()
            print('pid:',i,'查询结果\n',details_response, '\n搜索条件',cv,'\n')
            if cv_key == True:
                assert details_response['data']['LinkedinUserInfo']['total'] != 0
            elif cv_key == False:
                assert details_response['data']['LinkedinUserInfo']['total'] == 0

# if __name__ == '__main__':
#     print(getCompanyBaseInfo(HOST).getEntSectionInfo_RiskInfo_subset(
#         pid='90c2f9836fe55b385f877f629bc59aee', subset='Executor').json())
