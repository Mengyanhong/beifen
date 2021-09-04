# -*- coding: utf-8 -*-
import openpyxl
import yaml,pytest,time
from ..adv_search.search_API import search_API

with open('multiSelect.yaml') as f:
    yaml_data = yaml.safe_load(f)

# file = openpyxl.load_workbook('来源站点.xlsx')
# sheet = file['来源']
# source_list = []
# for i in range(192,222):
#     source_list.append(str(sheet['H' + str(i)].value))
# yaml_data['contactSource']=source_list   #list-int
# yaml_data['mobileSource']=source_list
# yaml_data['fixedSource']=source_list

key_list = list(yaml_data.keys())

class TestMultiSelect:
    @pytest.mark.parametrize('cr',["IN","NOT_IN"])
    # @pytest.mark.parametrize('cr',["IN"])

    @pytest.mark.parametrize('key',key_list)
    def test_multiSelect(self,key,cr,ES,date):
        es_client = ES
        current_time = int(time.time() * 1000)
        # cert_key_list = ['latest3MonthCertL2Type', 'latest6MonthCertL2Type']
        result_time = [date('af', 3), date('af', 6)]

        special_key=['entAlter.alterCategory']

        for value in yaml_data[key]:
            time.sleep(3)
            data = search_API(key, [value], cr)
            print(key, value, cr)
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

                if cr=="IN":
                    if key not in es_key_list and key not in special_key:
                    # if key not in cert_key_list and key not in es_key_list and key not in special_key:
                        assert True == False  # 这是个必错的情况
                    else:
                        if key in ['entStatus','entTypeDetail','recruitAvgFrequency']:
                            assert int(value)== es_result[key]
                        elif key in ['lastCap']:
                            assert value in es_result[key]

                        # elif key in cert_key_list:
                        #     if 'certificate' not in es_key_list:
                        #         assert True == False  # 这是个必错的情况
                        #     elif es_result['certificate'] == []:
                        #         assert True == False  # 这是个必错的情况
                        #     flag = False
                        #     for x in range(len(es_result['certificate'])):
                        #         if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
                        #             pass
                        #         elif es_result['certificate'][x]['type']== int(value)\
                        #                 and es_result['certificate'][x]['endDate'] != None \
                        #                 and current_time <= es_result['certificate'][x]['endDate'] <= result_time[cert_key_list.index(key)]:
                        #             flag = True
                        #             break
                        #     assert flag == True

                        elif key in special_key:
                            if 'entAlter' not in es_key_list:
                                assert True == False  # 这是个必错的情况
                            elif es_result['entAlter'] == []:
                                assert True == False  # 这是个必错的情况
                            flag = False
                            for x in range(len(es_result['entAlter'])):
                                if es_result['entAlter'][x]['alterCategory']== int(value):
                                    flag = True
                                    break
                            assert flag == True
                        else:
                            assert int(value) in es_result[key]

                else:
                    if key not in es_key_list:
                    # if key not in cert_key_list and key not in es_key_list:
                        assert True != False  # 这是个必对的情况
                    elif es_result[key]==None:
                    # elif key not in cert_key_list and es_result[key] == None:
                        pass
                    else:
                        if key in ['entStatus','entTypeDetail','recruitAvgFrequency']:
                            assert int(value)!= es_result[key]
                        elif key in ['lastCap']:
                            assert value not in es_result[key]

                        # elif key in cert_key_list:
                        #     if 'certificate' not in es_key_list:
                        #         assert True != False  # 这是个必对的情况
                        #     elif es_result['certificate'] == []:
                        #         assert True != False  # 这是个必对的情况
                        #     flag = False
                        #     for x in range(len(es_result['certificate'])):
                        #         if 'type' and 'endDate' not in list(es_result['certificate'][x].keys()):
                        #             pass
                        #         elif es_result['certificate'][x]['type']== int(value)\
                        #                 and es_result['certificate'][x]['endDate'] != None \
                        #                 and current_time <= es_result['certificate'][x]['endDate'] <= result_time[cert_key_list.index(key)]:
                        #             flag = True
                        #             break
                        #     assert flag == False
                        else:
                            assert int(value) not in es_result[key]
