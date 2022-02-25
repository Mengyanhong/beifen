# 有无搜索条件自动化case
import pytest, openpyxl, time
# from distutils import version
# from collections import Counter  # 导入表格统计模块
# from API_project.Configs.config_API import configuration_file
from API_project.Configs.search_API import search, getCompanyBaseInfo
from API_project.tools.get_yaml_set import get_yaml_data
from API_project.tools.install_Excel import install_Excel

file_name = time.strftime("%Y年%m月%d日%H时%M分")
HOST = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
RiskInfo_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['RiskInfo']
InterpersonalRelations_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')[
    'InterpersonalRelations']
Development_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['Development']
BaseInfo_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['BaseInfo']
contacts_num_search_conditions = get_yaml_data('../data/yaml/have_or_not_search.yaml')['contacts_num']
from API_project.tools.Excelread import Excel_Files
headersss = {
                'app_token': 'f6620ff6729345c8b6101174e695d0ab',
                'authorization': 'Token token=503ecbad1cfb9ac85d2da95c63ea9a47',
                'content-type': 'application/json',
                'crm_platform_type': 'ikcrm'
            }

# excel_file = Excel_Files(file_name="nianbao.xlsx", sheel="pid")  # 实例化Excel用例文件


class Test_have_or_not_search:
    # 基本信息
    @pytest.mark.parametrize('cv_key', [False, True])
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

    # 企业发展
    @pytest.mark.parametrize('cv_key', [False, True])
    @pytest.mark.parametrize('Development_search_conditions_value', Development_search_conditions)
    def test_Development_search(self, cv_key, Development_search_conditions_value, ES):  # 企业发展页面有无搜索+详情页数据对比case
        cv = [{"cn": Development_search_conditions_value['conditions'], "cr": 'IS', "cv": cv_key}]
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv, page=3, pagesize=10).json()['data']['items']
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

    # 年报抽查
    @pytest.mark.parametrize('pid', Excel_Files(file_name="nianbao.xlsx", sheel="pid").open_file_rows("pid"))
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

    # 参展信息抽查
    # @pytest.mark.parametrize('pid',
    #                          Excel_Files(file_name="聚合查询.xlsx", sheel="聚合查询").open_file_rows("_id.PID")[5500:6000:3])
    @pytest.mark.parametrize('pid',
                             Excel_Files(file_name="参展信息聚合查询大于10条.xlsx", sheel="聚合查询").open_file_rows("_id.PID")[1:20])
    # @pytest.mark.parametrize('pid',
    #                          Excel_Files(file_name="TradeShowEnts.xlsx", sheel="TradeShowEnts").open_file_rows("PID")[5500:6000:3])
    def test_TradeShow(self, pid, ES):  # 企业发展页面+详情页/ES数据对比
        install_files = install_Excel(file_name="参展信息3", file_title_name=file_name)  # 实例化测试报告文件
        if install_files.read_sum() == 1 and install_files.read_one_value() is None:
            install_files.install(row=1, column=1, value='pid')
            install_files.install(row=1, column=2, value='断言字段')
            install_files.install(row=1, column=3, value='测试结果')
            install_files.install(row=1, column=4, value='测试数据')
        time.sleep(2.1)
        details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=pid, section='ManageInfo', headers=headersss).json()
        totals = details_response['data']["TradeShow"]['total']
        TradeShow_startDatess = None
        TradeShow_endDatess = None
        TradeShow_namess = None
        try:
            es_result = ES.get(index="company_info_prod", id=pid)['_source']
        except:
            es_result = None
        if es_result is not None and "entName" in es_result.keys():
            startDate_list = []
            if totals != 0:
                totalsvaluesum = 0
                for AnnualReport_items_id in details_response['data']['TradeShow']['items']:
                    TradeShow_startDates = AnnualReport_items_id["startDate"]
                    TradeShow_endDates = AnnualReport_items_id["endDate"]
                    TradeShow_names = AnnualReport_items_id["name"]
                    if totalsvaluesum == 0:
                        TradeShow_startDatess = TradeShow_startDates
                        TradeShow_endDatess = TradeShow_endDates
                        TradeShow_namess = TradeShow_names

                    if TradeShow_startDates != "":
                        startDate_list.append(
                            time.strftime("%Y-%m-%d", time.localtime(int(AnnualReport_items_id["startDate"]) / 1000)))
                    else:
                        row_sum = install_files.read_sum() + 1
                        install_files.install(row=row_sum, column=1, value=pid)
                        install_files.install(row=row_sum, column=2, value='startDate')
                        install_files.install(row=row_sum, column=3, value='startDate为空')
                    totalsvaluesum += 1

                if 10 < totals:
                    totals_num = round(totals // 10)
                    totals_nums = round(totals / 10, 2)
                    if totals_nums > totals_num:
                        totals_num = totals_num + 2
                    else:
                        totals_num = totals_num + 1
                    for totalss in range(2, totals_num):
                        time.sleep(3)
                        details_responses = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=pid,
                                                                                       section='ManageInfo',
                                                                                       label='TradeShow',
                                                                                       page=totalss, headers=headersss).json()
                        for AnnualReport_items_ids in details_responses['data']['TradeShow']['items']:
                            if AnnualReport_items_ids["startDate"] != "":
                                startDate_list.append(time.strftime("%Y-%m-%d", time.localtime(
                                    int(AnnualReport_items_ids["startDate"]) / 1000)))
                            else:
                                row_sum = install_files.read_sum() + 1
                                install_files.install(row=row_sum, column=1, value=pid)
                                install_files.install(row=row_sum, column=2, value='startDate')
                                install_files.install(row=row_sum, column=3, value='startDate为空')

                if not details_response['data']["TradeShow"]['items']:
                    row_sum = install_files.read_sum() + 1
                    install_files.install(row=row_sum, column=1, value=pid)
                    install_files.install(row=row_sum, column=2, value='total')
                    install_files.install(row=row_sum, column=3, value='total不为空但是没有相应的展会数据')
                assert details_response['data']["TradeShow"]['items'] != []
                if "hasTradeShow" not in es_result.keys() or es_result["hasTradeShow"] is False:
                    row_sum = install_files.read_sum() + 1
                    install_files.install(row=row_sum, column=1, value=pid)
                    install_files.install(row=row_sum, column=2, value='hasTradeShow')
                    install_files.install(row=row_sum, column=3, value='有展会数据但是搜索不到')
                    install_files.install(row=row_sum, column=4, value=str(es_result["hasTradeShow"]))
                assert "hasTradeShow" in es_result.keys() and es_result["hasTradeShow"] is True
                tradeShowStartDate_list = []
                if es_result["tradeShowStartDate"] is not None and "tradeShowStartDate" in es_result.keys():
                    for es_ti in es_result["tradeShowStartDate"]:
                        # print(type(es_ti))
                        # print(time.strftime("%Y-%m-%d", time.localtime(es_ti)))
                        if es_ti is not None:
                            tradeShowStartDate_list.append(time.strftime("%Y-%m-%d", time.localtime(int(es_ti) / 1000)))
                baseinfo_ES = set(startDate_list).difference(set(tradeShowStartDate_list))
                ES_baseinfo = set(tradeShowStartDate_list).difference(set(startDate_list))
                # print(startDate_list)
                # print(tradeShowStartDate_list)
                if len(baseinfo_ES) != 0:
                    print('详情页有ES没有', baseinfo_ES)
                    row_sum = install_files.read_sum() + 1
                    install_files.install(row=row_sum, column=1, value=pid)
                    install_files.install(row=row_sum, column=2, value='tradeShowStartDate')
                    install_files.install(row=row_sum, column=3, value='ES没有详情页有')
                    install_files.install(row=row_sum, column=4, value=str(baseinfo_ES))
                # assert len(baseinfo_ES) == 0
                if len(ES_baseinfo) != 0:
                    print('ES有详情页没有', ES_baseinfo)
                    row_sum = install_files.read_sum() + 1
                    install_files.install(row=row_sum, column=1, value=pid)
                    install_files.install(row=row_sum, column=2, value='tradeShowStartDate')
                    install_files.install(row=row_sum, column=3, value='ES有详情页没有')
                    install_files.install(row=row_sum, column=4, value=str(ES_baseinfo))
                # assert len(ES_baseinfo) == 0
            else:
                if "hasTradeShow" in es_result.keys() and es_result["hasTradeShow"] is not False:
                    row_sum = install_files.read_sum() + 1
                    install_files.install(row=row_sum, column=1, value=pid)
                    install_files.install(row=row_sum, column=2, value='hasTradeShow')
                    install_files.install(row=row_sum, column=3, value='hasTradeShow搜索错误')
                    install_files.install(row=row_sum, column=4, value=es_result["hasTradeShow"])
                if details_response['data']["TradeShow"]['total'] != 0 or details_response['data']["TradeShow"][
                    'items'] != []:
                    row_sum = install_files.read_sum() + 1
                    install_files.install(row=row_sum, column=1, value=pid)
                    install_files.install(row=row_sum, column=2, value='total')
                    install_files.install(row=row_sum, column=3, value='搜索结果不为空')
                # assert es_result["hasTradeShow"] is False or "hasTradeShow" not in es_result.keys()
                # assert es_result["tradeShowStartDate"] == [] or es_result["tradeShowStartDate"] is None or "tradeShowStartDate" not in es_result.keys()
                assert details_response['data']["TradeShow"]['total'] == 0
                assert details_response['data']["TradeShow"]['items'] == []

            if TradeShow_startDatess != '' and TradeShow_startDatess is not None:
                TradeShow_startDatesss = time.strftime("%Y-%m-%d", time.localtime(int(TradeShow_startDatess) / 1000))
            else:
                TradeShow_startDatesss = None
            if TradeShow_endDatess != '' and TradeShow_endDatess is not None:
                TradeShow_endDatesss = time.strftime("%Y-%m-%d", time.localtime(int(TradeShow_endDatess) / 1000))
            else:
                TradeShow_endDatesss = None
            if TradeShow_namess != '' and TradeShow_namess is not None:
                TradeShow_namesss = TradeShow_namess
            else:
                TradeShow_namesss = None
            if "latestTradeShowStartTime" in es_result.keys() and es_result["latestTradeShowStartTime"] is not None:
                latestTradeShowStartTime = es_result["latestTradeShowStartTime"]
            else:
                latestTradeShowStartTime = None
            if "latestTradeShowEndTime" in es_result.keys() and es_result["latestTradeShowEndTime"] is not None:
                latestTradeShowEndTime = es_result["latestTradeShowEndTime"]
            else:
                latestTradeShowEndTime = None
            if "latestTradeShowNameRaw" in es_result.keys() and es_result["latestTradeShowNameRaw"] is not None:
                latestTradeShowNameRaw = es_result["latestTradeShowNameRaw"]
            else:
                latestTradeShowNameRaw = None
            if "tradeShowCount" in es_result.keys() and es_result["tradeShowCount"] is not None:
                tradeShowCount = es_result["tradeShowCount"]
            else:
                tradeShowCount = 0
            if TradeShow_startDatesss != latestTradeShowStartTime:
                row_sum = install_files.read_sum() + 1
                install_files.install(row=row_sum, column=1, value=pid)
                install_files.install(row=row_sum, column=2, value='latestTradeShowStartTime')
                install_files.install(row=row_sum, column=3, value='开始时间不相等')
                install_files.install(row=row_sum, column=4, value=latestTradeShowStartTime)
            if TradeShow_endDatesss != latestTradeShowEndTime:
                row_sum = install_files.read_sum() + 1
                install_files.install(row=row_sum, column=1, value=pid)
                install_files.install(row=row_sum, column=2, value='latestTradeShowEndTime')
                install_files.install(row=row_sum, column=3, value='结束时间不相等')
                install_files.install(row=row_sum, column=4, value=latestTradeShowEndTime)
            if latestTradeShowNameRaw != TradeShow_namesss:
                row_sum = install_files.read_sum() + 1
                install_files.install(row=row_sum, column=1, value=pid)
                install_files.install(row=row_sum, column=2, value='latestTradeShowNameRaw')
                install_files.install(row=row_sum, column=3, value='展会名称不相等')
                install_files.install(row=row_sum, column=4, value=latestTradeShowNameRaw)
            if int(tradeShowCount) != int(totals):
                print()
                row_sum = install_files.read_sum() + 1
                install_files.install(row=row_sum, column=1, value=pid)
                install_files.install(row=row_sum, column=2, value='tradeShowCount')
                install_files.install(row=row_sum, column=3, value='展会数量不相等')
                install_files.install(row=row_sum, column=4, value=tradeShowCount)
            assert int(tradeShowCount) == int(totals)
            assert latestTradeShowNameRaw == TradeShow_namesss
            assert TradeShow_endDatesss == latestTradeShowEndTime
            assert TradeShow_startDatesss == latestTradeShowStartTime

    # 风险信息
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
            else:
                print('判断条件错误', cv_key)

    # 员工人脉
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

    # 企业发展-企业标签搜索
    @pytest.mark.parametrize('cv_key', [False, True])
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
        # header = {
        #     'app_token': "a14cc8b00f84e64b438af540390531e4",
        #     'authorization': "Token token=4e15695de0bfe2273795e707fd602d46",
        #     'content-type': 'application/json',
        #     'crm_platform_type': "lixiaoyun"
        # }
        time.sleep(2.2)
        pid_list = []
        pid_responst = search(HOST).advanced_search(cv=cv, page=10, pagesize=10).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append(pid['id'])
        else:
            print('搜索结果：', pid_responst, '\n搜索条件:', cv, '\n')
            assert pid_responst != []
        for i in pid_list:
            time.sleep(2.1)
            es_result = ES.get(index="company_info_prod", id=i)['_source']
            details_response = getCompanyBaseInfo(HOST).getEntSectionInfo(pid=i,
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
                    assert "adminLicense" not in es_result.keys() or es_result["adminLicense"] == [] or es_result[
                        "adminLicense"] is None
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
            'app_token': "a14cc8b00f84e64b438af540390531e4",
            'authorization': "Token token=4e15695de0bfe2273795e707fd602d46",
            'content-type': 'application/json',
            'crm_platform_type': "lixiaoyun"
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
            if es_result["adminLicense"] != [] and es_result["adminLicense"] is not None:
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
            assert "adminLicense" not in es_result.keys() or es_result["adminLicense"] == [] or es_result[
                "adminLicense"] is None
            assert details_response['data']['AdministrativeLicense']['total'] == 0
            assert details_response['data']['AdministrativeLicense']['items'] == []

# if __name__ == '__main__':
#     print(getCompanyBaseInfo(HOST).getEntSectionInfo_RiskInfo_subset(
#         pid='90c2f9836fe55b385f877f629bc59aee', subset='Executor').json())
