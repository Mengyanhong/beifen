# -*- coding: utf-8 -*-
#资质证书类型
import pytest,openpyxl,time,sys,random,datetime
from Configs.search_API import search
from Configs.search_API import getCompanyBaseInfo
host = 'test'
getCompanyBaseInfo = getCompanyBaseInfo(host)
search = search(host)

file = openpyxl.load_workbook('..\data\Excel\涵盖证书类型.xlsx')
sheet = file['涵盖证书类型']
sheet_name = ['A','B','C','D','E','F','G','H','I','J','K']
row_list = [] #创建case标题列表
for i in sheet[1]: #获取case列表标题
    row_list.append(i.value)
index_type1 = row_list.index("certL1Type_value") #获取用例索引
index_type2 = row_list.index("certL2Type_value") #获取用例索引
# certL1Type_sum = 0
certL1Type_list = [] #创建certL1Type_value用例列表
for i in sheet[sheet_name[index_type1]]: #通过用例索引获取全部用例
    if i.value is not None: #判断用例不为空
        if i.value == sheet[str(sheet_name[index_type1])+str(1)].value: #跳过第一行标题
            continue
        elif i.value not in certL1Type_list: #判断重复case若case重复则不录入case列表
            certL1Type_list.append(i.value) #若case不重复则添加到case列表

certL2Type_sum = 0
certL2Type_list = []  #创建certL2Type_value用例列表
for i in sheet[sheet_name[index_type2]]: #通过用例索引获取全部用例
    if i.value is not None: #判断用例不为空
        if i.value == sheet[str(sheet_name[index_type2])+str(1)].value: #跳过第一行标题
            continue
        elif i.value not in certL2Type_list: #判断重复case若case重复则不录入case列表
            certL2Type_list.append(i.value) #若case不重复则添加到case列表
        else:
            print(i, sheet[sheet_name[index_type2 - 1]][certL2Type_sum].value, i.value)
            certL2Type_sum += 1

current_time = int(time.time() * 1000) #获取当前时间
class TestCertType():
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('level1',certL1Type_list)
    def test_firstCategory(self,cr,level1,ES):
        es_client=ES
        esCheck_field = 'certL1Type'
        data = search.search_API('certType', {'certL1Type': [f"{level1}"], 'certL2Type': []},cr)
        if data != None:
            if len(data['items']) == 0:
                print('level1', level1)
                assert len(data['items']) != 0
        else:
            assert data != None
        time.sleep(2.5)
        for i in [random.randint(0, len(data['items'])-1) for i in range(20)]:
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)
            # 和ES对比
            es_result=es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错
            if cr=='IN':
                assert int(level1) in es_result[esCheck_field]
            else:
                if esCheck_field not in list(es_result.keys()):
                    pass
                else:
                    assert int(level1) not in es_result[esCheck_field]

    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('level2',certL2Type_list)
    def test_secondCategory(self,cr,level2,ES):
        es_client = ES
        esCheck_field='certL2Type'  #行业es上分1级2级两个字段，其他暂时不分
        data = search.search_API('certType', {'certL1Type': [], 'certL2Type': [f"{level2}"]},cr)
        if len(data['items']) == 0:
            print('level2', level2)
        time.sleep(2.5)
        assert len(data['items']) != 0
        # print(data)
        for i in [random.randint(0, len(data['items'])-1) for i in range(20)]:
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)
            # 和ES对比
            es_result=es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错
            if cr=='IN':
                assert int(level2) in es_result[esCheck_field]
            else:
                if esCheck_field not in list(es_result.keys()):
                    pass
                else:
                    assert int(level2) not in es_result[esCheck_field]

cert_key_list=['latest3MonthCertL2Type', 'latest6MonthCertL2Type']
class TestLatestNMonthCertL2Type():
    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('level1',certL1Type_list)
    @pytest.mark.parametrize('cn',cert_key_list )
    def test_level1(self,cr,level1,cn,ES,date):
        es_client=ES
        result_time = [date('af', 3), date('af', 6)]
        data = search.search_API(cn, {'certL1Type': [f"{level1}"], 'certL2Type': []},cr)
        if len(data['items']) == 0:
            print('level1', level1)
        time.sleep(2.5)
        assert len(data['items']) != 0
        # print(data)
        for i in [random.randint(0, len(data['items'])-1) for i in range(20)]:
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
                    elif int(level1) in es_result['certificate'][x]['type'] and es_result['certificate'][x]['endDate'] != None:
                        if str(type(es_result['certificate'][x]['endDate'])) == "<class 'int'>":
                            print(es_result['certificate'][x]['endDate'],'shijianchuo')
                            if current_time <= es_result['certificate'][x]['endDate'] <= result_time[cert_key_list.index(cn)]:
                                flag = True
                                break
                        else:
                            start = es_result['certificate'][x]['endDate'].split('+')[0]
                            current = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f')
                            timeStamp = int(time.mktime(current.timetuple()) * 1000)
                            if current_time <= timeStamp <= result_time[cert_key_list.index(cn)]:
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
                            and es_result['certificate'][x]['endDate'] != None :
                        if str(type(es_result['certificate'][x]['endDate'])) == "<class 'int'>":
                            if current_time <= es_result['certificate'][x]['endDate'] <= result_time[cert_key_list.index(cn)]:
                                flag = True
                                break
                        else:
                            start = es_result['certificate'][x]['endDate'].split('+')[0]
                            current = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f')
                            timeStamp = int(time.mktime(current.timetuple()) * 1000)
                            if current_time <= timeStamp <= result_time[cert_key_list.index(cn)]:
                                flag = True
                                break
                assert flag == False

    @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
    @pytest.mark.parametrize('level2', certL2Type_list)
    @pytest.mark.parametrize('cn', cert_key_list)
    def test_level2(self, cr, level2, cn, ES, date):
        es_client = ES
        result_time = [date('af', 3), date('af', 6)]
        data = search.search_API(cn, {'certL1Type': [], 'certL2Type': [f"{level2}"]}, cr)
        if len(data['items']) == 0:
            print('level2', level2)
        time.sleep(2.5)
        assert len(data['items']) != 0
        # print(data)
        for i in [random.randint(0, len(data['items'])-1) for i in range(20)]:
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
                    elif int(level2) in es_result['certificate'][x]['type'] \
                            and es_result['certificate'][x]['endDate'] != None:
                        if str(type(es_result['certificate'][x]['endDate'])) == "<class 'int'>":
                            if current_time <= es_result['certificate'][x]['endDate'] <= result_time[
                                cert_key_list.index(cn)]:
                                flag = True
                                break
                        else:
                            start = es_result['certificate'][x]['endDate'].split('+')[0]
                            current = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f')
                            timeStamp = int(time.mktime(current.timetuple()) * 1000)
                            if current_time <= timeStamp <= result_time[cert_key_list.index(cn)]:
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
                    elif int(level2) in es_result['certificate'][x]['type'] and es_result['certificate'][x]['endDate'] != None:
                        if str(type(es_result['certificate'][x]['endDate'])) == "<class 'int'>":
                            if current_time <= es_result['certificate'][x]['endDate'] <= result_time[
                                cert_key_list.index(cn)]:
                                flag = True
                                break
                        else:
                            start = es_result['certificate'][x]['endDate'].split('+')[0]
                            current = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%f')
                            timeStamp = int(time.mktime(current.timetuple()) * 1000)
                            if current_time <= timeStamp <= result_time[cert_key_list.index(cn)]:
                                flag = True
                                break
                assert flag == False
