from selenium.webdriver.common.action_chains import ActionChains  # 导入鼠标事件的方法
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Programs\Python\Python38\chromedriver_win32\chromedriver.exe')  # 定义webdriver路径
# # coding = utf-8 from selenium import webdriver
driver.maximize_window()  # 最大化浏览器
driver.get(
    "https://lxcrm-test.weiwenjia.com/soukebox/search?keyword=%E4%BF%A1%E6%81%AF")  # 访问登录页面
# driver.implicitly_wait(1)#等待页面加载最长等待10秒
driver.find_element_by_id("account").send_keys("13162863099")  # 输入账户
driver.find_element_by_id("password").send_keys("Ik123456")  # 输入密码
time.sleep(1.5)
driver.find_element_by_class_name("ant-btn-primary").click()  # 点击登录
# company = ['励销+skb高级数据版+crm+jqr','爱客+单skb','励销+单SKB','爱客+skb高级数据版+crm+jqr']
# company_name = company[0]
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
    time.sleep(2)
    list_site_Ac = driver.find_elements_by_xpath(
        "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/div/ul/li[1]/a")  # 获取二级菜单内容
    if list_site_Ac == []:
        print('获取不到二级菜单', list_site_Ac, '\n', '进入一级菜单找企业', '\t')
        list_site.click()  # 点击找企业
    else:
        driver.find_element_by_xpath(
            "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/div/ul/li[1]/a/span").click()  # 点击二级菜单找企业
        time.sleep(1)
        if driver.find_elements_by_xpath(
                '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/input') != []:
            driver.find_element_by_xpath(
                '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/input').send_keys(
                '郑州')  # 定位输入框输入搜索内容
            driver.find_element_by_xpath(
                '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[2]/button').click()  # 执行搜索
            print('获取二级菜单成功开始进入找企业', '\t')
    time.sleep(3)
    search = driver.find_element_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div')  # 定位搜一搜按钮
    search_input = driver.find_element_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/input')  # 定位输入框
    search_input_del = driver.find_elements_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]')  # 定位输入框删除按钮
    if search_input_del != []:
        search_input.clear()
    time.sleep(1)
    search_input.send_keys('上海')
    time.sleep(1)
    search.click()
    time.sleep(5)

'''---------开始进行转移情况筛选判断----------'''

shift_crm = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/span')  # 定位转移情况位置
ActionChains(driver).move_to_element(shift_crm).perform()  # 鼠标移动到定位位置之上
time.sleep(2)
shift_crm_reminder = driver.find_element_by_xpath('/html/body/div[5]/div[1]')  # 获取转移情况悬浮内容
if shift_crm_reminder.text == '可以筛选线索的转移状态':  # 判断转移情况悬浮内容是否正确
    print('转移情况悬浮提示正确')
else:
    print('悬浮显示错误', shift_crm_reminder.text)
shift_crm.click()  # 点击转移情况按钮
time.sleep(2)
shift_crm_text = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/div').text  # 获取转移情况筛选项内容
shift_crm_text_list = shift_crm_text.replace('\n', ',')  # 将转移情况筛选项内容内的空格转换成','
shift_crm_text_list = shift_crm_text_list.split(',')  # 通过转移情况筛选项内容内的,将内容转换成列表
shift_crm_shift_num = 2
if shift_crm_text == '''全部
未转线索
已转线索''':
    print('转移情况筛选选择内容正确\t', shift_crm_text, '\t')
else:
    print('转移情况筛选选择内容错误', shift_crm_text, '\t')
shift_crm_shift = driver.find_element_by_xpath(
    f'/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/div/div[2]/div/div/div[1]/div/div[{shift_crm_shift_num}]/div')  # 定位转移筛选选择
shift_crm_shift.click()  # 执行转移筛选
time.sleep(2)
shift_crm_shift_text = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/span/span').text  # 获取执行转移筛后筛选项选择的内容
if shift_crm_shift_text == shift_crm_text_list[int(shift_crm_shift_num) - 1]:  # 判断转移后筛选项的内容是否正确
    print('转换正确,', shift_crm_shift_text, '==', shift_crm_text_list[shift_crm_shift_num - 1], '\t')
else:
    print('筛选项显示错误', shift_crm_shift_text, '!=', shift_crm_text_list[shift_crm_shift_num - 1], '\t')
time.sleep(5)
# driver.refresh()

'''----------开始进行联系方式判断----------'''

time.sleep(5)
leads_unShow = driver.find_elements_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div/div/div/span/label')  # 查找获取号码按钮
if leads_unShow != []:  # 判断联系方式是否已查看
    print('联系方式未查看')
