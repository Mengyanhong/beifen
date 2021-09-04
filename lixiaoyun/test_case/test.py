
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lixiaoyun.configs.config import driver,ActionChains
from lixiaoyun.libs.login import login
from lixiaoyun.libs.Search import Switch_module

from lixiaoyun.tools.yamlControl import get_yaml_data
file = get_yaml_data('../data/login_case.yaml')[0]

import time
shift_crm_shift_num = 2 #定义转crm筛选选择项
# # coding = utf-8 from selenium import webdriver
driver.maximize_window()  # 最大化浏览器s
driver.implicitly_wait(5)  # 等待页面加载最长等待10秒

print('----------开始登录企业----------')
login_file = login({"account":"13162863099","password":"Ik123456"},'爱客+SKB高级数据+JQR+CRM') #初始化登录数据
login_file.login() #登录
login_switch = login_file.login_case() #判断登录账户是否正确

print('''----------开始进行模块切换----------''')
se_module = Switch_module().search(login_switch,file[1]['search'])  #进入找企业
search_input = driver.find_elements_by_xpath(
            '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/input') # 定位找企业结果页输入框
search = driver.find_elements_by_xpath(
            '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div')  # 定位找企业结果页搜一搜按钮
search_input_del = driver.find_elements_by_xpath(
             '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]')  # 定位找企业结果页输入框删除按钮
if se_module == 'error':  #判断账户正确性
    print('账户登录错误')
else:
    if se_module == False:  #执行找企业搜索
        for i in search_input:
            i.send_keys(file[1]['search'])
        for i in search:
            i.click()
        print('搜索'+file[1]['search'])
    elif se_module == True:
        print('搜索' + file[1]['search'])

"""执行鼠标滑动"""

tar = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]')
time.sleep(5)
driver.execute_script("arguments[0].scrollIntoView();", tar) #通过定位需要移动到的位置移动到可见的元素区


print('''---------开始进行转移情况筛选判断----------''')

shift_crm = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/span')  # 定位转移情况位置
ActionChains(driver).move_to_element(shift_crm).perform()  # 鼠标移动到定位位置之上
shift_crm_reminder = driver.find_element_by_xpath('/html/body/div[5]/div[1]')  # 获取转移情况悬浮内容
if shift_crm_reminder.text == '包含转移到crm的数据':  # 判断转移情况悬浮内容是否正确
    print('转移情况悬浮提示正确')
else:
    print('悬浮显示错误', shift_crm_reminder.text)
shift_crm.click()  # 点击转移情况按钮
time.sleep(2)
shift_crm_text = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/div/div[2]/div/div/div[1]').text  # 获取转移情况筛选项内容
shift_crm_text_list = shift_crm_text.replace('\n', ',').split(',')  # 将转移情况筛选项内容内的换行转换成','再通过‘,’将内容转换成列表
if shift_crm_text == '''全部
未转crm
已转crm''':
    print('转移情况筛选选择内容正确')
else:
    print('转移情况筛选选择内容错误\n', shift_crm_text)
shift_crm_shift = driver.find_element_by_xpath(
    f'/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/div/div[2]/div/div/div[1]/div/div[{shift_crm_shift_num}]/div')  # 定位转移筛选选择
shift_crm_shift.click()  # 执行转移筛选
time.sleep(2.5)
driver.refresh() #刷新页面
time.sleep(5)
tar_2 = driver.find_element_by_xpath('/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/span[1]')
driver.execute_script("arguments[0].scrollIntoView();", tar_2) #页面刷新后通过定位需要移动到的位置移动到可见的元素区
time.sleep(3.5)
shift_crm_shift_text = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/span/span/span').text  # 获取执行转移筛后筛选项选择的内容
if shift_crm_shift_text == shift_crm_text_list[shift_crm_shift_num - 1]:  # 判断转移后筛选项的内容是否符合选择
    print('筛选选择正确')
else:
    print('筛选项不符合筛选选择', shift_crm_shift_text, '!=', shift_crm_text_list[shift_crm_shift_num - 1], '\n')

