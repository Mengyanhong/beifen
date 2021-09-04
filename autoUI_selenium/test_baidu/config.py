# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains #导入鼠标事件的方法
# import time
# driver = webdriver.Chrome() # 等同于chromedriver = r"C:\Users\admin\AppData\Local\Programs\Python\Python38\Scripts\msedgedriver.exe"
# driver.maximize_window()#最大化浏览器
# # driver.implicitly_wait(1)#等待页面加载最长等待10秒
# driver.get("https://uc-test.weiwenjia.com/web/index.html?appToken=f6620ff6729345c8b6101174e695d0ab#/lxyunLogin") #访问登录页面
# class case:
#     def case(self):
#         list_site = driver.find_element_by_xpath("/html/body/section/section/section/aside/section/section/nav/ul/li[2]/a")#定位悬浮位置
#         ActionChains(driver).move_to_element(list_site).perform() #鼠标移动到定位位置之上
#         time.sleep(3)
#         driver.find_element_by_xpath("/html/body/section/section/section/aside/section/section/nav/ul/li[2]/div/ul/li[1]/a").click()#选择悬浮内容并执行点击命令
#         time.sleep(2)
#         driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/input').send_keys('郑州')#定位输入框输入搜索内容
#         driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[2]/button').click()#执行搜索
# results = True
# if results = shannghai1:
#     print(1)