import time
import urllib3
from API_project.Configs.config_API import user
from API_project.Configs.search_API import search
# from API_project.conftest import ES
import requests, pytest, os
from elasticsearch import Elasticsearch

urllib3.disable_warnings()

ES = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，prod
                   http_auth=('mengyanhong', 'Aa123456'))
HOST = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
user_configs = user(HOST)
skb_search_configs = search(HOST)


class Test_search:

    def contacts_num_search(self, pid, entName):  # 联系方式搜索条件+详情页数据对比case
        es_result = ES.get(index="company_info_prod", id=pid)['_source']
        # # 返回es中所有的键，去除 无该字段时的报错
        # es_key_list_list = []
        # for es_key_list in es_result.keys():
        #     es_key_list_list.append(es_key_list)
        details_response = skb_search_configs.skb_contacts_num(id=pid, module='advance_search_detail')
        details_response_contacts = details_response.json()['data']['contacts']
        details_response_contactNum = details_response.json()['data']['contactNum']
        details_response.close()
        details_response_contacts_value = None
        if details_response_contacts:
            details_response_contacts_value = details_response_contacts
        elif details_response_contacts == [] and details_response_contactNum != 0:
            detail_response = skb_search_configs.skb_contacts(id=pid, entName=entName, module='advance_search_detail')
            detail_response_contacts = detail_response.json()['data']['contacts']
            print(detail_response_contacts)
            detail_response.close()
            details_response_contacts_value = detail_response_contacts
        mobilePhone_list = []
        fixedPhone_list = []
        email_list = []
        if details_response_contacts_value:
            for details_response_value in details_response_contacts_value:
                if details_response_value['type'] == 1:
                    mobilePhone_list.append(details_response_value['content'])
                elif details_response_value['type'] == 2:
                    fixedPhone_list.append(details_response_value['content'])
                elif details_response_value['type'] == 4:
                    email_list.append(details_response_value['content'])

            # for details_response_value in details_response_contacts_value:
            #     if details_response_value['type'] == 1:
            #         mobilePhone_list.append(details_response_value['content'])
            #         if details_response_value['content'] not in es_result["mobilePhone"]:
            #             print('手机,详情页有ES没有', details_response_value['contact'],details_response_value['content'])
            #     elif details_response_value['type'] == 2:
            #         fixedPhone_list.append(details_response_value['content'])
            #         if details_response_value['content'] not in es_result["fixedPhone"]:
            #             print('固话,详情页有ES没有', details_response_value['contact'],details_response_value['content'])
            #     elif details_response_value['type'] == 4:
            #         email_list.append(details_response_value['content'])
            #         if details_response_value['content'] not in es_result["email"]:
            #             print('邮箱,详情页有ES没有', details_response_value['contact'],details_response_value['content'])
        print('ES没有详情页有，手机', set(mobilePhone_list).difference(set(es_result["mobilePhone"])))
        print('ES没有详情页有，固话', list(set(fixedPhone_list).difference(set(es_result["fixedPhone"]))))
        print('ES没有详情页有，邮箱', set(email_list).difference(set(es_result["email"])))
        print('ES有详情页没有，手机', set(es_result["mobilePhone"]).difference(set(mobilePhone_list)))
        print('ES有详情页没有，固话', list(set(es_result["fixedPhone"]).difference(set(fixedPhone_list))))
        print('ES有详情页没有，邮箱', len(list(set(es_result["email"]).difference(set(email_list)))))
        return f"测试结束pid为：{pid}"


if __name__ == '__main__':
    print(Test_search().contacts_num_search(pid="af7d4ceeec233412790bad11f9016be1", entName="广州旭众食品机械有限公司"))
