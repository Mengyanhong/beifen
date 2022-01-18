# 有无搜索条件自动化case
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
BaseInfo_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['BaseInfo']
contacts_num_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['contacts_num']
from API_project.tools.Excelread import Excel_Files


# excel_file = Excel_Files(file_name="nianbao.xlsx", sheel="pid")  # 实例化Excel用例文件


class Test_have_or_not_search:
    @pytest.mark.parametrize('cv_key', [False, True])  # 基本信息
    @pytest.mark.parametrize('BaseInfo_search_conditions_value', BaseInfo_search_conditions)
    def test_BaseInfo_search(self, cv_key, BaseInfo_search_conditions_value):  # 基本信息页面有无搜索+详情页数据对比case
        cv = [{"cn": BaseInfo_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
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
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i, section='BaseInfo').json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            if cv_key == True:
                if BaseInfo_search_conditions_value['conditions'] == 'hasRegCCap':
                    print(BaseInfo_search_conditions_value)
                    assert details_response['data']['GSInfo']['regccap'] != '-'
                else:
                    assert details_response['data'][BaseInfo_search_conditions_value['detail_data']]['total'] != 0
                    assert details_response['data'][BaseInfo_search_conditions_value['detail_data']]['items'] != []
            elif cv_key == False:
                if BaseInfo_search_conditions_value['conditions'] == 'hasRegCCap':
                    print(BaseInfo_search_conditions_value)
                    assert details_response['data']['GSInfo']['regccap'] == '-'
                else:
                    assert details_response['data'][BaseInfo_search_conditions_value['detail_data']]['total'] == 0
                    assert details_response['data'][BaseInfo_search_conditions_value['detail_data']]['items'] == []
            else:
                print('判断条件错误', cv_key)

    @pytest.mark.parametrize('cv_key', [False, True])  # 企业发展
    @pytest.mark.parametrize('Development_search_conditions_value', Development_search_conditions)
    def test_Development_search(self, cv_key, Development_search_conditions_value, ES):  # 企业发展页面有无搜索+详情页数据对比case
        cv = [{"cn": Development_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv, page=3, pagesize=100).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append(pid['id'])
        else:
            print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
        for i in pid_list:
            time.sleep(2.1)
            es_result = ES.get(index="company_info_prod", id=i)['_source']
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i, section='Development').json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            if Development_search_conditions_value['conditions'] == 'hasAnnualInvestment':
                AnnualReport_investment_sum = 0
                employees_value = details_response['data']['AnnualReport']['items'][0]["socialSecNum"]
                for AnnualReport_items_id in details_response['data']['AnnualReport']['items']:
                    AnnualReport_data = getCompanyBaseInfo(HOST).getAnnualReportDetail(
                        annualReportId=AnnualReport_items_id['annualReportId']).json()['data']
                    print(AnnualReport_data)
                    if AnnualReport_data['investment']['total'] != 0:
                        AnnualReport_investment_sum += 1
                        break
                    else:
                        continue
                if employees_value == "":
                    assert es_result["employees"] is None
                else:
                    employees = employees_value.strip("人")
                    assert es_result["employees"] == int(employees)
                if cv_key == True:
                    assert AnnualReport_investment_sum != 0
                elif cv_key == False:
                    assert AnnualReport_investment_sum == 0
                else:
                    print('判断条件错误', cv_key)
            else:
                if cv_key == True:
                    assert details_response['data'][Development_search_conditions_value['detail_data']]['total'] != 0
                    assert details_response['data'][Development_search_conditions_value['detail_data']]['items'] != []
                elif cv_key == False:
                    assert details_response['data'][Development_search_conditions_value['detail_data']]['total'] == 0
                    assert details_response['data'][Development_search_conditions_value['detail_data']]['items'] == []
                else:
                    print('判断条件错误', cv_key)

    @pytest.mark.parametrize('pid', Excel_Files(file_name="nianbao.xlsx", sheel="pid").open_file_rows("pid"))  # 年报抽查
    def test_AnnualReport(self, pid, ES):  # 企业发展页面+详情页/ES数据对比
        time.sleep(2.1)
        details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=pid, section='Development').json()
        es_result = ES.get(index="company_info_prod", id=pid)['_source']
        AnnualReport_investment_sum = 0

        if details_response['data']["AnnualReport"]['total'] != 0:
            employees_value = details_response['data']['AnnualReport']['items'][0]["socialSecNum"]
            for AnnualReport_items_id in details_response['data']['AnnualReport']['items']:
                AnnualReport_data = getCompanyBaseInfo(HOST).getAnnualReportDetail(
                    annualReportId=AnnualReport_items_id['annualReportId']).json()['data']
                print(AnnualReport_data)
                if AnnualReport_data['investment']['total'] != 0:
                    AnnualReport_investment_sum += 1
                    break
                else:
                    continue
            if employees_value == "":
                assert es_result["employees"] is None
            else:
                employees = employees_value.strip("人")
                assert es_result["employees"] == int(employees)
            assert details_response['data']["AnnualReport"]['total'] != 0
            assert details_response['data']["AnnualReport"]['items'] != []
            assert "hasAnnu" in es_result.keys() and es_result["hasAnnu"] is True
            if AnnualReport_investment_sum != 0:
                assert "hasAnnualInvestment" in es_result.keys() and es_result["hasAnnualInvestment"] is True
            else:
                assert "hasAnnualInvestment" not in es_result.keys() or es_result["hasAnnualInvestment"] is False
        else:
            assert "employees" not in es_result.keys() or es_result["employees"] == 0 or es_result["employees"] is None
            assert details_response['data']["AnnualReport"]['total'] == 0
            assert details_response['data']["AnnualReport"]['items'] == []
            assert "hasAnnu" not in es_result.keys() or es_result["hasAnnu"] is False
            assert "hasAnnualInvestment" not in es_result.keys() or es_result["hasAnnualInvestment"] is False

    @pytest.mark.parametrize('cv_key', [False, True])  # 风险信息
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
            else:
                print('判断条件错误', cv_key)

    @pytest.mark.parametrize('cv_key', [False, True])  # 员工人脉
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
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i,
                                                                          section='InterpersonalRelations').json()
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
            else:
                print('判断条件错误', cv_key)

    @pytest.mark.parametrize('cv_key', [False, True])  # 企业发展-企业标签搜索
    @pytest.mark.parametrize('getCompanyBaseInfo_search_conditions_value',
                             get_yaml_data('../data/yaml/have_or_not_search.yaml')['getCompanyBaseInfo'])
    def test_getCompanyBaseInfo_search(self, cv_key,
                                       getCompanyBaseInfo_search_conditions_value):  # 基本信息页面有无搜索+详情页数据对比case
        cv = [{"cn": getCompanyBaseInfo_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
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
            details_response = getCompanyBaseInfo(HOST).getCompanyBase(pid=i).json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            order_sum = 0
            if details_response['data']['tags'] != []:
                for order in details_response['data']['tags']:
                    if 'order' in order.keys():
                        if order['order'] == getCompanyBaseInfo_search_conditions_value['detail_data']:
                            order_sum += 1
                        else:
                            continue
                    else:
                        continue
            else:
                print('pid:', i, '搜索结果错误\n搜索条件', cv, '\n')
                continue
            if cv_key == True:
                assert order_sum != 0
            elif cv_key == False:
                assert order_sum == 0
            else:
                print('判断条件错误', cv_key)


class Test_ManageInfo:
    # 行政许可
    @pytest.mark.parametrize('cv_key', [False, True])
    @pytest.mark.parametrize('ManageInfo_value', get_yaml_data('../data/yaml/have_or_not_search.yaml')['ManageInfo'])
    def test_hasAdminLicense(self, cv_key, ManageInfo_value, ES):  # 企业发展页面有无搜索+详情页数据对比case
        cv = [{"cn": ManageInfo_value['conditions'], "cr": 'IS', "cv": cv_key}]
        header = {
            'app_token': "f6620ff6729345c8b6101174e695d0ab",
            'authorization': "Token token=40fa13a7bc1136a7d1a198d345015d16",
            'content-type': 'application/json',
            'crm_platform_type': "ikcrm"
        }
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv, headers=header, page=10, pagesize=50).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append(pid['id'])
        else:
            print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
        for i in pid_list:
            time.sleep(2.1)
            es_result = ES.get(index="company_info_prod", id=i)['_source']
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i, headers=header,
                                                                          section='ManageInfo').json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            if ManageInfo_value['conditions'] == 'hasAdminLicense':
                if details_response['data'][ManageInfo_value['detail_data']]['total'] > 0:
                    valFrom_list = []
                    valTo_list = []
                    licAnth_list = []  # 许可机关
                    licItem_list = []  # 许可内容
                    ES_valFrom_list = []
                    ES_valTo_list = []
                    licenseCount = details_response['data'][ManageInfo_value['detail_data']]['total']  # 许可数量
                    ES_licenseCount = es_result["licenseCount"]  # 许可数量
                    ES_licAnth_list = es_result["licenseOffice"]  # 许可机关
                    ES_licItem_list = es_result["licenseContent"]  # 许可内容
                    for ES_value in es_result["adminLicense"]:
                        ES_valFrom_list.append(ES_value["createDate"])
                        ES_valTo_list.append(ES_value["expireDate"])
                    if details_response['data'][ManageInfo_value['detail_data']]['items']:
                        for valFrom_value in details_response['data'][ManageInfo_value['detail_data']]['items']:
                            if valFrom_value["valFrom"] != "":
                                valFrom_list.append(valFrom_value["valFrom"])
                            if valFrom_value["valTo"] != "":
                                valTo_list.append(valFrom_value["valTo"])
                            if valFrom_value["licAnth"] != "":
                                licAnth_list.append(valFrom_value["licAnth"])
                            if valFrom_value["licItem"] != "":
                                licItem_list.append(valFrom_value["licItem"])
                    assert licenseCount == ES_licenseCount
                    ES_from = set(valFrom_list).difference(set(ES_valFrom_list))
                    ESn_to = set(valTo_list).difference(set(ES_valTo_list))
                    ESn_anth = set(licAnth_list).difference(set(ES_licAnth_list))
                    ESn_item = set(licItem_list).difference(set(ES_licItem_list))
                    assert len(list(ES_from)) == 0
                    assert len(list(ESn_to)) == 0
                    assert len(list(ESn_anth)) == 0
                    assert len(list(ESn_item)) == 0
                else:
                    assert "licenseCount" not in es_result.keys() or es_result["licenseCount"] == 0
                    assert "licenseOffice" not in es_result.keys() or es_result["licenseOffice"] == []
                    assert "licenseContent" not in es_result.keys() or es_result["licenseContent"] == []
                    assert "adminLicense" not in es_result.keys() or es_result["adminLicense"] == []
            if cv_key == True:
                assert details_response['data'][ManageInfo_value['detail_data']]['total'] != 0
                assert details_response['data'][ManageInfo_value['detail_data']]['items'] != []
            elif cv_key == False:
                assert details_response['data'][ManageInfo_value['detail_data']]['total'] == 0
                assert details_response['data'][ManageInfo_value['detail_data']]['items'] == []
            else:
                print('判断条件错误', cv_key)

    # 行政许可抽测
    @pytest.mark.parametrize('pid', Excel_Files(file_name="adminlicense.xlsx", sheel="pid").open_file_rows("pid"))
    def test_AdminLicense(self, pid, ES):  # 企业发展页面有无搜索+详情页数据对比case
        header = {
            'app_token': "f6620ff6729345c8b6101174e695d0ab",
            'authorization': "Token token=40fa13a7bc1136a7d1a198d345015d16",
            'content-type': 'application/json',
            'crm_platform_type': "ikcrm"
        }
        time.sleep(2.1)
        es_result = ES.get(index="company_info_prod", id=pid)['_source']

        details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=pid, headers=header,
                                                                      section='ManageInfo').json()
        if details_response['data']['AdministrativeLicense']['total'] > 0:
            assert details_response['data']['AdministrativeLicense']['total'] != 0
            assert details_response['data']['AdministrativeLicense']['items'] != []
            valFrom_list = []
            valTo_list = []
            licAnth_list = []  # 许可机关
            licItem_list = []  # 许可内容
            ES_valFrom_list = []
            ES_valTo_list = []
            licenseCount = details_response['data']['AdministrativeLicense']['total']  # 许可数量
            ES_licenseCount = es_result["licenseCount"]  # 许可数量
            ES_licAnth_list = es_result["licenseOffice"]  # 许可机关
            ES_licItem_list = es_result["licenseContent"]  # 许可内容
            if es_result["adminLicense"] !=[] and es_result["adminLicense"] is not None:
                for ES_value in es_result["adminLicense"]:
                    ES_valFrom_list.append(ES_value["createDate"])
                    ES_valTo_list.append(ES_value["expireDate"])
            if details_response['data']['AdministrativeLicense']['items']:
                for valFrom_value in details_response['data']['AdministrativeLicense']['items']:
                    if valFrom_value["valFrom"] != "":
                        valFrom_list.append(valFrom_value["valFrom"])
                    if valFrom_value["valTo"] != "":
                        valTo_list.append(valFrom_value["valTo"])
                    if valFrom_value["licAnth"] != "":
                        licAnth_list.append(valFrom_value["licAnth"])
                    if valFrom_value["licItem"] != "":
                        licItem_list.append(valFrom_value["licItem"])
            assert licenseCount == ES_licenseCount
            ES_from = set(valFrom_list).difference(set(ES_valFrom_list))
            ESn_to = set(valTo_list).difference(set(ES_valTo_list))
            ESn_anth = set(licAnth_list).difference(set(ES_licAnth_list))
            ESn_item = set(licItem_list).difference(set(ES_licItem_list))
            assert len(list(ES_from)) == 0
            assert len(list(ESn_to)) == 0
            assert len(list(ESn_anth)) == 0
            assert len(list(ESn_item)) == 0
        else:
            assert "licenseCount" not in es_result.keys() or es_result["licenseCount"] == 0
            assert "licenseOffice" not in es_result.keys() or es_result["licenseOffice"] == []
            assert "licenseContent" not in es_result.keys() or es_result["licenseContent"] == []
            assert "adminLicense" not in es_result.keys() or es_result["adminLicense"] == [] or es_result["adminLicense"] is  None
            assert details_response['data']['AdministrativeLicense']['total'] == 0
            assert details_response['data']['AdministrativeLicense']['items'] == []


# if __name__ == '__main__':
#     print(getCompanyBaseInfo(HOST).getEntSectionInfo_RiskInfo_subset(
#         pid='90c2f9836fe55b385f877f629bc59aee', subset='Executor').json())
