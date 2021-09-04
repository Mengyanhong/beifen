print()
"""
接口名称：登录
类型：token机制/
用途：
    1- 自动化
    2- 获取token
"""
from configs.config import HOST
import requests
import hashlib
import pprint
def get_md5(psw):#等同于hashlib.md5('123456'.encode(encoding='utf-8')).hexdigest()
    """
    :param psw:
    :return: 返回md5加密的结果
    """
    md5 = hashlib.md5()
    md5.update(psw.encode("utf-8"))
    return md5.hexdigest()
# print(HOST)
# 封装登录类
class login:
    def login(self,inData,mode=False):#登录方法
        url = f"{HOST}/api/loginS" #f 格式化路径
        inData["password"] = get_md5(inData["password"]) #将加密后的结果付给字典
        payload = inData #引用传参
        """
        传参类型说明
        data----- 一般传表单格式
        json----- 传值为json格式
        files---- 文件上传类型
        params--- 参数为URL传参 ?a=1&b=2的形式
        """
        response = requests.post(url,json=payload) #发送请求
        # return response.text  #查看响应字符串类型
        if mode:
            return response.json()["token"]
        else:
            return response.json()  #返回字典类型
if __name__ == "__main__": #快捷键ctrl+j
    res = login().login({"username":"20154084","password":"123456"})
    pprint.pprint(res)
    # print(get_md5("123456"))

