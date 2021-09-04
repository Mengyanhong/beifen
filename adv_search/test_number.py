# -*- coding: utf-8 -*-
import pytest,random,yaml,time
from ..adv_search.search_API import search_API

with open('number.yaml') as f:
    yaml_data=yaml.safe_load(f)
big_key=yaml_data['big_key']
small_key=yaml_data['small_key']

random1=random.randint(10,50)
random2=random.randint(2,5)
big=[[f'{random1},{random1+20}'],[f'{random1+100},{random1+105}'],[f'{random1},{random1*10+400}'],
     [f'{random1},'],[f'{random1*10},'],[f',{random1}'],[f',{random1*10}']]

small=[[f'{random2},{random2+2}'],[f'{random2+2},{random2+4}'],[f'{random2-1},{random2+4}'],
     [f'{random2},'],[f'{random2+2},'],[f',{random2}'],[f',{random2+4}']]

class TestNumber():
    def compare(self,result,min,max):
        if min != '':
            assert result >= float(min)
            if max != '':
                assert result <= float(max)
        else:
            assert result<= float(max)

    def compare_list(self,result,min,max):
        if min != '':
            flag = False
            for cover in result:
                if cover >= int(min):
                    flag = True
                    break
            assert flag == True
            if max != '':
                flag = False
                for cover in result:
                    if cover <= int(max):
                        flag = True
                        break
                assert flag == True
        else:
            flag = False
            for cover in result:
                if cover <= int(max):
                    flag = True
                    break
            assert flag == True

    @pytest.mark.parametrize('value',big)
    @pytest.mark.parametrize('key',big_key)
    def test_number_big(self,key,value,ES):
        es_client = ES
        time.sleep(3)
        data = search_API(key, value,'BETWEEN')
        print(key,value)
        # print(data)
        assert len(data['items']) != 0
        min = value[0].split(',')[0]
        max = value[0].split(',')[1]
        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 和ES对比
            es_result = es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错d
            es_key_list = []
            for es_key in es_result.keys():
                es_key_list.append(es_key)

            if key not in es_key_list:
                assert True==False #这是一个必错的判断
            else:
                if key in ['baiduCover','qihu360Cover','sougouCover','websiteSpeed']:
                    self.compare_list(es_result[key], min, max)
                else:
                    self.compare(es_result[key], min, max)

    @pytest.mark.parametrize('value', small)
    @pytest.mark.parametrize('key', small_key)
    def test_number_small(self, key, value, ES,diff_date):
        es_client = ES
        data = search_API(key, value, 'BETWEEN')
        print(key, value)
        # print(data)
        assert len(data['items']) != 0
        min = value[0].split(',')[0]
        max = value[0].split(',')[1]
        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 和ES对比
            es_result = es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，去除 无该字段时的报错d
            es_key_list = []
            for es_key in es_result.keys():
                es_key_list.append(es_key)

            if key!='domainAge' and key not in es_key_list:
                assert True == False  # 这是一个必错的判断
            else:
                if key == 'domainAge':
                    if min != '':
                        flag = False
                        for cover in es_result['domainCreateDate']:
                            if diff_date(cover)[0] >= int(min):
                                flag = True
                                break
                        assert flag == True
                        if max != '':
                            flag = False
                            for cover in es_result['domainCreateDate']:
                                if diff_date(cover)[0]<= int(max):
                                    flag = True
                                    break
                            assert flag == True
                    else:
                        flag = False
                        for cover in es_result['domainCreateDate']:
                            if diff_date(cover)[0]<= int(max):
                                flag = True
                                break
                        assert flag == True

                elif key in ['baiduRank', 'qihu360Rank', 'sougouRank','baiduPcPage','baiduH5Page','domainRecordAge']:
                    self.compare_list(es_result[key], min, max)
                elif key=='appDownloadCount':
                    self.compare(es_result[key]/10000, min, max)
                else:
                    self.compare(es_result[key], min, max)




