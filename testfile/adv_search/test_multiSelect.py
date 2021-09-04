# -*- coding: utf-8 -*-
# 多选下拉框
import openpyxl
import yaml,pytest,time,random,requests
from adv_search.search_API import search
from adv_search.search_API import getCompanyBaseInfo
host = 'staging'
getCompanyBaseInfo = getCompanyBaseInfo(host)
search = search(host)
with open('multiSelect.yaml') as f:
    yaml_data = yaml.safe_load(f)
    f.close()

key_list_SearchCondition = list(yaml_data.keys())
data_list = []
for i in range(len(key_list_SearchCondition)):
        if key_list_SearchCondition[i] == "SearchCondition_techTypeCompany":
            for label_value in yaml_data[key_list_SearchCondition[i]]["cv"]["options"]:
                data_list.append((yaml_data[key_list_SearchCondition[i]]["name"], label_value["value"], label_value["label"],key_list_SearchCondition[i]))
        else:
            for value in yaml_data[key_list_SearchCondition[i]]:
                data_list.append((key_list_SearchCondition[i],value,None,None))
class TestMultiSelect:
    @pytest.mark.parametrize('cr',["IN","NOT_IN"])
    @pytest.mark.parametrize('key_list,key,key_name,key_list_SearchCondition', data_list)
    def test_multiSelect(self,key_list,key,key_name,key_list_SearchCondition,cr,ES,date):
        es_client = ES
        # current_time = int(time.time() * 1000)
        # cert_key_list_list = ['latest3MonthCertL2Type', 'latest6MonthCertL2Type']
        # result_time = [date('af', 3), date('af', 6)]
        special_key_list=['entAlter.alterCategory']
        data = search.search_API(key_list, [key], cr)
        time.sleep(2.5)
        print(key_list, key, cr)
        assert len(data['items']) != 0

        for i in [random.randint(0, len(data['items'])-1) for i in range(20)]:
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            # 和ES对比
            es_result = es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错
            es_key_list_list = []
            for es_key_list in es_result.keys():
                es_key_list_list.append(es_key_list)
            #对比详情页标签
            re_tag_list = []
            if key_list_SearchCondition == "SearchCondition_techTypeCompany" and i%5 == 0:
                re_tag = getCompanyBaseInfo.getCompanyBase(pid).json()["data"]["tags"]
                print(re_tag)
                for i in re_tag:
                    # if 'tag_name' in i:
                    #     re_tag_list.append(i['tag_name'])
                    if 'tagName' in i:
                        re_tag_list.append(i["tagName"])
                time.sleep(2.5)
            if cr=="IN":
                if key_list not in es_key_list_list and key_list not in special_key_list:
                # if key_list not in cert_key_list_list and key_list not in es_key_list_list and key_list not in special_key_list:
                    assert True == False  # 这是个必错的情况
                else:
                    if key_list in ['entStatus','entTypeDetail','recruitAvgFrequency']:
                        assert int(key) == es_result[key_list]
                    elif key_list in ['lastCap']:
                        assert int(key) in es_result[key_list]
                    # elif key_list in cert_key_list_list:
                    #     if 'certificate' not in es_key_list_list:
                    #         assert True == False  # 这是个必错的情况
                    #     elif es_result['certificate'] == []:
                    #         assert True == False  # 这是个必错的情况
                    #     flag = False
                    #     for x in range(len(es_result['certificate'])):
                    #         if 'type' and 'endDate' not in list(es_result['certificate'][x].keys():
                    #             pass
                    #         elif es_result['certificate'][x]['type']== int(key)\
                    #                 and es_result['certificate'][x]['endDate'] != None \
                    #                 and current_time <= es_result['certificate'][x]['endDate'] <= result_time[cert_key_list_list.index(key_list)]:
                    #             flag = True
                    #             break
                    #     assert flag == True
                    elif key_list in special_key_list:
                        if 'entAlter' not in es_key_list_list:
                            assert True == False  # 这是个必错的情况
                        elif es_result['entAlter'] == []:
                            assert True == False  # 这是个必错的情况
                        flag = False
                        for x in range(len(es_result['entAlter'])):
                            if es_result['entAlter'][x]['alterCategory']== int(key):
                                flag = True
                                break
                        assert flag == True
                    else:
                        try:
                            print(pid)
                            print(companyName)
                            assert int(key) in es_result[key_list]
                        except TypeError:
                            print(pid)
                            print(companyName)
                            assert int(key) == es_result[key_list]
                if re_tag_list:
                    print(re_tag_list)
                    print(pid)
                    print(companyName)
                    print(key_name)
                    assert key_name in re_tag_list
            else:
                if key_list not in es_key_list_list:
                # if key_list not in cert_key_list_list and key_list not in es_key_list_list:
                    assert True != False  # 这是个必对的情况
                elif es_result[key_list]==None:
                # elif key_list not in cert_key_list_list and es_result[key_list] == None:
                    pass
                else:
                    if key_list in ['entStatus','entTypeDetail','recruitAvgFrequency']:
                        assert int(key)!= es_result[key_list]
                    elif key_list in ['lastCap']:
                        assert key not in es_result[key_list]
                    # elif key_list in cert_key_list_list:
                    #     if 'certificate' not in es_key_list_list:
                    #         assert True != False  # 这是个必对的情况
                    #     elif es_result['certificate'] == []:
                    #         assert True != False  # 这是个必对的情况
                    #     flag = False
                    #     for x in range(len(es_result['certificate'])):
                    #         if 'type' and 'endDate' not in list(es_result['certificate'][x].keys():
                    #             pass
                    #         elif es_result['certificate'][x]['type']== int(key)\
                    #                 and es_result['certificate'][x]['endDate'] != None \
                    #                 and current_time <= es_result['certificate'][x]['endDate'] <= result_time[cert_key_list_list.index(key_list)]:
                    #             flag = True
                    #             break
                    #     assert flag == False
                    else:
                        try:
                            print(pid)
                            print(companyName)
                            print(key_name)
                            assert int(key) not in es_result[key_list]
                        except TypeError:
                            print(pid)
                            print(companyName)
                            print(key_name)
                            assert int(key) != int(es_result[key_list])
                if re_tag_list:
                    print(re_tag_list)
                    print(pid)
                    print(companyName)
                    print(key_name,'NOT_IN')
                    assert key_name not in re_tag_list
