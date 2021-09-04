#执行用例
import os

from tools.yamlControl import get_yaml_data
from libs.login import login

#1- 获取用例数据
res = get_yaml_data('../data/logincase.yaml')
print(res)
#2- 调用接口方法---获取相应数据
respData = login().login(res["data"],False)
print(respData)
#3- 断言
if respData["message"] == res["resp"]["message"]:
    print("---用例通过---")
else:
    print("---用力失败---",respData["message"],res["resp"]["message"])

#引入框架 pytest
#py测试文件必须以test_开头（或者以_test结尾）
import pytest
class Testlogin:
    #测试方法
    @pytest.mark.parametrize('inBody,expData',get_yaml_data('../data/logincase.yaml'))#数据驱动方法
    def test_login(self,inBody,expData):
        #调用业务代码
        res = login().login(inBody,False)
        #断言
        assert res["message"] == expData["message"]


if __name__ == '__main__':
    pytest.main(["test_login.py","-s","--alluredir","../report/tmp"])# -s 打印输出,-sq简化打印
    # os.system("allure serve ../report/temp")
    os.system("allure serve ../report/tmp")
"""f   用例失败
   E   ERROR
   。  成功的
"""