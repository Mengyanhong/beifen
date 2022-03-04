from pprint import pprint
import requests, json, time, pytest, os, random
from API_project.Configs.config_API import user
from API_project.Configs.search_API import search
from API_project.Configs.shop_API import shop_api
from API_project.Libs.sync_robot_libs import Sync_robot


# 转移操作通用Api
class sync_config:
    def __init__(self, host, way):
        self.host = host
        self.search = search(host)
        self.shop_search = shop_api(host)
        self.user_api = user(host)
        self.way = way

    # 转移前各维度搜索结果处理
    def search_value_list(self):
        # 搜索未查看，未转机器人的数据，有固话
        if self.way == 'search_list':
            response = self.search.skb_search()
            list_companyName_add = 'companyName'
        elif self.way == 'advanced_search_list':
            response = self.search.advanced_search()
            list_companyName_add = 'companyName'
        elif self.way == 'shop_search_list':
            response = self.shop_search.search_shop()
            list_companyName_add = 'name'
        else:
            response = self.search.skb_address_search(contact=2)
            list_companyName_add = 'companyName'

        request_payloads = json.loads(response.request.body.decode("unicode_escape"))
        request_url = response.request.url
        request_headers = response.request.headers
        response_value = response.json()
        response.close()
        if response_value['data'] == {}:
            print("搜索结果为空", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data'] != {}
        elif response_value['data']['total'] == 0:
            print("搜索结果为空", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['data']['total'] != 0
        elif response_value["error_code"] != 0:
            print("搜索异常", response_value, "\n搜索传参", request_payloads, "\n搜索url", request_url, "\n搜索heardes",
                  request_headers)
            assert response_value['error_code'] != 0
        pid_list = []
        pid_companyName_list = []
        # if way is None:
        #     pid = None
        #     pages = 500
        # elif page is None:
        #     pid = pid_list
        #     pages = None
        # else:
        #     pid = None
        #     pages = page

        if response_value['data']['items']:
            for i in response_value['data']['items']:
                pid_list.append(i['id'])
                pid_companyName_list.append(
                    {'pid': i['id'], 'company_name': i[list_companyName_add]})
        return {"pid_list": pid_list, "pid_companyName_list": pid_companyName_list,
                "payloads_request": request_payloads}

    # 转移后等待转移结束
    def search_elapsed_time(self):
        # for date_value in range(200):
        # starting_time = time.time()
        time.sleep(2.2)
        if self.way == 'search_list':
            response = self.search.skb_search().json()
        elif self.way == 'advanced_search_list':
            response = self.search.advanced_search().json()
        elif self.way == 'shop_search_list':
            response = self.shop_search.search_shop().json()
        else:
            response = self.search.skb_address_search(contact=2).json()
        if response['error_code'] == 0:
            # end_time = time.time()
            print("转移结束")
            # print('转移耗时', int(time.time() - stattime), 's')
        elif response['error_code'] == 401:
            print("接口401", response)
        elif response['error_code'] == 10007:
            self.search_elapsed_time()
        else:
            print("接口调用失败，搜索结果\n", response)

    # 联系方式获取
    def list_contact(self, pid, entName):
        contact_response = self.search.skb_contacts_num(id=pid, module=self.way).json()
        contact_response_contact = contact_response['data']['contacts']
        contact_response_contactNum = contact_response['data']['contactNum']
        if contact_response["error_code"] != 0:
            print(pid, entName, "联系方式接口调用失败", contact_response)
        hasMobile_sum = 0
        hasFixed_sum = 0
        hasEmail_sum = 0
        hasQq_sum = 0
        if contact_response_contact:
            details_response_contacts_value = contact_response_contact
        elif contact_response_contactNum != 0:
            contact_response_tow = self.search.skb_contacts(id=pid, entName=entName, module=self.way).json()
            if contact_response_tow["error_code"] != 0:
                print(pid, entName, "联系方式接口调用失败tow", contact_response_tow)
            if not contact_response_tow['data']['contacts']:
                print(pid, entName, "有联系方式但是获取失败tow", contact_response_tow)
            details_response_contacts_value = contact_response_tow['data']['contacts']
        else:
            print('pid:', pid, '企业名称', entName, '\n该企业联系方式为空', contact_response)
            details_response_contacts_value = []
        for contacts_value in details_response_contacts_value:
            if contacts_value['type'] == 1:
                hasMobile_sum += 1
            if contacts_value['type'] == 2:
                hasFixed_sum += 1
            if contacts_value['type'] == 3:
                hasQq_sum += 1
            if contacts_value['type'] == 4:
                hasEmail_sum += 1


