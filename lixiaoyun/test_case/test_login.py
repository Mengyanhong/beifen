#执行用例
import os

from tools.yamlControl import get_yaml_data
from libs.login import login
# from libs.driver import driver
from configs.config import driver

# #1- 获取用例数据
# res = get_yaml_data('../data/login_case.yaml')[0]
# print(res)
# #2- 调用接口方法---获取相应数据
# respData = login(res["data"],res['company']).login()
# print(respData)
# #3- 断言
# if respData == res["resp"]["message"]:
#     print("---用例通过---")
#     driver.quit()
#
# else:
#     print("---用力失败---",respData,res["resp"]["message"])
#     driver.quit()

#1- 获取用例数据
# res = get_yaml_data('../data/login_case.yaml')[0]
# print(res)
# #2- 调用接口方法---获取相应数据
# respData = login(res[1],res[0]).login()
# print(respData)
# #3- 断言
# if respData == res[2]["message"]:
#     print("---用例通过---")
#     driver.quit()
#
# else:
#     print("---用例通过---",respData,res[2]["message"])
#     driver.quit()


# 引入框架 pytest
# py测试文件必须以test_开头（或者以_test结尾）
import pytest
class Testlogin:
    #测试方法
    @pytest.mark.parametrize('incompany,inBody,expData',get_yaml_data('../data/login_case.yaml'))#数据驱动方法

    def test_login(self,incompany,inBody,expData):
        #调用业务代码
        # print(incompany)
        loog_file = login(inData=inBody,company=incompany,mode=False)
        res = loog_file.login()
        # 断言
        # assert res == expData["message"]
        res_1 = loog_file.login_case()
        #断言
        assert res_1 == False
        # print("---用例通过---")
        # driver.quit()


if __name__ == '__main__':
    pytest.main(["test_login.py","-sq","--alluredir","../report/tmp"])# -s 打印输出,-sq简化打印
    os.system("allure serve ../report/temp")
    os.system("allure generate ../report/tmp -o ../report/temp --clean")
"""f   用例失败
   E   ERROR
   。  成功的
"""