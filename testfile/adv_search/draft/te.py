# -*- coding: utf-8 -*-
#资质证书类型
import pytest,openpyxl,time,sys
from adv_search.search_API import search_API

file = openpyxl.load_workbook('../涵盖证书类型.xlsx')
# sheet = file['涵盖证书类型']
# certL1Type_list = []
# for i in range(3, 40):
#     if (sheet['C' + str(i)]).value != None:
#         certL1Type_list.append(sheet['C' + str(i)].value)
# certL2Type_list = []
# for i in range(3, 40):
#     if (sheet['E' + str(i)]).value != None:
#         certL2Type_list.append(sheet['E' + str(i)].value)

# projectname = 'adv_search'
# file_path = f"{sys.argv[0].split(projectname)[0]}{projectname}/涵盖证书类型.xlsx"
# print(file_path)
# file = openpyxl.load_workbook(file_path)
sheet = file['涵盖证书类型']
sheet_name = ['A','B','C','D','E','F','G','H','I','J','K']
row_list = []
for i in sheet[1]:
    row_list.append(i.value)
index_type1 = row_list.index("certL1Type_value")
index_type2 = row_list.index("certL2Type_value")
certL1Type_sum = 1
certL1Type_list = []
for i in sheet[sheet_name[index_type1]]:
    if i.value is not None:
        indata_value1 = i.value
        indata_name1 = sheet[sheet_name[index_type1 - 1]][certL1Type_sum].value
        append_value = {'certL1Type_value' : indata_value1, 'certL1Type_name' : indata_name1}
        if i.value == sheet[str(sheet_name[index_type1])+str(1)].value:
            continue
        elif append_value not in certL1Type_list:
            certL1Type_list.append(append_value)
        # else:
        #     print(i,sheet[sheet_name[index_type1-1]][certL1Type_sum].value,i.value)
    certL1Type_sum += 1

print(certL1Type_list)
certL2Type_sum = 1
certL2Type_list = []
for i in sheet[sheet_name[index_type2]]:
    if i.value is not None:
        indata_value2 = i.value
        indata_name2 = sheet[sheet_name[index_type2 - 1]][certL2Type_sum].value
        append_value = (indata_value2, indata_name2)
        if i.value == sheet[str(sheet_name[index_type2])+str(1)].value:
            continue
        elif append_value not in certL2Type_list:
            certL2Type_list.append(append_value)
        else:
            print(i, sheet[sheet_name[index_type2 - 1]][certL2Type_sum].value, i.value)
    certL2Type_sum += 1
