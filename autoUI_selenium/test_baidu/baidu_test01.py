# from selenium import webdriver
# import time
# driver = webdriver.Chrome(r'D:\Users\自动化项目\webdriverpackage\chromedriver.exe')#定义webdriver路径
# driver.get("https://www.baidu.com/")#访问百度
# driver.find_element_by_class_name('s_ipt').send_keys('driver')#定位输入框并输入webdriver
# driver.find_element_by_id('su').click()#点击百度一下执行搜索
# time.sleep(2)
# res = driver.find_element_by_id('1')
# if 'driver - 百度翻译' in res.text:
#     print('pass')
#     #       print('本周数据为0，上周数据为None')
#     # print(res)
# else:
#     print('fail')
#     print(res)
# time.sleep(5)
# driver.quit()
from test_baidu import example1
example1.fun2()