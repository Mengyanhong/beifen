import time

from API_project.Configs.Configuration import user
from API_project.Configs.search_API import search
from API_project.tools.install_Excel import install_Excel
import requests, pytest, os

HOST = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
user_configs = user(HOST)
skb_search_configs = search(HOST)


class Test_search:
    # @pytest.mark.parametrize('contact', [1, 2, 3, 4, 5])  # 基本信息
    def search_api(self, contact):
        url = f'https://{user_configs.skb_Host()}/api_skb/v1/search'
        payload = {
            "keyword": "科技",
            "filter": {
                "location": [],
                "industryshort": [],
                "secindustryshort": [],
                "registercapital": [],
                "establishment": [],
                "entstatus": [],
                "contact": [contact],
                "sortBy": "0",
                "companysource": [],
                "enttype": [
                    0
                ],
                "employees": [
                    0
                ],
                "hasrecruit": "0",
                "hassem": "0",
                "haswebsite": "0",
                "hastrademark": "0",
                "haspatent": "0",
                "hastender": "0",
                "haswechataccnt": "0",
                "filterUnfold": 0,
                "filterSync": 0,
                "filterSyncRobot": 0,
                "hasBuildingCert": "0",
                "isHighTech": "0",
                "hasFinanceInfo": "0",
                "hasAbnormalInfo": "0",
                "syncRobotRangeDate": []
            },
            "scope": "",
            "matchType": "most_fields",
            "pagesize": 10,
            "page": 1
        }
        time.sleep(3)
        response = requests.post(url, headers=user_configs.headers(), json=payload,
                                 verify=False)  # 搜索未查看，未转机器人,未转crm，有手机，有固话的数据
        # print(response.json())
        return response

    @pytest.mark.parametrize('contact', [1, 2, 3, 4, 5])  # 联系方式
    def test_contacts_num_search(self, contact):  # 联系方式搜索条件+详情页数据对比case
        pid_list = []
        time.sleep(2.2)
        pid_responst = Test_search().search_api(contact).json()['data']['items']
        if pid_responst:
            for pid in pid_responst:
                pid_list.append({'pid': pid['id'], 'entName': pid['name']})
        assert pid_list != []
        for i in pid_list:
            details_response = skb_search_configs.skb_contacts_num(id=i['pid'], module='advance_search_detail')
            details_response_contacts = details_response.json()['data']['contacts']
            details_response_contactNum = details_response.json()['data']['contactNum']
            details_response.close()
            details_response_contacts_value = None
            hasMobile_sum = 0
            hasFixed_sum = 0
            hasEmail_sum = 0
            hasQq_sum = 0
            if details_response_contacts:
                details_response_contacts_value = details_response_contacts
            elif details_response_contacts == [] and details_response_contactNum != 0:
                detail_response = skb_search_configs.skb_contacts(id=i['pid'], entName=i['entName'],
                                                            module='advance_search_detail')
                detail_response_contacts = detail_response.json()['data']['contacts']
                detail_response.close()
                details_response_contacts_value = detail_response_contacts
            else:
                if contact == 5:
                    if details_response_contacts != [] or details_response_contactNum != 0:
                        print('pid:', i, '搜索条件', contact, '\n该企业联系方式有误查询结果为', details_response)
                    assert details_response_contacts == [] and details_response_contactNum == 0
                else:
                    if contact != 5:
                        print('pid:', i, '搜索条件', contact, '\n该企业联系方式有误查询结果为', details_response)
                    assert contact == 5
            if details_response_contacts_value:
                for details_response_value in details_response_contacts_value:
                    if contact == 1:
                        if details_response_value['type'] == 1:
                            hasMobile_sum += 1
                            break
                        else:
                            continue
                    elif contact == 2:
                        if details_response_value['type'] == 2:
                            hasFixed_sum += 1
                            break
                        else:
                            continue
                    elif contact == 3:
                        if details_response_value['type'] == 4:
                            hasEmail_sum += 1
                            break
                        else:
                            continue
                    elif contact == 4:
                        if details_response_value['type'] == 3:
                            hasQq_sum += 1
                            break
                        else:
                            continue
                    else:
                        continue
            else:
                continue
            if contact == 1:
                if hasMobile_sum == 0:
                    print('pid:', i, '搜索条件', contact, '\n')
                assert hasMobile_sum != 0
            elif contact == 2:
                if hasFixed_sum == 0:
                    print('pid:', i, '搜索条件', contact, '\n')
                assert hasFixed_sum != 0
            elif contact == 3:
                if hasEmail_sum == 0:
                    print('pid:', i, '搜索条件', contact, '\n')
                assert hasEmail_sum != 0
            elif contact == 4:
                if hasQq_sum == 0:
                    print('pid:', i, '搜索条件', contact, '\n')
                assert hasQq_sum != 0
            else:
                if details_response_contacts != [] or details_response_contactNum != 0:
                    print('pid:', i, '搜索条件', contact, '\n')
                assert details_response_contacts == [] and details_response_contactNum == 0



