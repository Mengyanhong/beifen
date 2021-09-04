# -*- coding: utf-8 -*-
# @Time    : 2021/8/3—18:43
# @Author  : 孟艳红
# @File    : user_info.py 用户变量

class user: #用户信息
    def __init__(self, host='test'): #初始化环境变量
        self.host = host

    def headers(self): #headers环境配置
        if self.host == 'test':
            token = 'Token token=b792810fccc3ab092d476927049d4643'
            crm_platform_type = 'ikcrm'
        elif self.host == 'staging':
            token = 'Token token=17b1bc476fd501ebe8fdb01b37797a24'
            crm_platform_type = 'lixiaoyun'
        elif self.host == 'lxcrm':
            token = 'Token token=66dbf0159bdbdbb95f853740a002fc6c'
            crm_platform_type = 'ikcrm'
        else:
            print('传参错误')
            token = None
            crm_platform_type = None
        Headers = {
            'Authorization': token,
            'crm_platform_type': crm_platform_type,
            'Accept':'application/json',
        }
        return  Headers

    def HOST(self): #访客识别域名
        if self.host == 'test':
            HOST = 'https://visitor-test.weiwenjia.com'
        elif self.host == 'staging':
            HOST = 'https://visitor-stage.weiwenjia.com'
        elif self.host == 'lxcrm':
            HOST = 'https://visitor.weiwenjia.com'
        else:
            print('传参错误')
            HOST = None
        return  HOST
if __name__ == '__main__':
    print(user().HOST())