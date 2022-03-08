import requests, json, urllib3

urllib3.disable_warnings()


class Url_Host_Config:
    def __init__(self, host):
        self.host = host

    def skb_url_Host(self):  # 新搜客宝host
        if self.host == 'test':
            url_Host = 'skb-test.weiwenjia.com'
        elif self.host == 'staging':
            url_Host = 'skb-staging.weiwenjia.com'
        else:
            url_Host = 'skb.weiwenjia.com'
        return url_Host

    def biz_url_Host(self):  # 老搜客宝host
        if self.host == 'test':
            url_Host = 'test.lixiaoskb.com'
        elif self.host == 'staging':
            url_Host = 'stage.lixiaoskb.com'
        else:
            url_Host = 'biz.lixiaoskb.com'
        return url_Host

    def visitor_url_Host(self):  # 访客识别host
        if self.host == 'test':
            url_Host = 'visitor-test.weiwenjia.com'
        elif self.host == 'staging':
            url_Host = 'visitor-stage.weiwenjia.com'
        else:
            url_Host = 'visitor.weiwenjia.com'

        return url_Host

    def robot_url_Host(self):  # 机器人host
        if self.host == 'test':
            url_Host = 'jiqiren-test.weiwenjia.com'
        elif self.host == 'staging':
            url_Host = 'jiqiren-staging.weiwenjia.com'
        else:
            url_Host = 'jiqiren.weiwenjia.com'
        return url_Host


class User_Config(Url_Host_Config):
    def __init__(self, host, headers_parameters=None):
        super(User_Config, self).__init__(host)
        self.headers_parameters = headers_parameters

    def user_file(self):  # 用户headers环境配置,用户信息
        if self.host == 'test':  # 13162863099,Ik123456,python专用
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            token = "ad99f29c019e31af42ae5aa5b3db90ec"
            platform = 'lixiaoyun'
            gatewayId = 1181
        elif self.host == 'staging':  # 17388888888,Ik123456
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            token = 'b1a2727816c5a1bd7405a545e0927e81'
            platform = 'ikcrm'
            gatewayId = None
        else:  # 13162863099,励销云(CRM+机器人+skb)
            app_token = 'a14cc8b00f84e64b438af540390531e4'
            token = '18033bf7b969d9b12ef830c66c1f2464'
            platform = 'lixiaoyun'
            gatewayId = 9683
        return {'app_token': app_token, 'authorization': f'Token token={token}', 'crm_platform_type': platform,
                'gatewayId': gatewayId, 'token': f'{token}'}

    def user_file02(self):  # 用户headers环境配置,用户信息
        if self.host == 'test':  # 13162863099,Ik123456,python专用
            app_token = '2'
            token = "2"
            platform = 'lixiaoyun'
            gatewayId = 1181
        elif self.host == 'staging':  # 17388888888,Ik123456
            app_token = '2'
            token = '2'
            platform = 'ikcrm'
            gatewayId = None
        else:  # 13162863099,励销云(CRM+机器人+skb)
            app_token = '2'
            token = '2'
            platform = 'lixiaoyun'
            gatewayId = 9683

        return {'app_token': app_token, 'authorization': f'Token token={token}', 'crm_platform_type': platform,
                'gatewayId': gatewayId, 'token': f'{token}'}

    def user_file03(self):  # 用户headers环境配置,用户信息
        if self.host == 'test':  # 13162863099,Ik123456,python专用
            app_token = '3'
            token = "3"
            platform = 'lixiaoyun'
            gatewayId = 1181
        elif self.host == 'staging':  # 17388888888,Ik123456
            app_token = '3'
            token = '3'
            platform = 'ikcrm'
            gatewayId = None
        else:  # 13162863099,励销云(CRM+机器人+skb)
            app_token = '3'
            token = '3'
            platform = 'lixiaoyun'
            gatewayId = 9683

        return {'app_token': app_token, 'authorization': f'Token token={token}', 'crm_platform_type': platform,
                'gatewayId': gatewayId, 'token': f'{token}'}

    def headers_skb(self, headers_parameters=None):  # headers环境配置
        if headers_parameters is not None:
            headers = {
                'app_token': headers_parameters["app_token"],
                'authorization': headers_parameters["authorization"],
                'content-type': 'application/json',
                'crm_platform_type': headers_parameters["crm_platform_type"]
            }
        elif self.headers_parameters is None:
            headers = {
                'app_token': self.user_file()["app_token"],
                'authorization': self.user_file()["authorization"],
                'content-type': 'application/json',
                'crm_platform_type': self.user_file()["crm_platform_type"]
            }
        else:
            headers = {
                'app_token': self.headers_parameters["app_token"],
                'authorization': self.headers_parameters["authorization"],
                'content-type': 'application/json',
                'crm_platform_type': self.headers_parameters["crm_platform_type"]
            }
        return headers

    def userinfo_skb_Api(self):  # 查询新SKB用户信息
        url = f'https://{self.skb_url_Host()}/api_skb/v1/user/userInfo'
        response = requests.get(url=url, headers=self.headers_skb(), verify=False)
        return response

    def headers_robot(self, headers_parameters=None):  # 机器人headers配置
        if headers_parameters is not None:
            headers = {
                'platform': 'IK',
                'usertoken': headers_parameters["usertoken"],
                'content-type': 'application/json',
                'crmplatformtype': headers_parameters["crm_platform_type"]
            }
        elif self.headers_parameters is None:
            headers = {
                'platform': 'IK',
                'usertoken': self.user_file()["token"],
                'content-type': 'application/json',
                'crmplatformtype': self.user_file()["crm_platform_type"]
            }
        else:
            headers = {
                'platform': 'IK',
                'usertoken': self.headers_parameters["token"],
                'content-type': 'application/json',
                'crmplatformtype': self.headers_parameters["crm_platform_type"]
            }
        return headers
        # lxcrm_Headers = {
        #     'platform': 'IK',
        #     'usertoken': self.user_key()["token"],
        #     'Content-Type': 'application/json',
        #     'crmplatformtype': self.user_key()["platform"]
        # }
        # # test_Headers = {
        # #     'platform': 'IK',
        # #     'userToken': Token,
        # #     'Content-Type': 'application/json',
        # #     'CrmPlatformType': platform
        # # }
        # return lxcrm_Headers
        # # if self.host == 'lxcrm':
        # #     return lxcrm_Headers
        # # else:
        # #     return test_Headers

    def robot_gateway(self, headers_parameters=None):  # headers环境配置
        if headers_parameters is not None:
            gatewayId = {
                'gatewayId': headers_parameters["gatewayId"]
            }
        elif self.headers_parameters is None:
            gatewayId = {
                'gatewayId': self.user_file()["gatewayId"],
            }
        else:
            gatewayId = {
                'gatewayId': self.headers_parameters["gatewayId"],
            }
        return gatewayId


