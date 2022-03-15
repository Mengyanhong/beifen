
import time
import urllib3
from API_project.Configs.Config_Info import user
from API_project.Configs.search_Api import search
# from API_project.conftest import ES
import requests, pytest, os
from elasticsearch import Elasticsearch
urllib3.disable_warnings()

ES = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，prod
                   http_auth=('mengyanhong', 'Aa123456'))
HOST = "test"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
user_configs = user(HOST)
skb_search_configs = search(HOST)


class Test_search:

    def contacts_num_search(self, pid):  # 联系方式搜索条件+详情页数据对比case
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
            detail_response = skb_search_configs.skb_contacts(id=pid, module='advance_search_detail')
            detail_response_contacts = detail_response.json()['data']['contacts']
            detail_response.close()
            details_response_contacts_value = detail_response_contacts
        if details_response_contacts_value:
            for details_response_value in details_response_contacts_value:
                if details_response_value['type'] == 1:
                    if details_response_value['content'] not in es_result["mobilePhone"]:
                        print('手机', details_response_value)
                elif details_response_value['type'] == 2:
                    if details_response_value['content'] not in es_result["fixedPhone"]:
                        print('固话', details_response_value)
                elif details_response_value['type'] == 4:
                    if details_response_value['content'] not in es_result["email"]:
                        print('邮箱', details_response_value)
        return "测试结束"



if __name__ == '__main__':
    print(Test_search().contacts_num_search(pid="3893a695e5cf5fbeed974041ebf30e40"))
