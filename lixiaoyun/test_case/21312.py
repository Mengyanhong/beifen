from selenium.webdriver.common.action_chains import ActionChains  # 导入鼠标事件的方法
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()  # 定义webdriver路径
# # coding = utf-8 from selenium import webdriver
driver.maximize_window()  # 最大化浏览器
driver.implicitly_wait(10)  # 等待页面加载最长等待10秒
driver.get(
    "https://uc.weiwenjia.com/web/index.html?appToken=a14cc8b00f84e64b438af540390531e4&registered_way=normal_source&redirectUri=https://lxcrm.weiwenjia.com#/lxyunLogin")  # 访问登录页面
# driver.implicitly_wait(1)#等待页面加载最长等待10秒
driver.find_element_by_id("account").send_keys("16621006750")  # 输入账户
driver.find_element_by_id("password").send_keys("Shanghai123456")  # 输入密码
driver.find_element_by_class_name("ant-btn-primary").click()  # 点击登录
results = True  # 统计登陆结果
# WebDriverWait(driver,3,0.5).until(EC.visibility_of_element_located((By.CLASS_NAME,'customer-brand'))) #隐式等待
# if company_name not in driver.find_element_by_class_name('customer-brand').text: #判断登陆的企业是否正确
#     driver.find_element_by_id('newer_tour_lead_1').click() #若登陆的企业不正确点击设置按钮
#     time.sleep(2)
#     driver.find_element_by_class_name('caret').click() #点击用户按钮
#     user_name_Switch = driver.find_element_by_class_name('helper-hover') #定位切换企业的悬浮位置
#     ActionChains(driver).move_to_element(user_name_Switch).perform()  # 鼠标移动到切换企业之上
#     time.sleep(2)
#     Switch_name = driver.find_element_by_class_name('witch-org-ul')  # 获取当前用户的所有企业
#     if company_name in Switch_name.text:   # 判断当前用户是否拥有需要登录的企业
#         driver.find_element_by_link_text(company_name).click() # 若当前用户拥有需要登录的企业则点击企业名称进行切换
#         time.sleep(5)
#         if company_name not in driver.find_element_by_class_name('customer-brand').text:  # 判断切换的企业是否正确
#             print('企业切换失败开始重新登陆')
#             driver.find_element_by_class_name('user_name').click()  # 若切换的企业不正确点击用户按钮
#             driver.find_element_by_class_name('sign_out').click()  # 若切换的企业不正确点击退出登录按钮
#             time.sleep(3)
#             driver.find_element_by_id("account").send_keys("13162863099")  # 重新输入账户
#             driver.find_element_by_id("password").send_keys("Ik123456")  # 重新输入密码
#             driver.find_element_by_class_name("ant-btn-primary").click()  # 重新点击登录
#             time.sleep(3)
#             if company_name in driver.find_element_by_class_name('customer-brand').text:  # 若重新登陆的企业正确
#                 driver.save_screenshot(r"D:\桌面文件\app bug图\Pythonbug截图\企业名称页面.png")
#                 results = True #返回登陆结果
#                 print('企业重新登陆成功')
#             else:
#                 results = False #返回登陆结果
#                 print('企业重新登陆失败')
#         else:
#             results = True #返回登陆结果
#             print('企业切换成功')
#     else:
#         driver.save_screenshot(r"D:\桌面文件\app bug图\Pythonbug截图\企业名称页面.png") # 若当前用户没有需要登录的企业保存屏幕截图
#         results = False #返回登陆结果
#         print('此账户没有这个企业')
# else:
#     results = True #返回登陆结果
#     print('企业登陆成功')

'''----------开始进行模块切换----------'''