# if __name__ == '__main__':
#     headers = {
#         'app_token': "app_token",
#         'authorization': "authorization",
#         'content-type': 'application/json',
#         'crm_platform_type': "crm_platform_type"
#     }
#     hear = User_Config("test")
#     print(hear.headers_skb())
#     print(hear.headers_skb(header=hear.user_file03()))
#     print(User_Config("test", header=User_Config("test").user_file02()).headers_skb())
#     print(hear.headers_skb(header=headers))
#     print(User_Config("test", header=headers).headers_skb())
#     print(hear.skb_url_Host())


class Configuration_Api_File(User_Config):  # 配置文件调用

    def conditionGroups_Api(self):  # 高级搜索搜索条件
        path = '/api_skb/v1/companyDetail/conditionGroups?groupName=enterprise&category=advancedSearch'
        response = requests.get(self.biz_url_Host() + path, headers=self.headers_skb(), verify=False)
        return response

    def staticConfig_Api(self):  # 来源（contactSource）站配置
        path = '/api_skb/v1/companyDetail/staticConfig?namespace=withLevels'
        response = requests.get(self.biz_url_Host() + path, headers=self.headers_skb(), verify=False)
        response = response.json()['data']
        return response

    def staticConfig_recruitPlatformOption(self):  # 经营情况详情页筛选配置，recruitPlatformOption：招聘平台
        path = '/api_skb/v1/companyDetail/staticConfig?namespace=semPlatformOption,recruitPlatformOption,' \
               'tenderOption,semTypeOption'
        response = requests.get(self.biz_url_Host() + path, headers=self.headers_skb(), verify=False)
        response = response.json()['data']
        return response

    def staticConfig_IPR(self):  # 知识产权详情页筛选配置，templateSuppilerOption：建站方，trademarkTypeOption：商标类别
        path = '/api_skb/v1/companyDetail/staticConfig?namespace=trademarkTypeOption,templateSuppilerOption'
        response = requests.get(self.biz_url_Host() + path, headers=self.headers_skb(), verify=False)
        response = response.json()['data']
        return response

    def shopCategory(self):  # 店铺分类（shopCategory）配置
        path = '/api_skb/v1/companyDetail/staticConfig?namespace=shopCategory'
        response = requests.get(self.biz_url_Host() + path, headers=self.headers_skb(), verify=False)
        response = response.json()['data']
        return response

    def conditionConfig(self):  # 高级搜索搜索条件（conditionConfig）配置
        path = '/api_skb/v1/companyDetail/conditionConfig?groupName=enterprise&category=advancedSearch'
        response = requests.get(self.biz_url_Host() + path, headers=self.headers_skb(), verify=False).json()
        return response['data']

    def shopDivision(self):  # 店铺地区（shopDivision）配置
        path = '/api_skb/v1/companyDetail/staticConfig?namespace=shopDivision'
        response = requests.get(self.biz_url_Host() + path, headers=self.headers_skb(), verify=False).json()
        return response['data']['shopDivision']
        # a = r.text.encode(encoding="utf-8",errors="strict").decode(encoding="utf-8",errors="strict")#decode("unicode_escape")
        # a = json.dumps(r,ensure_ascii=False).encode("utf-8",errors="ignore").decode('utf-8',errors="ignore")
        # r = json.loads(r.text)
        # a = json.dumps(r, ensure_ascii=False).encode("utf-8", errors="ignore").decode('utf-8',errors="ignore")
        # b = open(r.text,encoding="utf-8")
        # file = open(r"C:\Users\admin\PycharmProjects\API_project\data\text\areer.yaml","w+",encoding="utf-8")
        # file.write(a)
        # file.close()
        # re_file = open(r"C:\Users\admin\PycharmProjects\API_project\data\text\areer.json")
        # data=json.loads(re_file)['data']['shopDivision']
        # data = a
        # print(re_file.json)
