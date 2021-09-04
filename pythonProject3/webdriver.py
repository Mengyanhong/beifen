from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains #导入鼠标事件的方法
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
driver = webdriver.Chrome(r'D:\Users\自动化项目\webdriverpackage\chromedriver.exe')#定义webdriver路径
# # coding = utf-8 from selenium import webdriver
driver.maximize_window()#最大化浏览器
driver.get("https://uc-test.weiwenjia.com/web/index.html?appToken=f6620ff6729345c8b6101174e695d0ab#/lxyunLogin") #访问登录页面
# driver.implicitly_wait(1)#等待页面加载最长等待10秒
driver.find_element_by_id("account").send_keys("13162863099") #输入账户
driver.find_element_by_id("password").send_keys("Ik123456") #输入密码
time.sleep(1.5)
driver.find_element_by_class_name("ant-btn-primary").click() #点击登录
# company = ['励销+skb高级数据版+crm+jqr','爱客+单skb','励销+单SKB','爱客+skb高级数据版+crm+jqr']
# company_name = company[0]
results = True #统计登陆结果
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
if results == True: #判断登陆结果
    # print('开始获取二级菜单')
    WebDriverWait(driver, 3, 0.5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/section/section/section/aside/section/section/nav/ul/li[2]/a')))  # 隐式等待
    list_site = driver.find_element_by_xpath(
        "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/a")  # 定位悬浮位置
    ActionChains(driver).move_to_element(list_site).perform()  # 鼠标移动到定位位置之上
    time.sleep(2)
    list_site_Ac = driver.find_elements_by_xpath(
            "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/div/ul/li[1]/a") # 获取二级菜单内容
    if list_site_Ac == []:
        print('获取不到二级菜单',list_site_Ac,'\n','进入找企业')
        list_site.click()
    else:
        time.sleep(2)
        driver.find_element_by_xpath(
            "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/div/ul/li[1]/a/span").click()
        # list_site_Acs
        WebDriverWait(driver, 1, 0.5).until(EC.visibility_of_element_located(
            (By.XPATH, '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[2]/button')))  # 隐式等待
        driver.find_element_by_xpath(
            '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/input').send_keys(
            '郑州')  # 定位输入框输入搜索内容
        driver.find_element_by_xpath(
            '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[2]/button').click()  # 执行搜索
        print('获取二级菜单成功开始进入找企业')
# WebDriverWait(driver, 3, 0.5).until(EC.visibility_of_element_located(
#             (By.XPATH, '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div')))  # 隐式等待
time.sleep(3)
search = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div')
search_input = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/input')
search_input_del = driver.find_elements_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]')
if search_input_del != []:
    search_input.clear()
time.sleep(1)
search_input.send_keys('郑州轻工业大学学术交流中心')
time.sleep(1)
search.click()
time.sleep(5)
# shift_crm = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/span/span')
# ActionChains(driver).move_to_element(shift_crm).perform()  # 鼠标移动到定位位置之上
# time.sleep(3)
# shift_crm_reminder = driver.find_element_by_xpath('/html/body/div[6]')
# # print(shift_crm_reminder)
# print(shift_crm_reminder.text)
# if shift_crm_reminder.text == '可以筛选线索的转移':
#     print('悬浮提示正确')
# else:
#     print('悬浮显示错误',shift_crm_reminder.text)
# shift_crm.click()
# time.sleep(2)
# shift_crm_text = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/div').text

# shift_crm_text_list = shift_crm_text.replace('\n',',')
# shift_crm_text_list = shift_crm_text_list.split(',')
# print(shift_crm_text_list)
# shift_crm_shift_num = 2
# if shift_crm_text == '''全部
# 未转线索
# 已转线索''':
#     print('筛选项正确')
#     # print(shift_crm_text)
# else:
#     print('筛选项错误')
    # print(shift_crm_text)
# shift_crm_shift = driver.find_element_by_xpath(f'/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/div/div[2]/div/div/div[1]/div/div[{shift_crm_shift_num}]/div')
# shift_crm_shift.click()
# shift_crm_shift_text = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/span/span').text
# if shift_crm_shift_text == shift_crm_text_list[shift_crm_shift_num-1]:
#     print('转换正确')
#     print(shift_crm_shift_text,shift_crm_text_list[shift_crm_shift_num-1])
# else:
#     print('筛选项显示错误')
#     print(shift_crm_shift_text,shift_crm_text_list[shift_crm_shift_num-1])
# driver.refresh()
# time.sleep(5)
# leads_unShow = driver.find_elements_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div/div/div/span/label')
# leads_unShow_Null = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div/div/div')
# if leads_unShow != []:
#     print('联系方式未查看')
# else:
#     print('该企业联系方式已查看',leads_unShow_Null.text,leads_unShow)
shift_crm_button = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/span/span')
if shift_crm_button.text == '转线索':
    print('选项正确')
shift_crm_button.click()
"""判断是否有新增线索权限和导入线索池权限"""

time.sleep(2)
# caidan = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/div').text
# caidan_list = caidan.split('\n')
# print(caidan_list,caidan)
# shift_crm_button_click
# driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/div/div[2]/div/div/div[1]/div/div[1]/div').click()
# WebDriverWait(driver, 5, 0.5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]')))  # 隐式等待
tanchuang = driver.find_elements_by_xpath('/html/body/div[5]')
if tanchuang != []:
    tanchuang_text = driver.find_element_by_xpath('/html/body/div[5]').text
    print(tanchuang_text)
    if tanchuang_text == '请至少选择1条线索':
        print('未选择线索，测试通过')
    else:
        print('提示错误')
else:
    print('测试失败，未弹出提示')


# driver.quit() #关闭浏览器



# # 获取aaa.html的绝对路径
# file_path = os.path.abspath('aaa.html')
# print
# file_path
# driver.get(file_path)
# # 点击Link1链接（弹出下拉列表）
# driver.find_element_by_xpath("html/body/div[1]/div/div/a").click()
# # 在下拉列表中找到如下xpath路径对应元素
# menu = driver.find_element_by_xpath("//*[@id='dropdown1']/li[1]/a")
# time.sleep(3)
# # 鼠标定位到该元素上
# webdriver.ActionChains(driver).move_to_element(menu).perform()
# time.sleep(3)
# driver.quit()
