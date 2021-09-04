# -*- coding: utf-8 -*-
# @Time    : 2021/8/5—14:52
# @Author  : 孟艳红
# @File    : config_org_sites.py
from Tools.ExcelControl import Excel_Files
from Configs.Upload_File import Upload
host = 'staging' #设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境


import requests,random,json
from Configs.user_info import user
from Configs.Pymysql import to_pymysql


from Tools.ExcelControl import Excel_Files
# host = 'test' #设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
class site_config:
    def __init__(self, host,token=None):
        self.User = user(host)
        self.token = token
    def org_sites_list(self):
        if self.token != None:
                header = {
                    'ucServerToken': '3ecc50224cf24081a4d7148d33f31214',
                    'thirdPlatform': '300.cn',
                    'code': 'gf-user-test-002',
                    'sign': '5a0719f93b80f0939c6b95914765d25c'
                }
                url = f'{self.User.HOST()}/api_vi/v1/external/visitor_identify/org_sites'
        else:
            header = self.User.headers()
            url = f'{self.User.HOST()}/api_vi/v1/visitor_identify/org_sites'
        response = requests.get(url=url, headers=header).json()
        if response['data'] != []:
            return response['data']
        else:
            return None
        # return response


    def org_sites(self, inData=None, ossId=None,updata = None,project=None):
        # inData = json.loads(inData)
        # print(self.User.HOST())
        if self.token != None:
            header = {
                'ucServerToken':'3ecc50224cf24081a4d7148d33f31214',
                'thirdPlatform':'300.cn',
                'code':'gf-user-test-002',
                'sign':'5a0719f93b80f0939c6b95914765d25c'
            }
            url = f'{self.User.HOST()}/api_vi/v1/external/visitor_identify/org_sites'
        else:
            url = f'{self.User.HOST()}/api_vi/v1/visitor_identify/org_sites'
            header = self.User.headers()
        if ossId == None:
            if updata==None:
                if project==None:
                    inData.pop('installSuccess')
                    payload = inData
                else:
                    payload = inData
                print('请求传参', payload)
                response = requests.post(url=url, headers=header, json=payload)

            else:
                if project==None:
                    inData.pop('installSuccess')
                    inData.update({"id" : updata,"ossId": None})
                    payload = inData
                else:
                    inData.update({"id": updata,"ossId": None})
                    payload = inData
                print('请求传参', payload)
                response = requests.put(url=url, headers=header, json=payload)
        else:
            # payload = {
            #     "siteHome": f"http://wiki.weiwenjia.com/{random.randint(1000, 2000)}/",
            #     "siteName": f"测试图片{random.randint(1000, 2000)}",
            #     "enableWebChat": "true",
            #     "ossId": f"{ossId}",
            #     "installSuccess": "true"
            # }
            if updata == None:
                if project==None:
                    inData.pop('installSuccess')
                    inData.update({"ossId": f"{ossId}"})
                    payload = inData
                else:
                    inData.update({"ossId": f"{ossId}"})
                    payload = inData
                print('请求传参', payload)
                response = requests.post(url=url, headers=header, json=payload)
            else:
                if project==None:
                    inData.pop('installSuccess')
                    inData.update({"id":updata,"ossId": f"{ossId}"})
                    payload = inData
                else:
                    inData.update({"id": updata, "ossId": f"{ossId}"})
                    payload = inData
                print('请求传参',payload)
                response = requests.put(url=url, headers=header, json=payload)

        return response.json()

if __name__ == '__main__':
    Excel = Excel_Files().open_case(Sizer_value='站点接口-站点地址检验')
    site_sum = site_config(host).org_sites_list()
    # site_sum = site_config
    print(site_sum.request.headers)
    print(site_sum.request.url)
    print(site_sum.json())
    # if site_sum != None:
    #     upda = site_sum[random.randint(0, len(site_sum) - 1)]['id']
    # else:
    #     upda = site_sum
    # print(upda)
    # respData = site_config.org_sites(inData=Excel[0][0], updata=upda)
    # # a=requests.get(url='')
    # # a.request.body
    # print(respData.request.body)

    # cursor.execute(
    #     "delete  from org_sites where oid = 5505101 and id = 216")
    # cursor.execute(
    #     "delete  from org_sites where oid = 5505101 and id = 217")
    # for i in range(len(Excel)):
    #     site_sum = site_config.org_sites_list()
    #
    #     # if site_sum != None:
    #     #     upda = site_sum[random.randint(0,len(site_sum)-1)]['id']
    #     # else:
    #     #     upda = site_sum
    #     # Excel = Excel_Files().open_case(Sizer_value=['站点接口-添加图片'])
    #     # Excel_sum = random.randint(0,len(Excel))
    #     # respData_image = Upload(host).upload_site_img(files_name=Excel[Excel_sum][0])
    #     # if respData_image['data'] == {}:
    #     #     respData_image_value = None
    #     # else:
    #     #     respData_image_value = respData_image['data']['ossId']
    #     # if respData_image["error_code"] != Excel[Excel_sum][1]["error_code"]:
    #     #     assert respData_image["error_code"] == Excel[Excel_sum][1]["error_code"]
    #     # print(site_sum)
    #     # print(site_sum[0]['oid'])
    #     # print(len(site_sum))
    #     if site_sum is not None:
    #         if len(site_sum) < 5 :
    #             up = site_config.org_sites(inData=Excel[i][0])
    #             print(up, '\n', Excel[i][1])
    #             assert up['error_code'] == Excel[i][1]['error_code']
    #     # print(site_config.org_sites(inData=Excel[i][0]))
    #         else:
    #             pymysql = to_pymysql(host).pymysql()
    #             cursor = pymysql.cursor()
    #             cursor.execute(f"delete  from site_visitors where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
    #             pymysql.commit()
    #             cursor.execute(
    #                 f"delete  from site_visitor_sessions where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
    #             pymysql.commit()
    #             cursor.execute(
    #                 f"delete  from site_visitor_session_records where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
    #             pymysql.commit()
    #             cursor.execute(
    #                 f"delete  from site_visitor_identify where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
    #             pymysql.commit()
    #             cursor.execute(
    #                 f"delete  from online_customer_msg_info where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
    #             pymysql.commit()
    #             cursor.execute(
    #                 f"delete  from org_sites where oid = {site_sum[0]['oid']}")
    #             pymysql.commit()
    #             cursor.close()
    #             pymysql.close()
    #             up = site_config.org_sites(inData=Excel[i][0])
    #             print(up, '\n', Excel[i][1])
    # #             assert up['error_code'] == Excel[i][1]['error_code']
    #     else:
    #         up = site_config.org_sites(inData=Excel[i][0])
    #         print(up, '\n', Excel[i][1])
    #         assert up['error_code'] == Excel[i][1]['error_code']


