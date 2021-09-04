# -*- coding: utf-8 -*-

import requests, json
import urllib3
urllib3.disable_warnings()

class user: #用户信息
    def __init__(self, test):
        self.test = test
    def headers(self): #headers环境配置
        if self.test == 'test':
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            token = "fdc7cd52a1808e344b490b9457bb70e3"
        elif self.test == 'staging':
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            token = 'b329f23fc5b2d0aaefb384cef8170c99'
        elif self.test == 'lxcrm':
            app_token = 'a14cc8b00f84e64b438af540390531e4'
            token = '66dbf0159bdbdbb95f853740a002fc6c'
        else:
            print('传参错误')
            app_token = None
            token = None
        self.Headers = {
            'app_token': app_token,
            'Authorization': f'Token token={token}',
            'Content-Type': 'application/json',
            'crm_platform_type': 'lixiaoyun'
        }
        return  self.Headers



class configuration_file:#配置文件调用
    """
    environment:环境变量
    """
    def __init__(self,environment):
        self.test = environment
        self.user = user(environment)
    def url(self):
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
        path='companyDetail/conditionGroups?groupName=enterprise&category=advancedSearch'
        r=requests.get(configuration_file(self.test).url()+path,headers=self.user.headers(),verify=False)
        data=r.json()['data']
        return data
    def staticConfig(self): #来源（contactSource）站配置
        path='companyDetail/staticConfig?namespace=withLevels'
        r=requests.get(configuration_file(self.test).url()+path,headers=self.user.headers(),verify=False)
        data=r.json()['data']
        return data
    def shopCategory(self): #店铺分类（shopCategory）配置
        path='companyDetail/staticConfig?namespace=shopCategory'
        r=requests.get(configuration_file(self.test).url()+path,headers=self.user.headers())
        data=r.json()['data']
        return data
    def shopDivision(self): #店铺地区（shopDivision）配置
        path='companyDetail/staticConfig?namespace=shopDivision'
        r=requests.get(configuration_file(self.test).url()+path,headers=self.user.headers()).json()
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
