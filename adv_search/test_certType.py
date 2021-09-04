# -*- coding: utf-8 -*-
import pytest,openpyxl,time
from search_API import search_API

file = openpyxl.load_workbook('二级选项.xlsx')

sheet = file['涵盖证书类型']

certL1Type_list = []
for i in range(3, 40):
    if (sheet['C' + str(i)]).value != None:
        certL1Type_list.append(sheet['C' + str(i)].value)
certL2Type_list = []
for i in range(3, 40):
    if (sheet['E' + str(i)]).value != None:
        certL2Type_list.append(sheet['E' + str(i)].value)

current_time = int(time.time() * 1000)

class TestCertType():
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('level1',certL1Type_list)
    def test_firstCategory(self,cr,level1,ES):
        es_client=ES
        esCheck_field = 'certL1Type'

        time.sleep(3)
        data = search_API('certType', {'certL1Type': [f"{level1}"], 'certL2Type': []},cr)
        if len(data['items']) == 0:
            print('level1', level1)
        # assert len(data['items']) != 0
        # print(data)

        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 和ES对比
            es_result=es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错
            if cr=='IN':
                assert level1 in es_result[esCheck_field]
            else:
                if esCheck_field not in list(es_result.keys()):
                    pass
                else:
                    assert level1 not in es_result[esCheck_field]

    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('level2',certL2Type_list)
    def test_secondCategory(self,cr,level2,ES):
        es_client = ES
        esCheck_field='certL2Type'  #行业es上分1级2级两个字段，其他暂时不分

        time.sleep(3)
        data = search_API('certType', {'certL1Type': [], 'certL2Type': [f"{level2}"]},cr)
        if len(data['items']) == 0:
            print('level2', level2)
        # assert len(data['items']) != 0
        # print(data)

        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 和ES对比
            es_result=es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错
            if cr=='IN':
                assert level2 in es_result[esCheck_field]
            else:
                if esCheck_field not in list(es_result.keys()):
                    pass
                else:
                    assert level2 not in es_result[esCheck_field]

cert_key_list=['latest3MonthCertL2Type', 'latest6MonthCertL2Type']
class TestLatestNMonthCertL2Type():
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('level1',certL1Type_list)
    @pytest.mark.parametrize('cn',cert_key_list )
    def test_level1(self,cr,level1,cn,ES,date):
        es_client=ES
        result_time = [date('af', 3), date('af', 6)]

        time.sleep(3)
        data = search_API(cn, {'certL1Type': [f"{level1}"], 'certL2Type': []},cr)
        if len(data['items']) == 0:
            print('level1', level1)
        assert len(data['items']) != 0
        # print(data)

        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 和ES对比
            es_result=es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错
            es_key_list = []
            for es_key in es_result.keys():
                es_key_list.append(es_key)

            if cr == "IN":
                if 'certificate' not in es_key_list:
                    assert True == False  # 这是个必错的情况
                elif es_result['certificate'] == []:
                    assert True == False  # 这是个必错的情况
                flag = False
                for x in range(len(es_result['certificate'])):
                    if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
                        pass
                    elif int(level1) in es_result['certificate'][x]['type']  \
                            and es_result['certificate'][x]['endDate'] != None \
                            and current_time <= es_result['certificate'][x]['endDate'] <= result_time[
                        cert_key_list.index(cn)]:
                        flag = True
                        break
                assert flag == True

            else:
                if 'certificate' not in es_key_list:
                    assert True != False  # 这是个必对的情况
                elif es_result['certificate'] == []:
                    assert True != False  # 这是个必对的情况
                flag = False
                for x in range(len(es_result['certificate'])):
                    if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
                        pass
                    elif int(level1) in es_result['certificate'][x]['type'] \
                            and es_result['certificate'][x]['endDate'] != None \
                            and current_time <= es_result['certificate'][x]['endDate'] <= result_time[
                        cert_key_list.index(cn)]:
                        flag = True
                        break
                assert flag == False

    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('level2', certL2Type_list)
    @pytest.mark.parametrize('cn', cert_key_list)
    def test_level2(self, cr, level2, cn, ES, date):
        es_client = ES
        result_time = [date('af', 3), date('af', 6)]

        time.sleep(3)
        data = search_API(cn, {'certL1Type': [], 'certL2Type': [f"{level2}"]}, cr)
        if len(data['items']) == 0:
            print('level2', level2)
        assert len(data['items']) != 0
        # print(data)

        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 和ES对比
            es_result = es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错
            es_key_list = []
            for es_key in es_result.keys():
                es_key_list.append(es_key)

            if cr == "IN":
                if 'certificate' not in es_key_list:
                    assert True == False  # 这是个必错的情况
                elif es_result['certificate'] == []:
                    assert True == False  # 这是个必错的情况
                flag = False
                for x in range(len(es_result['certificate'])):
                    if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
                        pass
                    elif int(level2) in es_result['certificate'][x]['type']\
                            and es_result['certificate'][x]['endDate'] != None \
                            and current_time <= es_result['certificate'][x]['endDate'] <= result_time[
                        cert_key_list.index(cn)]:
                        flag = True
                        break
                assert flag == True

            else:
                if 'certificate' not in es_key_list:
                    assert True != False  # 这是个必对的情况
                elif es_result['certificate'] == []:
                    assert True != False  # 这是个必对的情况
                flag = False
                for x in range(len(es_result['certificate'])):
                    if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
                        pass
                    elif int(level2) in es_result['certificate'][x]['type']\
                            and es_result['certificate'][x]['endDate'] != None \
                            and current_time <= es_result['certificate'][x]['endDate'] <= result_time[
                        cert_key_list.index(cn)]:
                        flag = True
                        break
                assert flag == False
