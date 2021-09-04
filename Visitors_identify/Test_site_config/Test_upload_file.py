# -*- coding: utf-8 -*-
# @Time    : 2021/8/5—13:29
# @Author  : 孟艳红
# @File    : Test_upload_file.py

from Tools.ExcelControl import Excel_Files
from Configs.Upload_File import Upload
host = 'test' #设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
Upload = Upload(host)
import pytest,os
class Test_upload:
    #测试方法
    @pytest.mark.parametrize('inBody,expData,Sizer_name_value',Excel_Files().open_case(Sizer_value=['站点接口-添加图片','站点接口-添加图片错误校验']))#数据驱动方法

    def test_upload(self,inBody,expData,Sizer_name_value):
        #调用业务代码
        print(inBody,'\n',expData['error_code'])
        respData = Upload.upload_site_img(files_name=inBody,token=1)
        print(respData)
        #断言
        assert respData["error_code"] == expData["error_code"]
        assert respData["message"] == expData["message"]
if __name__ == '__main__':
    pytest.main(["Test_upload_file.py", "-sq", "--alluredir", "../report/tmp"])  # -s 打印输出,-sq简化打印
    # os.system("allure serve ../report/temp")
    os.system("allure serve ../report/tmp")
"""f   用例失败
   E   ERROR
   。  成功的
"""