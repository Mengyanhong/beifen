from selenium.webdriver.common.action_chains import ActionChains
import time
# import win32gui
import win32com.client
# from selenium.webdriver.common.keys import Keys
from configs.BasePage import basepage
from configs.myDriver import Driver
from selenium.webdriver.common.by import By
# import pypiwin32
class upload_files_page(basepage): #定位元素
    def __init__(self):
        super().__init__()
        self.url = "https://lxcrm-test.weiwenjia.com/soukebox/batch_search" #定义批量查企业界面的URL
    def search_carte(self):#定位找企业二级菜单
        return self.driver.find_element_by_xpath('//li[@id="menu-zhaoqiye"]/a/span[text()="找企业"]') #定位2级菜单
    def search_click_carte(self): #定位找企业入口
        return self.driver.find_element_by_xpath('//ul[@class="nav"]/li/a/span[text()="找企业"]')
    def batch_search_carte(self): #定位批量查企业按钮
        return self.driver.find_element_by_xpath('//div/div/span[text()="批量查企业"]')
    def upload_data_carte(self): #定位上传数据按钮，并判断定位是否为空
        return self.driver.find_elements_by_xpath(
                    '//div[@class="batch-search-title"]/span[@class="batch-right-operate"]/span')
    def upload_file_carte(self):#定位上传文件按钮
        return self.driver.find_element_by_xpath('//input[@class="upload-file"]')
    def Check_all(self): #定位开始查询按钮
        return self.driver.find_element_by_css_selector('button.el-button--primary>span')
    def affirm(self): #定位开始查询时提示弹窗确认按钮
        return self.driver.find_element_by_css_selector(
            '#app > div > div > div.popup-window > div > div > div > span > span.submit-btn')

class automation(upload_files_page): #执行动作
    def uploadfiles(self): #执行上传文件操作
        Driver.login() #登陆账户
        self.to_page(1,self.url) #等待1秒钟后直接访问批量找企业页面
        ActionChains(self.driver).move_to_element(self.search_carte()).perform()  # 鼠标移动到定位位置之上
        time.sleep(1)
        self.search_click_carte().click() #点击找企业
        time.sleep(2)
        firstwin = self.driver.current_window_handle  # 获取当前窗口
        self.batch_search_carte().click() #点击批量查企业
        time.sleep(2)
        allwin = self.driver.window_handles #获取所有窗口
        # 选择窗口
        for win in allwin:
            if win != firstwin:
                self.driver.switch_to.window(win) #切换到新的页面tab
                time.sleep(1)
                # self.driver.execute_script("window.scrollBy(800,0);")
                if self.upload_data_carte(): #判断上传数据按钮存在
                    self.upload_data_carte()[0].click() #点击上传数据按钮
                    time.sleep(1)
                    ActionChains(self.driver).click(self.upload_file_carte()).perform() #使用鼠标点击动作点击input型元素，选择文件按钮
                    time.sleep(1)
                    shell = win32com.client.Dispatch('WScript.Shell')
                    shell.SendKeys(r'C:\Users\admin\Desktop\20210426213631.xlsx')
                    shell.SendKeys("{ENTER}")
                    shell.SendKeys("{ENTER}")
                    # self.get_element_WebDriverWait(10,{By.CSS_SELECTOR,'button.el-button--primary'})
                    time.sleep(5)
                    ActionChains(self.driver).click(self.Check_all()).perform()  #点击开始查询按钮
                    # self.Check_all().click()
                    # time.sleep(2)
                    self.affirm().click() #点击开始查询提示的确认按钮
                    return ("上传成功")
                else:
                    return ("上传失败")
