# @Time : 2021/9/29 10:01
# @Author : 孟艳红
# @File : user_config.py
class User_Config:  # 用户信息
    def __init__(self, environment):
        self.test = environment

    def user_key(self):  # headers环境配置
        if self.test == 'test':
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            Token_value = "fdc7cd52a1808e344b490b9457bb70e3"
            platform = 'lixiaoyun'
            gatewayId = None
        elif self.test == 'staging':
            app_token = 'f6620ff6729345c8b6101174e695d0ab'
            Token_value = 'b329f23fc5b2d0aaefb384cef8170c99'
            platform = 'lixiaoyun'
            gatewayId = None
        elif self.test == 'lxcrm':
            app_token = 'a14cc8b00f84e64b438af540390531e4'
            Token_value = '18033bf7b969d9b12ef830c66c1f2464'
            platform = 'lixiaoyun'
            gatewayId = "9203"
        else:
            print('传参错误')
            app_token = None
            Token_value = None
            platform = None
            gatewayId = None
        return {'app_token': app_token, 'Token': Token_value, 'platform': platform,'gatewayId':gatewayId}

if __name__ == '__main__':
    print(User_Config('test').user_key()["Token"])
