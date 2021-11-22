from API_project.Configs.user_config import User_Config
import requests, json, urllib3

urllib3.disable_warnings()

class user:  # 用户信息
    def __init__(self, environment):
        self.test = environment
        self.user_key = User_Config(environment).user_key()

    def user_key(self):
        return self.user_key

    def headers(self):  # headers环境配置
        if self.test == 'test':
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            Token = "Token token=b792810fccc3ab092d476927049d4643"
            platform = 'ikcrm'
        elif self.test == 'staging':
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            Token = 'Token token=b329f23fc5b2d0aaefb384cef8170c99'
            platform = 'lixiaoyun'
        elif self.test == 'lxcrm':
            app_token = 'a14cc8b00f84e64b438af540390531e4'
            Token = 'Token token=18033bf7b969d9b12ef830c66c1f2464'
            platform = 'lixiaoyun'
        else:
            print('传参错误')
            app_token = None
            Token = None
            platform = None
        Headers = {
            'app_token': app_token,
            'Authorization': Token,
            'Content-Type': 'application/json',
            'crm_platform_type': platform
        }
        return Headers

    def skb_Host(self):  #新搜客宝host
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

    def biz_url(self):  #老搜客宝host
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

    def skb_userinfo(self,headers=None):  #查询新SKB用户信息
        url = f'https://{user(self.test).skb_Host()}/api_skb/v1/user/userInfo'
        if headers == None:
            header = user(self.test).shop_headers()
        else:
            header = headers
        response = requests.get(url,headers=header,verify=False)
        return response

    def shop_headers(self):  # headers环境配置
        Headers = {
            'app_token': self.user_key["app_token"],
            'authorization': f'''Token token={self.user_key["Token"]}''',
            'content-type': 'application/json',
            'crm_platform_type': self.user_key["platform"]
        }
        return Headers

    def visitor_HOST(self): #访客识别host
        if self.test == 'test':
            HOST = 'visitor-test.weiwenjia.com'
        elif self.test == 'staging':
            HOST = 'visitor-stage.weiwenjia.com'
        elif self.test == 'lxcrm':
            HOST = 'visitor.weiwenjia.com'
        else:
            print('传参错误')
            HOST = None
        return  HOST

    def robot_headers(self): #机器人headers配置
        lxcrm_Headers = {
            'platform': 'IK',
            'usertoken': self.user_key["Token"],
            'Content-Type': 'application/json',
            'crmplatformtype': self.user_key["platform"]
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

    def robot_Host(self):  #机器人host
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
if __name__ == '__main__':
    print(user('lxcrm').shop_headers())


class configuration_file:  #配置文件调用
    """
    environment:环境变量
    """
    def __init__(self, environment):
        self.test = environment
        self.user = user(environment)

    def url(self):  #配置文件host
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

    def conditionGroups(self):
        path = 'companyDetail/conditionGroups?groupName=enterprise&category=advancedSearch'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(), verify=False)
        data = r.json()['data']
        return data

    def staticConfig(self):  # 来源（contactSource）站配置
        path = 'companyDetail/staticConfig?namespace=withLevels'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(), verify=False)
        data = r.json()['data']
        return data
    def staticConfig_recruitPlatformOption(self):  # 详情页筛选配置，recruitPlatformOption：招聘平台
        path = 'companyDetail/staticConfig?namespace=semPlatformOption,recruitPlatformOption,tenderOption,semTypeOption'
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
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers() , verify=False).json()
        return r['data']

    def shopDivision(self):  # 店铺地区（shopDivision）配置
        path = 'companyDetail/staticConfig?namespace=shopDivision'
        r = requests.get(configuration_file(self.test).url() + path, headers=self.user.headers(),verify=False).json()
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
    print(len(configuration_file('test').conditionConfig()['recruitPlatform']['cv']['options']))