#
# # if __name__ == '__main__':
# #     print(user('test').headers())
# if __name__ == '__main__':
#     import pprint
#     from API_project.tools.install_Excel import install_Excel
#     install_files = install_Excel(file_name="联系方式渠道配置", file_title_name="联系方式渠道配置")  # 实例化测试报告文件
#     if install_files.read_sum() == 1 and install_files.read_one_value() is None:
#         install_files.install(row=1, column=1, value='name')
#         install_files.install(row=1, column=2, value='value')
#         install_files.install(row=1, column=3, value='dbName')
#     staticConfig = configuration_file('test').staticConfig()['contactSiteSourceMap']
#     staticConfig_list = []
#     for staticConfig_value in staticConfig:
#         for i in staticConfig_value['sub']:
#             # print(i)
#             # break
#             row_sum = install_files.read_sum() + 1
#             install_files.install(row=row_sum, column=1, value=i['name'])
#             install_files.install(row=row_sum, column=2, value=i['value'])
#             install_files.install(row=row_sum, column=3, value=i['dbName'])
#         staticConfig_list = staticConfig_list+staticConfig_value['sub']
#         # for sub in staticConfig_value['sub']:
#         #     staticConfig_list.append(sub)
#     # for v in staticConfig_list:
#     #     for key, value in v.items():
#     #         print(key, value)
#     #     break
#     print(staticConfig_list)
#     # print(configuration_file('test').staticConfig_recruitPlatformOption()['recruitPlatformOption'] )
    # if __name__ == '__main__':
    #     staticConfig = configuration_file('lxcrm').staticConfig()['contactSiteSourceMap']  # 实例化高级搜索配置withLevels并返回配置信息
    #     print(staticConfig)
    #     staticConfig_lists = []
    #     for staticConfig_value in staticConfig:
    #         staticConfig_list = staticConfig_lists + staticConfig_value['sub']