# print()
# """
# 接口名称：登录
# 类型：token机制/
# 用途：
#     1- 自动化
#     2- 获取token
# """
# from configs.config import HOST
# import requests
# import hashlib
# import pprint
# def get_md5(psw):#等同于hashlib.md5('123456'.encode(encoding='utf-8')).hexdigest()
#     """
#     :param psw:
#     :return: 返回md5加密的结果
#     """
#     md5 = hashlib.md5()
#     md5.update(psw.encode("utf-8"))
#     return md5.hexdigest()
# # print(HOST)
# # 封装登录类
# class login:
#     def login(self,inData,mode=False):#登录方法
#         url = f"{HOST}/api/loginS" #f 格式化路径
#         inData["password"] = get_md5(inData["password"]) #将加密后的结果付给字典
#         payload = inData #引用传参
#         """
#         传参类型说明
#         data----- 一般传表单格式
#         json----- 传值为json格式
#         files---- 文件上传类型
#         params--- 参数为URL传参 ?a=1&b=2的形式
#         """
#         response = requests.post(url,json=payload) #发送请求
#         # return response.text  #查看响应字符串类型
#         if mode:
#             return response.json()["token"]
#         else:
#             return response.json()  #返回字典类型
# if __name__ == "__main__": #快捷键ctrl+j
#     res = login().login({"username":"20154084","password":"123456"})
#     pprint.pprint(res)
#     # print(get_md5("123456"))
# # coding = utf-8 from selenium import webdriver
from configs.config import TEST_HOST,driver,ActionChains
from tools.yamlControl import get_yaml_data
import pprint
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
 # 定义webdriver路径
# driver.maximize_window()  # 最大化浏览器
# driver.implicitly_wait(1)#等待页面加载最长等待10秒
class login:
    def __init__(self,inData,company,mode=False):
        self.inData = inData
        self.company = company
        self.mode = mode
    def login(self):
        driver.implicitly_wait(3)
        driver.get(f'{TEST_HOST}')  # 访问登录页面
        login_click = driver.find_elements_by_class_name("ant-btn-primary")
        if login_click != []:
            driver.find_element_by_id("account").send_keys(self.inData['account'])  # 输入账户
            driver.find_element_by_id("password").send_keys(self.inData['password'])  # 输入密码
            for i in login_click:
                i.click() # 点击登录
            return driver.find_element_by_class_name('customer-brand').text  # 返回企业名称
        else:
            if driver.find_elements_by_class_name('customer-brand') != []: # 登陆成功返回企业名称
                for i in driver.find_elements_by_class_name('customer-brand'):
                    return i.text
            else:
                return '登录网址出错'
    def login_case(self):
        driver.implicitly_wait(5)
        driver.maximize_window()  # 最大化浏览器s
        # WebDriverWait(driver, 3, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'customer-brand')))  # 隐式等待
        if self.company != driver.find_element_by_class_name('customer-brand').text: #判断登陆的企业是否正确
            driver.find_element_by_id('newer_tour_lead_1').click() #若登陆的企业不正确点击设置按钮
            driver.find_element_by_class_name('caret').click() #点击用户按钮
            user_name_Switch = driver.find_element_by_class_name('helper-hover') #定位切换企业的悬浮位置
            ActionChains(driver).move_to_element(user_name_Switch).perform()  # 鼠标移动到切换企业之上
            time.sleep(3)
            Switch_name = driver.find_element_by_class_name('witch-org-ul')  # 获取当前用户的所有企业
            if self.company in Switch_name.text:   # 判断当前用户是否拥有需要登录的企业
                driver.find_element_by_link_text(self.company).click() # 若当前用户拥有需要登录的企业则点击企业名称进行切换
                if self.company not in driver.find_element_by_class_name('customer-brand').text:  # 判断切换的企业是否正确
                    driver.find_element_by_class_name('user_name').click()  # 若切换的企业不正确点击用户按钮
                    driver.find_element_by_class_name('sign_out').click()  # 若切换的企业不正确点击退出登录按钮
                    driver.find_element_by_id("account").send_keys(self.inData['account'])  # 重新输入账户
                    driver.find_element_by_id("password").send_keys(self.inData['password'])  # 重新输入密码
                    driver.find_element_by_class_name("ant-btn-primary").click()  # 重新点击登录
                    if self.company in driver.find_element_by_class_name('customer-brand').text:  # 若重新登陆的企业正确
                        driver.save_screenshot(r"D:\桌面文件\app bug图\Pythonbug截图\企业名称页面.png")
                        print ('企业重新登陆成功'+self.company)
                        return True
                    else:
                        print ('企业重新登陆失败'+self.company)
                        return False
                else:
                    print ('企业切换成功'+self.company)
                    return True
            else:
                driver.save_screenshot(r"D:\桌面文件\app bug图\Pythonbug截图\企业名称页面.png") # 若当前用户没有需要登录的企业保存屏幕截图
                print ('此账户没有这个企业'+self.company)
                return False
        else:
            print('企业登陆成功'+self.company)
            return True

if __name__ == "__main__": #快捷键ctrl+j
    file = get_yaml_data('../data/login_case.yaml')[0]
    print(file)
    loog_file = login(file[1],file[0])
    res = loog_file.login()
    print(res)
    res_1 = loog_file.login_case()
    print(res_1)
    time.sleep(3)
    driver.quit()
    # pprint.pprint(res_1)