print(certL2Type_list)
# current_time = int(time.time() * 1000)
#
# class TestCertType():
#     @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
#     @pytest.mark.parametrize('indata_value1,indata_name1',certL1Type_list)
#     def test_firstCategory(self,cr,indata_value1,indata_name1,ES):
#         es_client=ES
#         esCheck_field = 'certL1Type'
#
#         time.sleep(3)
#         data = search_API('certType', {'certL1Type': [f"{indata_value1}"], 'certL2Type': []},cr)
#         print(data)
#         if len(data['items']) == 0:
#             print('indata_value1', indata_value1)
#         # assert len(data['items']) != 0
#         # print(data)
#
#         for i in range(len(data['items'])):
#             pid = data['items'][i]['id']
#             companyName = data['items'][i]['companyName']
#             print(pid)
#             print(companyName)
#
#             # 和ES对比
#             es_result=es_client.get(index="company_info_prod", id=pid)['_source']
#             # 返回es中所有的键，去除 无该字段时的报错
#             if cr=='IN':
#                 assert int(indata_value1) in es_result[esCheck_field]
#             else:
#                 if esCheck_field not in list(es_result.keys()):
#                     pass
#                 else:
#                     assert int(indata_value1) not in es_result[esCheck_field]
#
#     @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
#     @pytest.mark.parametrize('indata_value2,indata_name2',certL2Type_list)
#     def test_secondCategory(self,cr,indata_value2,indata_name2,ES):
#         es_client = ES
#         esCheck_field='certL2Type'  #行业es上分1级2级两个字段，其他暂时不分
#
#         time.sleep(3)
#         data = search_API('certType', {'certL1Type': [], 'certL2Type': [f"{indata_value2}"]},cr)
#         if len(data['items']) == 0:
#             print('indata_value2', indata_value2)
#         # assert len(data['items']) != 0
#         # print(data)
#
#         for i in range(len(data['items'])):
#             pid = data['items'][i]['id']
#             companyName = data['items'][i]['companyName']
#             print(pid)
#             print(companyName)
#
#             # 和ES对比
#             es_result=es_client.get(index="company_info_prod", id=pid)['_source']
#             # 返回es中所有的键，去除 无该字段时的报错
#             if cr=='IN':
#                 assert int(indata_value2) in es_result[esCheck_field]
#             else:
#                 if esCheck_field not in list(es_result.keys()):
#                     pass
#                 else:
#                     assert int(indata_value2) not in es_result[esCheck_field]
#
# cert_key_list=['latest3MonthCertL2Type', 'latest6MonthCertL2Type']
# class TestLatestNMonthCertL2Type():
#     @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
#     @pytest.mark.parametrize('indata_value1,indata_name1',certL1Type_list)
#     @pytest.mark.parametrize('cn',cert_key_list )
#     def test_indata_value1(self,cr,indata_value1,indata_name1,cn,ES,date):
#         es_client=ES
#         result_time = [date('af', 3), date('af', 6)]
#
#         time.sleep(3)
#         data = search_API(cn, {'certL1Type': [f"{indata_value1}"], 'certL2Type': []},cr)
#         if len(data['items']) == 0:
#             print('indata_value1', indata_value1)
#         assert len(data['items']) != 0
#         # print(data)
#
#         for i in range(len(data['items'])):
#             pid = data['items'][i]['id']
#             companyName = data['items'][i]['companyName']
#             print(pid)
#             print(companyName)
#
#             # 和ES对比
#             es_result=es_client.get(index="company_info_prod", id=pid)['_source']
#             # 返回es中所有的键，去除 无该字段时的报错
#             es_key_list = []
#             for es_key in es_result.keys():
#                 es_key_list.append(es_key)
#
#             if cr == "IN":
#                 if 'certificate' not in es_key_list:
#                     assert True == False  # 这是个必错的情况
#                 elif es_result['certificate'] == []:
#                     assert True == False  # 这是个必错的情况
#                 flag = False
#                 for x in range(len(es_result['certificate'])):
#                     if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
#                         pass
#                     elif int(indata_value1) in es_result['certificate'][x]['type']  \
#                             and es_result['certificate'][x]['endDate'] != None \
#                             and current_time <= es_result['certificate'][x]['endDate'] <= result_time[
#                         cert_key_list.index(cn)]:
#                         flag = True
#                         break
#                 assert flag == True
#
#             else:
#                 if 'certificate' not in es_key_list:
#                     assert True != False  # 这是个必对的情况
#                 elif es_result['certificate'] == []:
#                     assert True != False  # 这是个必对的情况
#                 flag = False
#                 for x in range(len(es_result['certificate'])):
#                     if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
#                         pass
#                     elif int(indata_value1) in es_result['certificate'][x]['type'] \
#                             and es_result['certificate'][x]['endDate'] != None \
#                             and current_time <= es_result['certificate'][x]['endDate'] <= result_time[
#                         cert_key_list.index(cn)]:
#                         flag = True
#                         break
#                 assert flag == False
#
#     @pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
#     @pytest.mark.parametrize('indata_value2,indata_name2', certL2Type_list)
#     @pytest.mark.parametrize('cn', cert_key_list)
#     def test_indata_value2(self, cr, indata_value2,indata_name2, cn, ES, date):
#         es_client = ES
#         result_time = [date('af', 3), date('af', 6)]
#
#         time.sleep(3)
#         data = search_API(cn, {'certL1Type': [], 'certL2Type': [f"{indata_value2}"]}, cr)
#         if len(data['items']) == 0:
#             print('indata_value2', indata_value2)
#         assert len(data['items']) != 0
#         # print(data)
#
#         for i in range(len(data['items'])):
#             pid = data['items'][i]['id']
#             companyName = data['items'][i]['companyName']
#             print(pid)
#             print(companyName)
#
#             # 和ES对比
#             es_result = es_client.get(index="company_info_prod", id=pid)['_source']
#             # 返回es中所有的键，去除 无该字段时的报错
#             es_key_list = []
#             for es_key in es_result.keys():
#                 es_key_list.append(es_key)
#
#             if cr == "IN":
#                 if 'certificate' not in es_key_list:
#                     assert True == False  # 这是个必错的情况
#                 elif es_result['certificate'] == []:
#                     assert True == False  # 这是个必错的情况
#                 flag = False
#                 for x in range(len(es_result['certificate'])):
#                     if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
#                         pass
#                     elif int(indata_value2) in es_result['certificate'][x]['type']\
#                             and es_result['certificate'][x]['endDate'] != None \
#                             and current_time <= es_result['certificate'][x]['endDate'] <= result_time[
#                         cert_key_list.index(cn)]:
#                         flag = True
#                         break
#                 assert flag == True
#
#             else:
#                 if 'certificate' not in es_key_list:
#                     assert True != False  # 这是个必对的情况
#                 elif es_result['certificate'] == []:
#                     assert True != False  # 这是个必对的情况
#                 flag = False
#                 for x in range(len(es_result['certificate'])):
#                     if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
#                         pass
#                     elif int(indata_value2) in es_result['certificate'][x]['type']\
#                             and es_result['certificate'][x]['endDate'] != None \
#                             and current_time <= es_result['certificate'][x]['endDate'] <= result_time[
#                         cert_key_list.index(cn)]:
#                         flag = True
#                         break
#                 assert flag == False
