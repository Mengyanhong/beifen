# -*- coding: utf-8 -*-
# @Time    : 2021/8/3—18:49
# @Author  : 孟艳红
# @File    : Upload_File.py
import requests
from Configs.user_info import user
from Tools.ExcelControl import Excel_Files
# host = 'test' #设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
class Upload:
    def __init__(self,host):
        self.User = user(host)
    def upload_site_img(self,files_name,token=None):
        # print(self.User.HOST())
        if token != None:
            header = {
                'ucServerToken':'3ecc50224cf24081a4d7148d33f31214',
                'thirdPlatform':'300.cn',
                'code':'gf-user-test-002',
                'sign':'5a0719f93b80f0939c6b95914765d25c'
            }
            url = f'{self.User.HOST()}/api_vi/v1/external/visitor_identify/upload_site_img'
        else:
            header = self.User.headers()
            url = f'{self.User.HOST()}/api_vi/v1/visitor_identify/upload_site_img'
        file = {'uploadFile':open(f'D:\\Users\\admin\\上传数据\\访客识别数据上传\\{files_name}', 'rb')}
        response = requests.post(url=url,headers=header ,files=file)
        return response.json()
if __name__ == '__main__':
    Excel = Excel_Files().open_case(Sizer_value=['站点接口-添加图片'])
    print(type(Excel[-2][0]))
    print(Excel[-2][0])
    upload = Upload("test")
    up = upload.upload_site_img(files_name=Excel[-2][0],token=1)

    print(up)