if results == True:  # 判断登陆结果
    WebDriverWait(driver, 3, 0.5).until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/section/section/section/aside/section/section/nav/ul/li[2]/a')))  # 隐式等待
    list_site = driver.find_element_by_xpath(
        "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/a")  # 定位悬浮位置
    ActionChains(driver).move_to_element(list_site).perform()  # 鼠标移动到定位位置之上
    # time.sleep(2)
    list_site_Ac = driver.find_elements_by_xpath(
        "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/div/ul/li[1]/a")  # 获取二级菜单内容
    if list_site_Ac == []:
        print('获取不到二级菜单', list_site_Ac, '\n', '进入一级菜单找企业', '\t')
        list_site.click()  # 点击找企业
    else:
        driver.find_element_by_xpath(
            "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/div/ul/li[1]/a/span").click()  # 点击二级菜单找企业
        # time.sleep(1)
        if driver.find_elements_by_xpath(
                '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/input') != []:
            driver.find_element_by_xpath(
                '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/input').send_keys(
                '郑州')  # 定位输入框输入搜索内容
            driver.find_element_by_xpath(
                '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[2]/button').click()  # 执行搜索
            print('获取二级菜单成功开始进入找企业', '\t')
    # time.sleep(3)
    search = driver.find_element_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div')  # 定位搜一搜按钮
    search_input = driver.find_element_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/input')  # 定位输入框
    search_input_del = driver.find_elements_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]')  # 定位输入框删除按钮
    if search_input_del != []:
        search_input.clear()
    # time.sleep(1)
    search_input.send_keys('上海')
    # time.sleep(1)
    search.click()
    # time.sleep(5)
time.sleep(5)

"""----------执行鼠标滑动----------"""
target = driver.find_element_by_xpath("//*[contains(text(),'已选条件')]")
driver.execute_script("arguments[0].scrollIntoView();", target)
# tar = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]')
# # target2=driver.find_element_by_css_selector('[class="row"]:nth-child(4) [class="panel-heading"]')
# # driver.execute_script(tar)
# driver.execute_script("arguments[0].scrollIntoView();", tar)
# time.sleep(2)
#
# scroll = 'document.documentElement.scrollTop=800'
# driver.execute_script(scroll)



# document.get
# a= 'var a=document.getElementsByClassName("scroll")[0].scrollHeight' # 获取滚动条高度
# document.getElementsByClassName("scroll")[0].scrollWidth # 获取横向滚动条宽度
# # document.getElementsByClassName("scroll")[0].scrollLeft=xxx # 控制横向滚动条位置

# js="var action=document.documentElement.scrollTop=10000"  #document.documentElement的去调用scrollTop.后面的数值是滚动条距离顶部的距离
# driver.execute_script(js) #执行js脚本

# print(driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"))
# # driver.switch_to("iframe")

# js="window.scrollTo(500,500)" #js的滚动写法，后面的0.0代表x轴和y轴
# driver.execute_script(js) #js的滚动写法，后面的0.0代表x轴和y轴


# js= "var revise = document.getElementsByClassName('skb-result-wrapper')[0]"
# driver.execute_script(js)

# JavascriptExecutor executor = (JavascriptExecutor) driver;
# executor.executeScript("arguments[0].scrollTop=1000",element);

# ActionChains(driver).move_to_element("skb-result-wrapper").perform()

# from selenium.webdriver.common.keys import Keys
# driver.find_element_by_xpath("/html/body/section/section/section/div[2]/div/div").send_keys(Keys.TAB)


# time.sleep(3)
# mon = driver.find_element_by_class_name('skb-result-wrapper')
# mon = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div')
# ActionChains(driver).drag_and_drop_by_offset(mon,0,200).perform()
# target = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/span/span')
# driver.execute_script("arguments[0].scrollIntoView();", target)#拖动到可见的元素去
# self._current_browser().execute_script("arguments[0].focus();", target)
# js="var q=document.getElementById('id').scrollTop=100"
# # driver.execute_script(js)
# ActionChains(driver).click_and_hold(mon).move_by_offset(0,100).release().perform()
# js="var q=document.documentElement.scrollTop=800"
# driver.execute_script(js)


