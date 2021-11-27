# -*- coding: utf-8 -*-
# @Time    : 2021/8/5—18:26
# @Author  : 孟艳红
# @File    : Test_Config_org_sites.py

from Visitors_identify.Tools.ExcelControl import Excel_Files
from Visitors_identify.Configs.Upload_File import Upload
from Visitors_identify.Configs.Pymysql import to_pymysql
from Visitors_identify.Libs.config_org_sites import site_config
import random
host = 'staging' #设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
Upload = Upload(host)
site_config = site_config(host)
import pytest,os
# class Test_site_config:
#     # @pytest.mark.parametrize('inBody,expData,Sizer_name_value',Excel_Files().open_case(Sizer_value=['站点接口-站点地址检验','站点接口-站点地址和其它企业相同']))#数据驱动方法
#     #
#     # def test_org_sites(self,inBody,expData,Sizer_name_value):
#     #     pymysql = to_pymysql(host).pymysql()
#     #     cursor = pymysql.cursor()
#     #     site_sum = site_config.org_sites_list()
#     #     #调用业务代码
#     #     if site_sum is not None:
#     #         if len(site_sum) < 5:
#     #             respData = site_config.org_sites(inData=inBody)
#     #             assert respData["error_code"] == expData["error_code"]
#     #             assert respData["message"] == expData["message"]
#     #         else:
#     #             cursor.execute(f"delete  from site_visitors where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from site_visitor_sessions where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from site_visitor_session_records where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from site_visitor_identify where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from online_customer_msg_info where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from org_sites where oid = {site_sum[0]['oid']} and id != 256")
#     #             pymysql.commit()
#     #             respData = site_config.org_sites(inData=inBody)
#     #             assert respData["error_code"] == expData["error_code"]
#     #             assert respData["message"] == expData["message"]
#     #     else:
#     #         respData = site_config.org_sites(inData=inBody)
#     #         assert respData["error_code"] == expData["error_code"]
#     #         assert respData["message"] == expData["message"]
#     #     cursor.close()
#     #     pymysql.close()
#
#     @pytest.mark.parametrize('inBody,expData,Sizer_name_value',
#                              Excel_Files().open_case(Sizer_value=['站点接口-站点名称检验','站点接口-站点地址检验', '站点接口-站点地址和其它企业相同','站点接口-站点地址和站点名称都和其它企业相同']))  # 数据驱动方法
#     def test_org_sites_image(self, inBody, expData, Sizer_name_value):
#         pymysql = to_pymysql(host).pymysql()
#         cursor = pymysql.cursor()
#         site_sum = site_config.org_sites_list()
#         # 调用业务代码
#         # Excel = Excel_Files().open_case(Sizer_value=['站点接口-添加图片'])
#         # Excel_sum = random.randint(0, len(Excel)-1)
#         respData_image = Upload.upload_site_img(files_name='占用100.jpg')
#         if respData_image['data'] == {}:
#             respData_image_value = None
#         else:
#             respData_image_value = respData_image['data']['ossKey']
#         # if respData_image["error_code"] != Excel[Excel_sum][1]["error_code"]:
#         #     assert respData_image["error_code"] == Excel[Excel_sum][1]["error_code"]
#         if site_sum is not None:
#             if len(site_sum) < 5:
#                 respData = site_config.org_sites(inData=inBody, ossId=respData_image_value)
#                 assert respData["error_code"] == expData["error_code"]
#                 assert respData["message"] == expData["message"]
#             else:
#                 cursor.execute(
#                     f"delete  from site_visitors where site_id in (select id from org_sites where oid = {site_sum[0]['oid']} and id != 1010)")
#                 pymysql.commit()
#                 cursor.execute(
#                     f"delete  from site_visitor_sessions where site_id in (select id from org_sites where oid = {site_sum[0]['oid']} and id != 1010)")
#                 pymysql.commit()
#                 cursor.execute(
#                     f"delete  from site_visitor_session_records where site_id in (select id from org_sites where oid = {site_sum[0]['oid']} and id != 1010)")
#                 pymysql.commit()
#                 cursor.execute(
#                     f"delete  from site_visitor_identify where site_id in (select id from org_sites where oid = {site_sum[0]['oid']} and id != 1010)")
#                 pymysql.commit()
#                 cursor.execute(
#                     f"delete  from online_customer_msg_info where site_id in (select id from org_sites where oid = {site_sum[0]['oid']} and id != 1010)")
#                 pymysql.commit()
#                 cursor.execute(
#                     f"delete  from org_sites where oid = {site_sum[0]['oid']} and id != 1010")
#                 pymysql.commit()
#                 respData = site_config.org_sites(inData=inBody, ossId=respData_image_value)
#                 assert respData["error_code"] == expData["error_code"]
#                 assert respData["message"] == expData["message"]
#         else:
#             respData = site_config.org_sites(inData=inBody, ossId=respData_image_value)
#             assert respData["error_code"] == expData["error_code"]
#             assert respData["message"] == expData["message"]
#         cursor.close()
#         pymysql.close()

