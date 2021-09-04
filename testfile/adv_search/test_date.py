# -*- coding: utf-8 -*-
# 时间类型测试
import pytest,time,yaml
from adv_search.search_API import search
host = 'test'
search = search(host)
current_time=int(time.time()*1000)
past_value=[f'{current_time-7776000000}-{current_time}',f'{current_time-31104000000}-{current_time}',
          f'{current_time-155520000000}-{current_time-31104000000}']
#3月内，1年内，1-5年（1个月按30天算，1年按360天算）
value=[f'{current_time}-{current_time+7776000000}',f'{current_time}-{current_time+31104000000}',f'{current_time+31104000000}-{current_time+155520000000}']
#未来 3月内，1年内，1-5年

with open('date.yaml') as f:
    yaml_data=yaml.safe_load(f)
past_key=yaml_data['past_key']
key=yaml_data['key']

class TestSearchdate():
    def special_key_compare(self,key,value,es_key_list,es_result):
        if key.split('.')[0] not in es_key_list:
            assert True == False  # 这是一个必错的判断
        elif es_result[key.split('.')[0]] == []:
            assert True == False  # 这是个必错的情况
        else:
            # 只要有一个在该时间范围就可以
            flag = False
            for x in range(len(es_result[key.split('.')[0]])):
                if es_result[key.split('.')[0]][x][key.split('.')[1]] == None:
                    pass  # 单个无值ok,若所有无值，则flag保持False
                else:
                    if int(value.split('-')[0]) <= es_result[key.split('.')[0]][x][key.split('.')[1]] <= int(
                            value.split('-')[1]):
                        flag = True
                        break
            assert flag == True

    @pytest.mark.parametrize('value',past_value)
    @pytest.mark.parametrize('key',past_key)
    def test_date_past(self,key, value,ES):
        special_key_list=['adminLicense.createDate','tender.pubDate','recruitment.releaseDate','entAlter.alterDate']
        es_client = ES
        data = search.search_API(key, value,'BETWEEN')
        # print(data)
        print(key,value)
        assert len(data['items']) != 0
        time.sleep(2)
        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 在ES中确认
            es_result=es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，以判断是否有该字段
            es_key_list = []
            for es_key in es_result.keys():
                es_key_list.append(es_key)
            print(es_key_list)

            if key in special_key_list:
                self.special_key_compare(key,value,es_key_list, es_result)
            else:
                if key not in es_key_list:
                    assert True == False  # 这是个必错的情况
                elif es_result[key]==None:
                    assert True == False  # 这是个必错的情况
                elif key in ['webLastChangeDate','tradeShowStartDate','patentApplyDate','patentApplyPubDate','trademarkApplyDate' ]:
                    #es的字段是list类型的都要加到这里
                    flag = False
                    for x in range(len(es_result[key])):
                        if int(value.split('-')[0]) <= es_result[key][x] <= int(value.split('-')[1]):
                            flag = True
                            break
                    assert flag == True
                else:
                    assert int(value.split('-')[0])<=es_result[key]<=int(value.split('-')[1])

    @pytest.mark.parametrize('value', past_value+value)
    @pytest.mark.parametrize('key', key)
    def test_date(self, key, value, ES):
        special_key_list = ['adminLicense.expireDate','certificate.endDate']
        es_client = ES
        data = search.search_API(key, value, 'BETWEEN')
        # print(data)
        print(key, value)
        assert len(data['items']) != 0
        time.sleep(2)
        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 在ES中确认
            es_result = es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，以判断是否有该字段
            es_key_list = []
            for es_key in es_result.keys():
                es_key_list.append(es_key)

            if key in special_key_list:
                self.special_key_compare(key,value,es_key_list, es_result)
            else:
                if key not in es_key_list:
                    assert True == False  # 这是个必错的情况
                elif es_result[key] == []:
                    assert True == False  # 这是个必错的情况
                else: #domainExpireDate
                    flag = False
                    for x in range(len(es_result[key])):
                        if int(value.split('-')[0]) <= es_result[key][x]<= int(value.split('-')[1]):
                            flag = True
                            break
                    assert flag == True
