#执行用例
import os
from UC_wwj_skb_test.tools.yamlControl import get_yaml_data
from UC_wwj_skb_test.Configs.config import HOST
from UC_wwj_skb_test.Libs.batch_search import upload_batch_search_file
from UC_wwj_skb_test.Libs.industry_label import industry_labels
DEV_HOST = HOST.search_fin_staging()
# #1- 获取用例数据
# file = get_yaml_data('../Data/staging_se_files.yaml')
# print(file)
#
# #2- 调用接口方法---获取相应数据
# respData = upload_batch_search_file(file[0][0],DEV_HOST,file[0][0]['oss_key']).search_file()
# print(respData)
# #3- 断言
# # if respData["error_code"] == file[0][1]["error_code"]:
# #     print("---用例通过---")
# # else:
# #     print("---用力失败---",respData["error_code"],file[0][1]["error_code"])

# 引入框架 pytest
# py测试文件必须以test_开头（或者以_test结尾）
# from API_project.Configs.Config_Info import Config_info
import pytest
class Test_search_fin:
    #测试方法
    @pytest.mark.parametrize('inBody,expData',get_yaml_data('../Data/staging_se_fin.yaml'))#数据驱动方法

    def test_searchfin(self,inBody,expData):
        #调用业务代码
        respData = upload_batch_search_file(inBody,DEV_HOST,).search_fin(inBody['oss_key'])
        #断言
        assert respData["error_code"] == expData["error_code"]
        assert respData["message"] == expData["message"]
class Test_search_files:
    @pytest.mark.parametrize('filesBody,filesData', get_yaml_data('../Data/staging_se_files.yaml'))  # 数据驱动方法
    def test_searchfiles(self,filesBody,filesData):
        res = upload_batch_search_file(filesBody,DEV_HOST,).search_files(filesBody['file_name'])
        assert res["error_code"] == filesData["error_code"]
        assert res["message"] == filesData["message"]

class Test_industry_tag:
    @pytest.mark.parametrize('filesBody,filesData', get_yaml_data('../Data/staging_industry_tags.yaml'))  # 数据驱动方法
    def test_industry_tag(self,filesBody,filesData):
        rers=industry_labels(filesBody,DEV_HOST,).industry_tags()
        assert rers["error_code"] == filesData["error_code"]
if __name__ == '__main__':
    pytest.main(["Test_batch_search.py::Test_industry_tag::test_industry_tag","-sq","--alluredir","../report/tem"])# -s 打印输出,-sq简化打印
    # os.system("allure serve ../report/temp")
    os.system("allure generate ../report/tem -o ../report/temp --clean")
"""f   用例失败
   E   ERROR
   。  成功的
"""