class Test_sites_update:
#     # @pytest.mark.parametrize('inBody,expData,Sizer_name_value',
#     #                          Excel_Files().open_case(Sizer_value=['站点接口-站点地址检验', '站点接口-站点地址和其它企业相同']))  # 数据驱动方法
#     # def test_org_sites_update(self, inBody, expData,Sizer_name_value):
#     #     pymysql = to_pymysql(host).pymysql()
#     #     cursor = pymysql.cursor()
#     #     site_sum = site_config.org_sites_list()
#     #     if site_sum != None and site_sum != {}:
#     #         upda = site_sum[0]['id']
#     #     else:
#     #         upda = None
#     #     # 调用业务代码
#     #     print(site_sum)
#     #     if site_sum is not None and site_sum != {}:
#     #         if len(site_sum) < 5:
#     #             respData = site_config.org_sites(inData=inBody,updata=upda)
#     #             assert respData["error_code"] == expData["error_code"]
#     #             assert respData["message"] == expData["message"]
#     #         else:
#     #             cursor.execute(
#     #                 f"delete  from site_visitors where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from site_visitor_sessions where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from site_visitor_session_records where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from site_visitor_identify where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from online_customer_msg_info where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
#     #             pymysql.commit()
#     #             cursor.execute(
#     #                 f"delete  from org_sites where oid = {site_sum[0]['oid']} and id != 256")
#     #             pymysql.commit()
#     #             respData = site_config.org_sites(inData=inBody,updata=upda)
#     #             assert respData["error_code"] == expData["error_code"]
#     #             assert respData["message"] == expData["message"]
#     #     else:
#     #         respData = site_config.org_sites(inData=inBody,updata=upda)
#     #         assert respData["error_code"] == expData["error_code"]
#     #         assert respData["message"] == expData["message"]
#     #     cursor.close()
#     #     pymysql.close()

    @pytest.mark.parametrize('inBody,expData,Sizer_name_value',
                             Excel_Files().open_case(Sizer_value=['站点接口-站点名称检验','站点接口-站点地址检验', '站点接口-站点地址和其它企业相同','站点接口-站点地址和站点名称都和其它企业相同']))  # 数据驱动方法
    def test_org_sites_update_image(self, inBody, expData,Sizer_name_value):
        pymysql = to_pymysql(host).pymysql()
        cursor = pymysql.cursor()
        site_sum = site_config.org_sites_list()
        if site_sum != None and site_sum != {}:
            upda = site_sum[0]['id']
        else:
            upda = None
            assert site_sum != None
        # 调用业务代码
        # Excel = Excel_Files().open_case(Sizer_value=['站点接口-添加图片'])
        # Excel_sum = random.randint(0,5)
        respData_image = Upload.upload_site_img(files_name='占用100.jpg')
        if respData_image['data'] == {}:
            respData_image_value = None
        else:
            respData_image_value = respData_image['data']['ossKey']
        # if respData_image["error_code"] != Excel[Excel_sum][1]["error_code"]:
        #     assert respData_image["error_code"] == Excel[Excel_sum][1]["error_code"]
        if site_sum is not None and site_sum != {}:
            if len(site_sum) < 5:
                respData = site_config.org_sites(inData=inBody,updata=upda,ossId=respData_image_value)
                print(respData)
                assert respData["error_code"] == expData["error_code"]
                assert respData["message"] == expData["message"]
            else:
                cursor.execute(
                    f"delete  from site_visitors where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
                pymysql.commit()
                cursor.execute(
                    f"delete  from site_visitor_sessions where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
                pymysql.commit()
                cursor.execute(
                    f"delete  from site_visitor_session_records where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
                pymysql.commit()
                cursor.execute(
                    f"delete  from site_visitor_identify where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
                pymysql.commit()
                cursor.execute(
                    f"delete  from online_customer_msg_info where site_id in (select id from org_sites where oid = {site_sum[0]['oid']})")
                pymysql.commit()
                cursor.execute(
                    f"delete  from org_sites where oid = {site_sum[0]['oid']} and id != 256")
                pymysql.commit()
                respData = site_config.org_sites(inData=inBody,updata=upda,ossId=respData_image_value)
                assert respData["error_code"] == expData["error_code"]
                assert respData["message"] == expData["message"]
        else:
            respData = site_config.org_sites(inData=inBody,updata=upda,ossId=respData_image_value)
            assert respData["error_code"] == expData["error_code"]
            assert respData["message"] == expData["message"]
        cursor.close()
        pymysql.close()


if __name__ == '__main__':
    pytest.main(["Test_Config_org_sites.py", "-sq", "--alluredir", "../report/tmp"])  # -s 打印输出,-sq简化打印
    # os.system("allure serve ../report/temp")
    os.system("allure serve ../report/tmp")
"""f   用例失败
   E   ERROR
   。  成功的
"""