# -*- coding: utf-8 -*-
import yaml,pytest,time
from ..adv_search.search_API import search_API

with open('singleSelect.yaml') as f:
    key_list = yaml.safe_load(f)
value_list = [True, False]
today = int(time.time() * 1000)

class TestSingleSelect:
    @pytest.mark.parametrize('value',value_list)
    @pytest.mark.parametrize('key', key_list)
    def test_singleSelect(self,value,key,ES):
        es_client = ES
        data = search_API(key, value, 'IS')
        # print(data)
        print(key, value)
        assert len(data['items']) != 0
        for i in range(len(data['items'])):
            pid = data['items'][i]['id']
            companyName = data['items'][i]['companyName']
            print(pid)
            print(companyName)

            # 在ES中确认
            es_result = es_client.get(index="company_info_prod", id=pid)['_source']
            # 返回es中所有的键，判断字段是否存在
            es_key_list = []
            for es_key in es_result.keys():
                es_key_list.append(es_key)

            if key=='isHighTech':
                if 'certificate' not in es_key_list:
                    result =False
                elif es_result['certificate']==[]:
                    result = False
                else:
                    result = False
                    for j in range(len(es_result['certificate'])):
                        if 'category' not in list(es_result['certificate'][j].keys()) or 'endDate' not in list(es_result['certificate'][j].keys()):
                            pass#判断字段是否存在
                        elif es_result['certificate'][j]['category']==1 and (es_result['certificate'][j]['endDate']==None or
                                                                             es_result['certificate'][j]['endDate']>today):
                            result = True
                            break
                assert result == value

            else:
                if key not in es_key_list:
                    result = False
                    assert result == value
                else:
                    assert es_result[key] == value