print("""----------判断是否有新增线索权限和导入线索池权限----------""")
#判断转crm按钮内容
shift_crm_button = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/span/span')  # 获取转crm按钮位置
shift_crm_button_text = shift_crm_button.text
shift_crm_button.click()  # 点击转crm按钮
time.sleep(2)
caidan = driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/div').text  # 获取转crm菜单内容
caidan_list = caidan.split('\n')  # 通过空格将转crm菜单内容转换成表格
if shift_crm_button_text == '转crm':  # 判断转crm按钮是否正确
    if caidan_list == ['转移所选','转前500条']:
        print('该企业是中企账户\n',caidan_list)
    elif caidan_list == ['转移所选']:
        print('该企业不是中企账户\n',caidan_list)
    else:
        print('转crm选项内容错误\n',caidan_list)
else:
    print('转crm按钮选项名称错误', shift_crm_button_text)

#执行不选择内容时的转移操作
driver.find_element_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[2]/div[1]/span[1]/div/div[2]/div/div/div[1]/div/div[1]/div').click()  # 点击转crm菜单中的转移所选按钮
# div = driver.find_elements_by_xpath('/html/body/div[6]') #定位转移所选后的提示弹窗
div = driver.find_elements_by_css_selector('[role=alert]')
if div != []:
    for i in div:
        if i.get_attribute('role') == 'alert':  # 判断标签内是否有弹窗元素
            tanchuang_text = i.get_attribute('textContent')
            if tanchuang_text == '请至少选择1条线索':  # 判断弹窗文本是否正确
                print('弹窗提示正确', tanchuang_text)
                break
            else:
                tanchuang = False
                print('测试失败错误提示为', tanchuang_text)
        else:
            print([i.get_attribute('role') for i in div if i.get_attribute('role') in div])
else:
    print('测试失败弹窗未出现',div)
# driver.implicitly_wait(5)  # 等待页面加载最长等待10秒

print('''----------开始进行联系方式判断和详情页转线索操作----------''')
time.sleep(3)
leads_unShow_result = driver.find_elements_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/div/div/div/span[1]') # 判断结果列表是否有结果
leads_unShow = driver.find_elements_by_xpath(
    '/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div/div/div/span/label')  # 查找获取号码按钮
leads_unShow_Null = driver.find_elements_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[3]/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div/div/div')  # 查找联系方式内容
if leads_unShow_result != []:
    if leads_unShow != []: # 判断联系方式是否已查看
        print('联系方式未查看')
    elif leads_unShow_Null != []: # 判断联系方式是否有内容
        for i in leads_unShow_Null:
            if i.get_attribute('textContent') == '无联系方式':
                print("该企业无联系方式")
            else:
                print('该企业联系方式已查看', i.get_attribute('textContent'), '\t')
    else:
        print('无法获取联系方式')
    for i in leads_unShow_result: # 点击线索进入详情页
        i.click()
        time.sleep(2)
    leads_unshou_screen = driver.find_elements_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[5]/div/div/div[1]/div/div[1]/div/div[4]/div[2]/button')  # 获取详情页转线索按钮
    leads_unshou_screen_text = driver.find_elements_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[5]/div/div/div[1]/div/div[1]/div/div[4]/div[2]/div')  # 获取详情页转线索按钮
    if leads_unshou_screen != []:
        for i in leads_unshou_screen:
            i.click() # 点击详情页转线索按钮
    else:
        if leads_unshou_screen_text != []:
            for i in leads_unshou_screen_text:
                print('转移筛选出错，错误结果\n', i.text)
        else:
            print('详情页获取不到转线索情况')
    driver.implicitly_wait(30)  # 等待页面加载最长等待10秒
    div_succeed = driver.find_elements_by_css_selector('[role=alert]') #css通过键值进行定位
    if div_succeed != []:  # 判断是否获取到弹窗
        for i in div_succeed:  # 进入弹窗内容循环
            tanchuang_text = i.get_attribute('textContent')  # 获取循环文本
            if tanchuang_text == '线索转移成功':  # 判断弹窗文本是否正确
                print('弹窗提示正确', tanchuang_text)
            else:
                print('测试失败错误提示为', tanchuang_text)
    else:
        print('测试失败弹窗未出现', div_succeed)
else:
    print('搜索结果为空')
time.sleep(2)
driver.quit()  # 关闭浏览器
