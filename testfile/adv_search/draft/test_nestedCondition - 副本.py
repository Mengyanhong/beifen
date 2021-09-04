# -*- coding: utf-8 -*-
import yaml,time,pytest
from skb_project.adv_search.search_API import nestedSearch_API

with open('./nestedCondition.yaml',encoding='utf-8') as f:
    yamldata=yaml.safe_load(f)
print(yamldata)
key_list=list(yamldata.keys())
# int_field=['certL2Type']
# str_field=['certL2Name','certificate.certOrgName']
# data_field=['certificate.endDate']


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
        print(bindata)

    @pytest.mark.parametrize('key',key_list)
    def test_bindCondition(self,key,ES):
        es_client = ES
        index=key_list.index(key)
        for value in bindata[index][key]:
            print(value)
            data = nestedSearch_API(value[0]['cn'], value[0]['nn'],value[0]['cr'],value[0]['cv'],value[1]['cn'], value[1]['nn'],value[1]['cr'],value[1]['cv'])
            print(data)
            print(value[0]['cn'], value[0]['nn'],value[0]['cr'],value[0]['cv'],value[1]['cn'], value[1]['nn'],value[1]['cr'],value[1]['cv'])
            assert len(data['items']) != 0
            time.sleep(1)
            for i in range(len(data['items'])):
                print(i)
                pid = data['items'][i]['id']
                companyName = data['items'][i]['companyName']
                print(pid)
                print(companyName)

                # 在ES中确认
                es_result = es_client.get(index="company_info_prod", id=pid)['_source']
                # # 返回es中所有的键，以判断是否有该字段
                field_level0=value[0]['nn'].split('.')[0]
                field_level10=value[0]['nn'].split('.')[1]
                field_level11=value[1]['nn'].split('.')[1]

                int_field = ['certL2Type']
                str_field = ['certL2Name', 'certificate.certOrgName']
                data_field = ['certificate.endDate']

                try:
                    flag = False
                    if value[0]['cr']=='IN' and value[1]['cr']=='IN':
                        for ele in es_result[field_level0]:



                # try:
                #     flag = False
                #     if value[0]['cr']=='IN' and value[1]['cr']=='IN':
                #         for ele in es_result[field_level0]:
                #             for cv0 in value[0]['cv']:
                #                 for cv1 in value[1]['cv']:
                #                     if
                #
                #
                #
                #                     if cv0
                #                     if int(cv0)==ele[field_level10] and int(cv1)!=ele[field_level11]:
                #                         flag=True
                #                         break
                #     elif value[0]['cr']=='IN' and value[1]['cr']=='NOT_IN':
                #         for ele in es_result[field_level0]:
                #             for cv0 in value[0]['cv']:
                #                 for cv1 in value[1]['cv']:
                #                     if int(cv0)==ele[field_level10] and int(cv1)!=ele[field_level11]:
                #                         flag=True
                #                         break
                #     elif value[0]['cr']=='IN' and value[1]['cr']=='BETWEEN':
                #         date10 = int(value[1]['cv'][0].split('-')[0])
                #         date11 = int(value[1]['cv'][0].split('-')[1])
                #         for ele in es_result[field_level0]:
                #             for cv0 in value[0]['cv']:
                #                 if int(cv0)==ele[field_level10] and ele[field_level11]!=None and date10<=ele[field_level11]<=date11:
                #                     flag=True
                #                     break
                #     elif value[0]['cr']=='BETWEEN' and value[1]['cr']=='IN':
                #         date00=int(value[0]['cv'][0].split('-')[0])
                #         date01=int(value[0]['cv'][0].split('-')[1])
                #         for ele in es_result[field_level0]:
                #             for cv1 in value[1]['cv']:
                #                 if date00<=ele[field_level10]<=date01 and ele[field_level10]!=None and int(cv1)==ele[field_level11]:
                #                     flag=True
                #                     break
                #     elif value[0]['cr']=='BETWEEN' and value[1]['cr']=='NOT_IN':
                #         date00 = int(value[0]['cv'][0].split('-')[0])
                #         date01 = int(value[0]['cv'][0].split('-')[1])
                #         for ele in es_result[field_level0]:
                #             for cv1 in value[1]['cv']:
                #                 if ele[field_level10]!=None and date00<=ele[field_level10]<=date01 and int(cv1)!=ele[field_level11]:
                #                     flag=True
                #                     break
                #     elif value[0]['cr']=='BETWEEN' and value[1]['cr']=='BETWEEN':
                #         date00 = int(value[0]['cv'][0].split('-')[0])
                #         date01 = int(value[0]['cv'][0].split('-')[1])
                #         date10 = int(value[1]['cv'][0].split('-')[0])
                #         date11 = int(value[1]['cv'][0].split('-')[1])
                #         for ele in es_result[field_level0]:
                #             if ele[field_level10]!=None and ele[field_level11]!=None and date00<=ele[field_level10]<=date01 and date10<=ele[field_level11]<=date11:
                #                 flag=True
                #                 break
                #     assert flag == True
                #
                # except KeyError:
                #     return KeyError



    # def test_bindCondition(self,ES):
    #     es_client = ES
    #     for i in range(len(bindata)):
    #         key=key_list[i]
    #         for value in bindata[i][key]:
    #             data = search_API(key, value, 'MUST')
    #             # print(data)
    #             print(key, value)
    #             assert len(data['items']) != 0
    #             time.sleep(1)
    #             for i in range(len(data['items'])):
    #                 pid = data['items'][i]['id']
    #                 companyName = data['items'][i]['companyName']
    #                 print(pid)
    #                 print(companyName)
    #
    #                 # 在ES中确认
    #                 es_result = es_client.get(index="company_info_prod", id=pid)['_source']
    #                 # # 返回es中所有的键，以判断是否有该字段
    #                 field_level0=value[0]['cn'].split('.')[0]
    #                 field_level10 = value[0]['cn'].split('.')[1]
    #                 field_level11 = value[1]['cn'].split('.')[1]
    #
    #                 try:
    #                     flag = False
    #                     if value[0]['cr']=='IN' and value[1]['cr']=='IN':
    #                         for ele in es_result[field_level0]:
    #                             for cv0 in value[0]['cv']:
    #                                 for cv1 in value[1]['cv']:
    #                                     if cv0 in ele[field_level10] and cv1 in ele[field_level11]:
    #                                         flag=True
    #                                         break
    #                     elif value[0]['cr']=='IN' and value[1]['cr']=='NOT_IN':
    #                         for ele in es_result[field_level0]:
    #                             for cv0 in value[0]['cv']:
    #                                 for cv1 in value[1]['cv']:
    #                                     if cv0 in ele[field_level10] and cv1 not in ele[field_level11]:
    #                                         flag=True
    #                                         break
    #                     elif value[0]['cr']=='IN' and value[1]['cr']=='BETWEEN':
    #                         date10 = value[1]['cv'][0].split('-')[0]
    #                         date11 = value[1]['cv'][0].split('-')[1]
    #                         for ele in es_result[field_level0]:
    #                             for cv0 in value[0]['cv']:
    #                                 if cv0 in ele[field_level10] and date10<=ele[field_level11]<=date11:
    #                                     flag=True
    #                                     break
    #                     elif value[0]['cr']=='BETWEEN' and value[1]['cr']=='IN':
    #                         date00=value[0]['cv'][0].split('-')[0]
    #                         date01=value[0]['cv'][0].split('-')[1]
    #                         for ele in es_result[field_level0]:
    #                             for cv1 in value[1]['cv']:
    #                                 if date00<=ele[field_level10]<=date01 and cv1 in ele[field_level11]:
    #                                     flag=True
    #                                     break
    #                     elif value[0]['cr']=='BETWEEN' and value[1]['cr']=='NOT_IN':
    #                         date00=value[0]['cv'][0].split('-')[0]
    #                         date01=value[0]['cv'][0].split('-')[1]
    #                         for ele in es_result[field_level0]:
    #                             for cv1 in value[1]['cv']:
    #                                 if date00<=ele[field_level10]<=date01 and cv1 not in ele[field_level11]:
    #                                     flag=True
    #                                     break
    #                     elif value[0]['cr']=='BETWEEN' and value[1]['cr']=='BETWEEN':
    #                         date00=value[0]['cv'][0].split('-')[0]
    #                         date01=value[0]['cv'][0].split('-')[1]
    #                         date10 = value[1]['cv'][0].split('-')[0]
    #                         date11 = value[1]['cv'][0].split('-')[1]
    #                         for ele in es_result[field_level0]:
    #                             if date00<=ele[field_level10]<=date01 and date10<=ele[field_level11]<=date11:
    #                                 flag=True
    #                                 break
    #                     assert flag == True
    #
    #                 except KeyError:
    #                     return KeyError
    #
    #
