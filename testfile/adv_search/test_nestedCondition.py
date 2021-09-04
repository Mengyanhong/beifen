# -*- coding: utf-8 -*-
# 测试组合条件
import yaml,time,pytest
from adv_search.search_API import nestedSearch_API

with open('./nestedCondition.yaml',encoding='utf-8') as f:
    yamldata=yaml.safe_load(f)
print(yamldata)
key_list=list(yamldata.keys())

#IN&NOT_IN 中可以有多个值
class TestBindCondition:
    global bindata
    bindata = []  # 存放处理好的绑定条件
    def setup(self):
        for key in key_list:
            # 在CV中取两个字段进行绑定组合
            value=[]
            for i in range(len(yamldata[key])-1):
                for j in range(i+1,len(yamldata[key])):
                    cv_list_ele = []  # 精细化cv的每一个组合
                    cv_list_ele.append(yamldata[key][i])
                    cv_list_ele.append(yamldata[key][j])
                    value.append(cv_list_ele)

            # 把每个条件中的CV，CR值进行遍历
            value_final = []
            for value_ele in value:
                for cr0_ele in value_ele[0]['cr']:
                    if cr0_ele!='NOT_IN':  # 去除第一条件关系为NOT_IN的情况
                        for cv0_ele in value_ele[0]['cv']:
                            for cr1_ele in value_ele[1]['cr']:
                                for cv1_ele in value_ele[1]['cv']:
                                    value_final.append([{'cn': value_ele[0]['cn'], 'nn':value_ele[0]['nn'],'cr': cr0_ele, 'cv': cv0_ele},
                                                 {'cn': value_ele[1]['cn'],'nn':value_ele[1]['nn'], 'cr': cr1_ele, 'cv': cv1_ele}])
            ele_dict = {key:value_final}
            bindata.append(ele_dict)
        # print(bindata)

    @pytest.mark.parametrize('key',key_list)
    def test_bindCondition(self,key,ES):
        es_client = ES
        index=key_list.index(key)
        for value in bindata[index][key]:
            time.sleep(2)
            data = nestedSearch_API(value[0]['cn'], value[0]['nn'],value[0]['cr'],value[0]['cv'],value[1]['cn'], value[1]['nn'],value[1]['cr'],value[1]['cv'])
            # print(data)
            print(value[0]['cn'], value[0]['nn'],value[0]['cr'],value[0]['cv'],value[1]['cn'], value[1]['nn'],value[1]['cr'],value[1]['cv'])
            if len(data['items'])==0:
                print('长度为0')
            assert len(data['items']) != 0

            for i in range(len(data['items'])):
                pid = data['items'][i]['id']
                companyName = data['items'][i]['companyName']
                print(pid)
                print(companyName)

                # 在ES中确认
                es_result = es_client.get(index="company_info_prod", id=pid)['_source']

                field_level0 = value[0]['nn'].split('.')[0]
                field_level1=[value[0]['nn'].split('.')[1],value[1]['nn'].split('.')[1]]

                try:
                    for ele in es_result[field_level0]:
                        flag = [False,False]
                        for x in [0, 1]:#遍历两个条件
                            if value[x]['cr'] == 'BETWEEN':
                                date = []
                                date.append(int(value[x]['cv'].split('-')[0]))
                                date.append(int(value[x]['cv'].split('-')[1]))
                                if ele[field_level1[x]]!=None and date[0] <=ele[field_level1[x]]<=date[1]:
                                    flag[x] = True
                            elif value[x]['cr'] =='IN' and value[x]['cv'] in str(ele[field_level1[x]]):
                                flag[x] = True
                            elif value[x]['cr'] =='NOT_IN' and value[x]['cv'] not in str(ele[field_level1[x]]):
                                flag[x] = True

                        if flag==[True,True]:
                            break
                        else:
                            continue
                    print(flag)
                    assert flag==[True,True]
                except KeyError:
                    return KeyError