elif driver.find_elements_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/div/div/div') != []:  # 判断结果列表是否有结果
    leads_unShow_Null = driver.find_element_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div/div/div')  # 获取联系方式
    print('该企业联系方式已查看', leads_unShow_Null.text, '\t')
else:
    print('搜索结果为空')

"""判断是否有新增线索权限和导入线索池权限"""

shift_crm_button = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/span/span')  # 获取转crm按钮位置
if shift_crm_button.text == '转线索':  # 判断转crm按钮内容是否正确
    print('按钮选项名称正确')
else:
    print('按钮选项名称错误', shift_crm_button.text)
shift_crm_button.click()  # 点击转crm按钮
time.sleep(1)
caidan = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/div').text  # 获取转crm菜单内容
caidan_list = caidan.split('\n')  # 通过空格将转crm菜单内容转换成表格
print(caidan_list)
time.sleep(2)
driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/div/div[2]/div/div/div[1]/div/div[1]/div').click()  # 点击转crm菜单中的转移所选按钮
driver.implicitly_wait(5)#等待页面加载最长等待10秒
div = driver.find_elements_by_tag_name('div') #通过标签进行定位
tanchuang = False
for i in div:
    if i.get_attribute('role') == 'alert': #判断标签内是否有弹窗元素
        tanchuang_text = i.get_attribute('textContent')
        tanchuang = True
        if tanchuang_text == '请至少选择1条线索': #判断弹窗文本是否正确
            print('弹窗提示正确',tanchuang_text)
        else:
            print('测试失败错误提示为',tanchuang_text)
        break
    # else:
    #     print(i.get_attribute('role'))
print (tanchuang)
if tanchuang == False:
    print('测试失败弹窗未出现')

'''----------开始进入详情页并判断详情页转线索操作----------'''

lears = driver.find_elements_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[3]')  # 判断结果列表是否有结果
# print(lears)
if lears != []:
    driver.find_element_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/div/div/div/span[1]').click()  # 点击线索进入详情页
    time.sleep(2)
    driver.find_element_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[5]/div/div/div[1]/div/div[1]/div/div[4]/div[2]/button').click()  # 点击详情页转线索按钮
    driver.implicitly_wait(5)  # 等待页面加载最长等待10秒
    div = driver.find_elements_by_tag_name('p')  # 通过标签进行定位
    div1 = driver.find_elements_by_xpath('/html/body/div[8]')  # 定位弹窗内容/html/body/div[7]
    # div1 = driver.find_element_by_xpath('/ html / body / div[8]').text  # 定位弹窗内容
    # div1 = driver.find_element_by_xpath('/ html / body / div[8]').get_attribute('textContent') #定位弹窗内容
    #get_attribute()还有get_attribute("innerHTML")和get_attribute("outerHTML")方法

    print(div)
    print(div1)
    print(driver.find_elements_by_tag_name('p'))
    print(driver.find_element_by_xpath('/ html / body / div[7]').get_attribute('textContent'))
    # if div1.get_attribute('textContent') == '与线索中现有信息重复，新增线索失败':
    #     print(div1.get_attribute('textContent'),'测试通过')
    # else:
    #     print(div1.get_attribute('textContent'),'失败')
    # / html / body / div[6]/html/body/div[6]/p
    # for i in div:
    #     if i.get_attribute('role') == 'alert':  # 判断标签内是否有弹窗元素
    #         tanchuang_text = i.get_attribute('textContent')
    #         tanchuang = True
    #         if tanchuang_text == '请至少选择1条线索':  # 判断弹窗文本是否正确
    #             print('弹窗提示正确', tanchuang_text)
    #         else:
    #             print('测试失败错误提示为', tanchuang_text)
    #         break
    if div != []: #判断是否获取到弹窗
        tanchuang = False
        for i in div: #进入弹窗内容循环
            tanchuang_text = i.get_attribute('textContent') #获取循环文本
            if tanchuang_text == '与线索中现有信息重复，新增线索失败':  # 判断弹窗文本是否正确
                print('弹窗提示正确', tanchuang_text)
                tanchuang = True
            else:
                print('测试失败错误提示为', tanchuang_text)
        print(tanchuang)
        if tanchuang == False:
            print('测试失败弹窗未出现')
    else:
        print('测试失败弹窗未出现',div1)
    # # print(driver.find_element_by_css_selector('[role=alert]').text) #css通过键值进行定位
    # # print(driver.find_element_by_css_selector('body>div>p').text) #css通过标签层级进行定位
else:
    print('结果列表无数据')
time.sleep(5)
# driver.quit()  # 关闭浏览器
