import requests, json, urllib3

urllib3.disable_warnings()


class user:
    def __init__(self, environment):
        self.test = environment

    def user_key(self):  # 用户headers环境配置,用户信息
        if self.test == 'test':  # 13162863099,Ik123456,python专用
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            Token_value = "ad99f29c019e31af42ae5aa5b3db90ec"
            platform = 'lixiaoyun'
            gatewayId = 1181
        elif self.test == 'staging':  # 17388888888,Ik123456
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            Token_value = 'b1a2727816c5a1bd7405a545e0927e81'
            platform = 'ikcrm'
            gatewayId = None
        elif self.test == 'lxcrm':
            app_token = 'a14cc8b00f84e64b438af540390531e4'
            Token_value = '18033bf7b969d9b12ef830c66c1f2464'
            platform = 'lixiaoyun'
            gatewayId = 9683
        else:
            print('传参错误')
            app_token = None
            Token_value = None
            platform = None
            gatewayId = None
        return {'app_token': app_token, 'Token': f'Token token={Token_value}', 'platform': platform,
                'gatewayId': gatewayId, 'token': f'{Token_value}'}

    def skb_Host(self):  # 新搜客宝host
        if self.test == 'test':
            host = 'skb-test.weiwenjia.com'
        elif self.test == 'staging':
            host = 'skb-staging.weiwenjia.com'
        elif self.test == 'lxcrm':
            host = 'skb.weiwenjia.com'
        else:
            print('传参错误')
            host = None
        return host

    def biz_url(self):  # 老搜客宝host
        if self.test == 'test':
            url = 'test.lixiaoskb.com'
        elif self.test == 'staging':
            url = 'stage.lixiaoskb.com'
        elif self.test == 'lxcrm':
            url = 'biz.lixiaoskb.com'
        else:
            print('传参错误')
            url = None
        return url

    def skb_userinfo(self, headers=None):  # 查询新SKB用户信息
        url = f'https://{user(self.test).skb_Host()}/api_skb/v1/user/userInfo'
        if headers == None:
            header = user(self.test).headers()
        else:
            header = headers
        response = requests.get(url, headers=header, verify=False)
        return response

    def headers(self, headers=None):  # headers环境配置
        if headers == None:
            header = {
                'app_token': user(self.test).user_key()["app_token"],
                'authorization': user(self.test).user_key()["Token"],
                'content-type': 'application/json',
                'crm_platform_type': user(self.test).user_key()["platform"]
            }
        else:
            header = headers
        return header

    # if __name__ == '__main__':
    #     print(user('test').headers())

    def visitor_HOST(self):  # 访客识别host
        if self.test == 'test':
            HOST = 'visitor-test.weiwenjia.com'
        elif self.test == 'staging':
            HOST = 'visitor-stage.weiwenjia.com'
        elif self.test == 'lxcrm':
            HOST = 'visitor.weiwenjia.com'
        else:
            print('传参错误')
            HOST = None
        return HOST

    def robot_headers(self):  # 机器人headers配置
        lxcrm_Headers = {
            'platform': 'IK',
            'usertoken': user(self.test).user_key()["token"],
            'Content-Type': 'application/json',
            'crmplatformtype': user(self.test).user_key()["platform"]
        }
        # test_Headers = {
        #     'platform': 'IK',
        #     'userToken': Token,
        #     'Content-Type': 'application/json',
        #     'CrmPlatformType': platform
        # }
        return lxcrm_Headers
        # if self.test == 'lxcrm':
        #     return lxcrm_Headers
        # else:
        #     return test_Headers

    def robot_Host(self):  # 机器人host
        if self.test == 'test':
            host = 'jiqiren-test.weiwenjia.com'
        elif self.test == 'staging':
            host = 'jiqiren-staging.weiwenjia.com'
        elif self.test == 'lxcrm':
            host = 'jiqiren.weiwenjia.com'
        else:
            print('传参错误')
            host = None
        return host


class configuration_file:  # 配置文件调用
    """
    environment:环境变量
    """

    def __init__(self, environment):
        self.test = environment
        self.user = user(environment)

    def url(self):  # 配置文件host
        if self.test == 'test':
            url = 'https://test.lixiaoskb.com/api_skb/v1/'
        elif self.test == 'staging':
            url = 'https://stage.lixiaoskb.com/api_skb/v1/'
        elif self.test == 'lxcrm':
            url = 'https://biz.lixiaoskb.com/api_skb/v1/'
        else:
            print('传参错误')
            url = None
        return url

    def conditionGroups(self): #高级搜索搜索条件
        path = 'companyDetail/conditionGroups?groupName=enterprise&category=advancedSearch'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(), verify=False)
        data = r.json()['data']
        return data

    def staticConfig(self):  # 来源（contactSource）站配置
        path = 'companyDetail/staticConfig?namespace=withLevels'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(), verify=False)
        data = r.json()['data']
        return data

    def staticConfig_recruitPlatformOption(self):  # 经营情况详情页筛选配置，recruitPlatformOption：招聘平台
        path = 'companyDetail/staticConfig?namespace=semPlatformOption,recruitPlatformOption,tenderOption,semTypeOption'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(), verify=False)
        data = r.json()['data']
        return data
    def staticConfig_IPR(self):  # 知识产权详情页筛选配置，templateSuppilerOption：建站方，trademarkTypeOption：商标类别
        path = 'companyDetail/staticConfig?namespace=trademarkTypeOption,templateSuppilerOption'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(), verify=False)
        data = r.json()['data']
        return data

    def shopCategory(self):  # 店铺分类（shopCategory）配置
        path = 'companyDetail/staticConfig?namespace=shopCategory'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers())
        data = r.json()['data']
        return data

    def conditionConfig(self):  # 高级搜索搜索条件（conditionConfig）配置
        path = 'companyDetail/conditionConfig?groupName=enterprise&category=advancedSearch'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(), verify=False).json()
        return r['data']

    def shopDivision(self):  # 店铺地区（shopDivision）配置
        path = 'companyDetail/staticConfig?namespace=shopDivision'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(), verify=False).json()
        return r['data']['shopDivision']
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


if __name__ == '__main__':
    import pprint
    from API_project.tools.install_Excel import install_Excel
    install_files = install_Excel(file_name="联系方式渠道配置", file_title_name="联系方式渠道配置")  # 实例化测试报告文件
    if install_files.read_sum() == 1 and install_files.read_one_value() is None:
        install_files.install(row=1, column=1, value='name')
        install_files.install(row=1, column=2, value='value')
        install_files.install(row=1, column=3, value='dbName')
    staticConfig = configuration_file('test').staticConfig()['contactSiteSourceMap']
    staticConfig_list = []
    for staticConfig_value in staticConfig:
        for i in staticConfig_value['sub']:
            # print(i)
            # break
            row_sum = install_files.read_sum() + 1
            install_files.install(row=row_sum, column=1, value=i['name'])
            install_files.install(row=row_sum, column=2, value=i['value'])
            install_files.install(row=row_sum, column=3, value=i['dbName'])
        staticConfig_list = staticConfig_list+staticConfig_value['sub']
        # for sub in staticConfig_value['sub']:
        #     staticConfig_list.append(sub)
    # for v in staticConfig_list:
    #     for key, value in v.items():
    #         print(key, value)
    #     break
    print(staticConfig_list)
    # print(configuration_file('test').staticConfig_recruitPlatformOption()['recruitPlatformOption'] )
