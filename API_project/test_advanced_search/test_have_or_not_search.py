# 有无搜索条件自动化case
import pytest, openpyxl, time
# from distutils import version
# from collections import Counter  # 导入表格统计模块
# from API_project.Configs.config_API import configuration_file
from API_project.Configs.search_API import search, getCompanyBaseInfo
from API_project.tools.get_yaml_set import get_yaml_data

HOST = "staging"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
RiskInfo_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['RiskInfo']
InterpersonalRelations_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')[
    'InterpersonalRelations']
Development_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['Development']
BaseInfo_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['BaseInfo']
contacts_num_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['contacts_num']


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
    def test_Development_search(self, cv_key, Development_search_conditions_value):  # 企业发展页面有无搜索+详情页数据对比case
        cv = [{"cn": Development_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
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
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i, section='Development').json()
            print('pid:', i, '查询结果\n', details_response, '\n搜索条件', cv, '\n')
            if Development_search_conditions_value['conditions'] == 'hasAnnualInvestment':
                AnnualReport_investment_sum = 0
                for AnnualReport_items_id in details_response['data']['AnnualReport']['items']:
                    AnnualReport_data = getCompanyBaseInfo(HOST).getAnnualReportDetail(
                        annualReportId=AnnualReport_items_id['annualReportId']).json()['data']
                    print(AnnualReport_data)
                    if AnnualReport_data['investment']['total'] != 0:
                        AnnualReport_investment_sum += 1
                        break
                    else:
                        continue
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

    @pytest.mark.parametrize('cv_key', [True, False])  # 联系方式
    @pytest.mark.parametrize('contacts_num_search_conditions_value', contacts_num_search_conditions)
    def test_contacts_num_search(self, cv_key,
                                 contacts_num_search_conditions_value):  # 联系方式有无搜索条件+详情页数据对比case
        cv = [{"cn": contacts_num_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
        pid_list = []
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
            hasMobile_sum = 0
            hasFixed_sum = 0
            hasEmail_sum = 0
            hasQq_sum = 0
            if details_response_contacts != []:
                print('查询结果\n', details_response_contacts, 'pid:', i, '\n搜索条件', cv, '\n')
                for details_response_value in details_response_contacts:
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
                            hasEmail_sum += 1
                            break
                        else:
                            continue
                    elif contacts_num_search_conditions_value['detail_data'] == 4:
                        if details_response_value['type'] == 4:
                            hasQq_sum += 1
                            break
                        else:
                            continue
                    else:
                        print('搜索条件号码类型错误', contacts_num_search_conditions_value)
                        assert contacts_num_search_conditions_value['detail_data'] == 1 or \
                               contacts_num_search_conditions_value['detail_data'] == 2 or \
                               contacts_num_search_conditions_value['detail_data'] == 3 or \
                               contacts_num_search_conditions_value['detail_data'] == 4
            elif details_response_contacts == [] and details_response_contactNum != 0:
                detail_response = search(HOST).skb_contacts(id=i['pid'], entName=i['entName'],
                                                            module='advance_search_detail')
                detail_response_contacts = detail_response.json()['data']['contacts']
                detail_response.close()
                if detail_response_contacts != []:
                    print('pid:', i, '查询结果\n', detail_response_contacts, '\n搜索条件', cv, '\n')
                    for contact_value in detail_response_contacts:
                        if contacts_num_search_conditions_value['detail_data'] == 1:
                            if contact_value['type'] == 1:
                                hasMobile_sum += 1
                                break
                            else:
                                continue
                        elif contacts_num_search_conditions_value['detail_data'] == 2:
                            if contact_value['type'] == 2:
                                hasFixed_sum += 1
                                break
                            else:
                                continue
                        elif contacts_num_search_conditions_value['detail_data'] == 3:
                            if contact_value['type'] == 3:
                                hasEmail_sum += 1
                                break
                            else:
                                continue
                        elif contacts_num_search_conditions_value['detail_data'] == 4:
                            if contact_value['type'] == 4:
                                hasQq_sum += 1
                                break
                            else:
                                continue
                        else:
                            print('搜索条件号码类型错误', contacts_num_search_conditions_value)
                            assert contacts_num_search_conditions_value['detail_data'] == 1 or \
                                   contacts_num_search_conditions_value['detail_data'] == 2 or \
                                   contacts_num_search_conditions_value['detail_data'] == 3 or \
                                   contacts_num_search_conditions_value['detail_data'] == 4
                else:
                    print('联系方式获取失败')
                    print('pid:', i, '查询结果\n', detail_response_contacts, '\n搜索条件', cv, '\n')
                    assert detail_response_contacts != []

            else:
                print('该企业联系方式为空')
                print('pid:', i, '查询结果\n', details_response_contactNum, '\n搜索条件', cv, '\n')
                assert details_response_contacts != [] and details_response_contactNum != 0
            if cv_key == True:
                if contacts_num_search_conditions_value['detail_data'] == 1:
                    assert hasMobile_sum != 0
                elif contacts_num_search_conditions_value['detail_data'] == 2:
                    assert hasFixed_sum != 0
                elif contacts_num_search_conditions_value['detail_data'] == 3:
                    assert hasEmail_sum != 0
                elif contacts_num_search_conditions_value['detail_data'] == 4:
                    assert hasQq_sum != 0
                else:
                    print('pid:', i, '搜索条件有误', contacts_num_search_conditions_value)
                    assert contacts_num_search_conditions_value['detail_data'] == 1 or \
                           contacts_num_search_conditions_value['detail_data'] == 2 or \
                           contacts_num_search_conditions_value['detail_data'] == 3 or \
                           contacts_num_search_conditions_value['detail_data'] == 4
            elif cv_key == False:
                if contacts_num_search_conditions_value['detail_data'] == 1:
                    assert hasMobile_sum == 0
                elif contacts_num_search_conditions_value['detail_data'] == 2:
                    assert hasFixed_sum == 0
                elif contacts_num_search_conditions_value['detail_data'] == 3:
                    assert hasEmail_sum == 0
                elif contacts_num_search_conditions_value['detail_data'] == 4:
                    assert hasQq_sum == 0
                else:
                    print('pid:', i, '搜索条件有误', contacts_num_search_conditions_value)
                    assert contacts_num_search_conditions_value['detail_data'] == 1 or \
                           contacts_num_search_conditions_value['detail_data'] == 2 or \
                           contacts_num_search_conditions_value['detail_data'] == 3 or \
                           contacts_num_search_conditions_value['detail_data'] == 4
            else:
                print('pid:', i, '判断条件错误', cv_key)
                assert cv_key == False or cv_key == True

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

# if __name__ == '__main__':
#     print(getCompanyBaseInfo(HOST).getEntSectionInfo_RiskInfo_subset(
#         pid='90c2f9836fe55b385f877f629bc59aee', subset='Executor').json())