class  Transfer_the_filter_element(basepage): # 定位转移筛选元素
    # def __init__(self):
    #     pass
    #'''请输入筛选项名称，1转crm，2转机器人，3导出'''
    def transfer_element(self,transfer_value): # 选择转移操作
        return self.driver.find_element_by_css_selector(
            f'.option-left-btn #userDeInput:nth-child({transfer_value}) .text-wrapper')
    # '''请输入转移选项，1转移所选，2转前500，3转前1000,4转前2000'''
    def transfer_operation_value(self,transfer_value): # 转移选项选择内容
        return self.driver.find_element_by_css_selector(f'div:nth-child({transfer_value})>.general-item')
    # '''请输入扣点方式，1仅转移已查看，2扣除额度展开线索'''
    def transfer_deduct(self,deduct_value): # 转移选项扣点方式
        return self.driver.find_element_by_css_selector(
            f'.checkCont div:nth-child({deduct_value}) .el-radio__inner')
    #'''请输入操作方式，1取消，2确认'''
    def transfer_affirm(self,affirm_value):    # 转移弹窗确认/取消操作
        return self.driver.find_element_by_css_selector(f'.el-dialog__footer>span>button:nth-child({affirm_value})')
    #'''请输入筛选项名称，1转crm情况，2转机器人，3查看情况'''
    def filter_leads_ele(self,element_value): #定位转移筛选选项
        return self.driver.find_element_by_css_selector(
            f'.skb-filter-right-btn #userDeInput:nth-child({element_value}) .text-wrapper')
    # def filter_robot_ele(self): #定位转机器人情况
    #     return self.driver.find_element_by_css_selector(
    #         '.skb-filter-right-btn #userDeInput:nth-child(2) .text-wrapper')
    # def filter_check_ele(self): #定位查看情况
    #     return self.driver.find_element_by_css_selector(
    #         '.skb-filter-right-btn #userDeInput:nth-child(3) .text-wrapper')
    #筛选项选择内容
    #'''请输入筛选项内容，1全部，2未转，3已转'''
    def filter_leads_robot_content(self,Screening_value): # #定位转crm和转机器人筛选内容选项
        return self.driver.find_element_by_css_selector(f'div:nth-child({Screening_value})>.general-item')
    # 筛选项选择内容
    # '''请输入筛选项内容，1全部，2已查，3未查'''
    def filter_check_content(self,Screening_value): #定位查看情况筛选内容选项
        return self.driver.find_element_by_css_selector(f'div:nth-child({Screening_value})>.general-item')
class Gets_business_list_information_element(basepage): #获取企业列表内的元素
    def companyname(self): #获取企业名称列表元素
        return self.driver.find_elements_by_css_selector('td.el-table_1_column_3 span.name')
    def com_element(self):  # 获取企业列表全选按钮
        return self.driver.find_element_by_css_selector('tr>th span.el-checkbox__inner')

class Transfer_the_filter_operation(Transfer_the_filter_element,Gets_business_list_information_element):
    def transfer_operation(self): #创建转移操作动作
        time.sleep(5)
        self.filter_leads_ele(1).click() #选择筛选项,（转crm情况）
        self.filter_leads_robot_content(2).click() #选择筛选内容，（未转crm）
        time.sleep(5)
        companynames = [] #创建企业名称列表
        if self.companyname():  #判断企业名称元素列表不为空
            for company in self.companyname():
                com = company.get_attribute('textContent') #获取企业名称元素列表内的企业名称值
                companynames.append(com.strip()) #将获取的企业名称添加到企业名称列表
        if companynames:
            self.com_element().click() #点击企业列表内的全选按钮
            self.transfer_element(1).click() #选择转移操作，（转crm）
            self.transfer_operation_value(1).click()  #选择转移选项，（转移所选）
            self.transfer_deduct(2).click() #选择扣点方式，（扣除额度展开线索再转移）
            self.transfer_affirm(2).click() #选择执行操作，（确认）
            return companynames
        else:
            return ('文件上传后匹配数据为空')
if __name__ == '__main__':
    AUTO = automation().uploadfiles()
    if AUTO == "上传成功":
        transfer = Transfer_the_filter_operation().transfer_operation()
        print(transfer)
    else:
        print(AUTO)
    time.sleep(2)
    Driver.get_driver().quit()
