# -*- coding: utf-8 -*-
# @Time    : 2021/7/30—15:59
# @Author  : 孟艳红
# @File    : write_case.py

class user: #用户信息
    def __init__(self, test):
        self.test = test
    def headers(self): #headers环境配置
        if self.test == 'test':
            token = '5c3bf587deaff969b8ca07627bc40bba'
        elif self.test == 'staging':
            token = 'b329f23fc5b2d0aaefb384cef8170c99'
        elif self.test == 'lxcrm':
            token = '66dbf0159bdbdbb95f853740a002fc6c'
        else:
            print('传参错误')
            token = None
        Headers = {
            'Authorization': f'Token token={token}',
            'crm_platform_type': 'lixiaoyun'
        }
        return  Headers
    def host(self):
        if self.test == 'test':
            HOST = 'https://visitor-test.weiwenjia.com'
        elif self.test == 'staging':
            HOST = 'https://visitor-stage.weiwenjia.com'
        elif self.test == 'lxcrm':
            HOST = 'https://visitor.weiwenjia.com'
        else:
            print('传参错误')
            HOST = None
        return  HOST
