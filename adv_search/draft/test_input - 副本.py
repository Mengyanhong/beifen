# -*- coding: utf-8 -*-
import pytest,yaml,time
from search_API import search_API

with open('../input.yaml') as f:
    yaml_data=yaml.safe_load(f)
    key_list=list(yaml_data.keys())

@pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
@pytest.mark.parametrize('key', key_list)
class Testinput:
    def test_input(self,key,cr,ES,date):
        es_client = ES
        current_time = int(time.time() * 1000)

        #special_key_list 判断时间的字段不同，要把同一种数据放一起，如 招聘，sem； 把同一统计时间的放在一起，如前6个月（招聘默认前6个月）
        special_key_list = ['latest6MonthJobName', 'recruitment.jobDetail','recruitment.entWelfare','recruitment.jobName',
                            'latest3MonthJobName','latest1MonthJobName',
                            'latest1MonthSemKeyword','certificate.certOrgName']    #前端传参
        special_value_list=['recruitment.jobName','recruitment.jobDetail','recruitment.entWelfare','recruitment.jobName',
                            'latest3MonthJobName','latest1MonthJobName',
                            'semPromo.keyword','certificate.certOrgName' ]   #以上传参对应的es 字段
        result_time = [date('bef', 6), date('bef', 1),date('bef',3)]

        for value in yaml_data[key]:
            data = search_API(key, value, cr)
            print(key, value, cr)
            assert len(data['items']) != 0
            print(data)

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
                    if key not in special_key_list and key not in es_key_list:
                        assert True == False  # 这是个必错的情况
                    else:
                        if key=='entName':# 需判断是否是历史名称匹配
                            if value in es_result[key]:
                                assert True != False  # 这是个必对的情况
                            else:
                                for x in range(len(es_result['historyName'])):
                                    if value in es_result['historyName'][x]:
                                        assert True != False  # 这是个必对的情况
                                        break
                                    else:
                                        assert True == False  # 这是个必错的情况

                        elif key in ['entName','opScope','contactAddress','abnormalInReason']:
                            # 非list 的添加到这里
                            assert value in es_result[key]

                        elif key in special_key_list:
                            # 嵌套格式的添加到这里
                            key_index=special_key_list.index(key)  #key 在special_key_list和special_key_list中的索引
                            key_first_name=special_value_list[key_index].split('.')[0]
                            key_second_name=special_value_list[key_index].split('.')[1] #字典的一级key名
                            if key_first_name not in es_key_list:
                                assert True == False  # 这是个必错的情况
                            elif es_result[key_first_name] == []:
                                assert True == False  # 这是个必错的情况

                            else:
                                flag = False
                                if key in special_key_list[:6]: #招聘字段
                                    for x in range(len(es_result[key_first_name])):
                                        if key_second_name and 'releaseDate' not in list(es_result[key_first_name][x]):
                                            pass
                                        elif es_result[key_first_name][x][key_second_name]==None or es_result[key_first_name][x]['releaseDate']==None:
                                            pass
                                        # 前6个月
                                        elif key in special_key_list[:4] and value in es_result[key_first_name][x][key_second_name]\
                                            and result_time[0] <=es_result[key_first_name][x]['releaseDate'] <=current_time :
                                            flag = True
                                            break
                                        # 前3个月
                                        elif key in special_key_list[4:5] and value in es_result[key_first_name][x][key_second_name]\
                                            and result_time[2] <=es_result[key_first_name][x]['releaseDate'] <=current_time :
                                            flag = True
                                            break
                                        # 前1个月
                                        elif key in special_key_list[5:6] and value in es_result[key_first_name][x][key_second_name]\
                                            and result_time[1] <=es_result[key_first_name][x]['releaseDate'] <=current_time :
                                            flag = True
                                            break
                                    assert flag == True

                                elif key=='latest1MonthSemKeyword':  #sem字段
                                    for x in range(len(es_result[key_first_name])):
                                        if key_second_name and 'semDate' not in list(es_result[key_first_name][x]):
                                            pass
                                        elif es_result[key_first_name][x][key_second_name]==None or es_result[key_first_name][x]['semDate']==None:
                                            pass
                                        elif value in es_result[key_first_name][x][key_second_name] \
                                                and result_time[1] <= es_result[key_first_name][x]['semDate'] <=current_time:
                                            flag = True
                                            break
                                    assert flag == True

                                else:
                                    for x in range(len(es_result[key_first_name])):
                                        if key_second_name not in list(es_result[key_first_name][x]):
                                            pass
                                        elif es_result[key_first_name][x][key_second_name]==None:
                                            pass
                                        elif value in es_result[key_first_name][x][key_second_name]:
                                            flag = True
                                            break
                                    assert flag == True

                        else:
                            #普通list的
                            flag = False
                            for x in range(len(es_result[key])):
                                if value in es_result[key][x]:
                                    flag = True
                                    break
                            assert flag == True

                else:
                    if key == 'entName':  # 需判断是否是历史名称匹配
                        if value in es_result[key]:
                            assert True == False  # 这是个必错的情况
                        else:
                            for x in range(len(es_result['historyName'])):
                                if value in es_result['historyName'][x]:
                                    assert True == False  # 这是个必错的情况
                                    break
                                else:
                                    assert True != False  # 这是个必对的情况

                    elif key not in special_key_list and key not in es_key_list:
                        assert True != False  # 这是个必对的情况
                    else:
                        if key in ['entName', 'opScope', 'contactAddress', 'abnormalInReason']:
                        # 非list 的添加到这里
                            assert value not in es_result[key]
                        elif key in special_key_list:
                        #嵌套格式的添加到这里
                            key_index = special_key_list.index(key)  # key 在special_key_list和special_key_list中的索引
                            key_first_name = special_value_list[key_index].split('.')[0]
                            key_second_name = special_value_list[key_index].split('.')[1]  # 字典的一级key名
                            if key_first_name not in es_key_list:
                                assert True != False  # 这是个必对的情况
                            elif es_result[key_first_name] == []:
                                assert True != False  # 这是个必对的情况

                            else:
                                flag = False
                                if key in special_key_list[:6]:  #招聘字段
                                    for x in range(len(es_result[key_first_name])):
                                        if key_second_name and 'releaseDate' not in list(es_result[key_first_name][x]):
                                            pass
                                        elif es_result[key_first_name][x][key_second_name]==None or es_result[key_first_name][x]['releaseDate']==None:
                                            pass
                                        #前6个月
                                        elif key in special_key_list[:4] and value in es_result[key_first_name][x][key_second_name] \
                                                and result_time[0]<= es_result[key_first_name][x]['releaseDate'] <=current_time:
                                            flag = True
                                            break
                                        # 前3个月
                                        elif key in special_key_list[4:5] and value in es_result[key_first_name][x][key_second_name] \
                                                and result_time[2]<= es_result[key_first_name][x]['releaseDate'] <=current_time:
                                            flag = True
                                            break
                                        # 前1个月
                                        elif key in special_key_list[5:6] and value in es_result[key_first_name][x][key_second_name] \
                                                and result_time[1]<= es_result[key_first_name][x]['releaseDate'] <=current_time:
                                            flag = True
                                            break
                                    assert flag == False

                                elif key == 'latest1MonthSemKeyword':  #sem字段
                                    for x in range(len(es_result[key_first_name])):
                                        if key_second_name and 'semDate' not in list(es_result[key_first_name][x]):
                                            pass
                                        elif es_result[key_first_name][x][key_second_name]==None or es_result[key_first_name][x]['semDate']==None:
                                            pass
                                        elif value in es_result[key_first_name][x][key_second_name] \
                                                and  result_time[1]<= es_result[key_first_name][x]['semDate'] <=current_time:
                                            flag = True
                                            break
                                    assert flag == False

                                else:
                                    for x in range(len(es_result[key_first_name])):
                                        if key_second_name not in list(es_result[key_first_name][x]):
                                            pass
                                        elif es_result[key_first_name][x][key_second_name] == None:
                                            pass
                                        elif value in es_result[key_first_name][x][key_second_name]:
                                            flag = True
                                            break
                                    assert flag == False

                        else:
                            #普通list的
                            flag = False
                            for x in range(len(es_result[key])):
                                if value in es_result[key][x]:
                                    flag = True
                                    break
                            assert flag == False



