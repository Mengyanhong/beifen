# -*- coding: utf-8 -*-
import pytest,yaml,time
from ...adv_search.search_API import search_API

with open('input.yaml') as f:
    yaml_data=yaml.safe_load(f)
    key_list=list(yaml_data.keys())

@pytest.mark.parametrize('cr', ['IN', 'NOT_IN'])
@pytest.mark.parametrize('key', key_list)
class Testinput:
    def test_input(self,key,cr,ES,date):
        es_client = ES
        current_time = int(time.time() * 1000)

        # 涉及到时间的字段 及其对应嵌套字段
        sepcial_key=['latest6MonthJobName', 'latest3MonthJobName', 'latest1MonthJobName', 'latest1MonthSemKeyword']
        sepcial_value=[['recruitmennt','jobName','releaseDate'],['recruitmennt','jobName','releaseDate'],['recruitmennt','jobName','releaseDate'],
                       ['semPromo','keyword','semDate']]

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
                    if (key not in sepcial_key) or (key not in es_key_list) or ('.' not in key):
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

                        elif '.' in key:
                            # key中包含 .
                            if key.split(',')[0] not in es_key_list:
                                assert True == False  # 这是个必错的情况
                            elif es_result[key.split(',')[0]] == []:
                                assert True == False  # 这是个必错的情况
                            else:
                                flag = False
                                for field in es_result[key.split(',')[0]]:
                                    if value in field[key.split(',')[1]]:
                                        flag=True
                                        break
                                assert flag==True

                        elif key in sepcial_key:
                            for str in key: #取出字段中的数字
                                if isinstance(str,int) :
                                    num=str
                            search_time=date('bef',num)

                            index=sepcial_key.index(key)
                            if sepcial_value[index][0] not in es_key_list:
                                assert True == False  # 这是个必错的情况
                            elif sepcial_value[index][0] == []:
                                assert True == False  # 这是个必错的情况
                            else:
                                flag = False
                                for field in sepcial_value[index][0]:
                                    if sepcial_value[index][1] and sepcial_value[index][2] not in field:
                                        pass
                                    elif sepcial_value[index][1] == None or sepcial_value[index][2] == None:
                                        pass
                                    elif value in sepcial_value[index][1] and search_time<=sepcial_value[index][2]<=current_time:
                                        flag=True
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
                    if key not in sepcial_key and key not in es_key_list and '.' not in key:
                        pass
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

                        elif key in ['entName', 'opScope', 'contactAddress', 'abnormalInReason']:
                            # 非list 的添加到这里
                            assert value not in es_result[key]

                        elif '.' in key:
                            # key中包含 .
                            if key.split(',')[0] not in es_key_list:
                                pass
                            elif es_result[key.split(',')[0]] == []:
                                pass
                            else:
                                flag = False
                                for field in es_result[key.split(',')[0]]:
                                    if value in field[key.split(',')[1]]:
                                        flag=True
                                        break
                                assert flag==False

                        elif key in sepcial_key:
                            for str in key: #取出字段中的数字
                                if isinstance(str,int) :
                                    num=str
                            search_time=date('bef',num)

                            index=sepcial_key.index(key)
                            if sepcial_value[index][0] not in es_key_list:
                                pass
                            elif sepcial_value[index][0] == []:
                                pass
                            else:
                                flag = False
                                for field in sepcial_value[index][0]:
                                    if sepcial_value[index][1] and sepcial_value[index][2] not in field:
                                        pass
                                    elif sepcial_value[index][1] == None or sepcial_value[index][2] == None:
                                        pass
                                    elif value in sepcial_value[index][1] and search_time<=sepcial_value[index][2]<=current_time:
                                        flag=True
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



