from Configs.uiconfig import driver, ActionChains
import time
import win32gui
import win32com.client
from selenium.webdriver.common.keys import Keys
# import pypiwin32
class Login:
    def __init__(self, account, password):
        self.account = account
        self.password = password
    def logins(self):
        driver.implicitly_wait(5)
        driver.get(
            'https://uc-staging.weiwenjia.com/web/index.html?appToken=f6620ff6729345c8b6101174e695d0ab#/lxyunLogin')
        driver.find_element_by_id('account').send_keys(self.account)
        driver.find_element_by_xpath('//span/input[@id="password"]').send_keys(self.password)
        driver.find_element_by_xpath('//button[@class="ant-btn ant-btn-primary"]').click()
    @classmethod
    def upload_file(cls): #上传文件
        shift_crm = driver.find_element_by_xpath('//li[@id="menu-zhaoqiye"]/a/span[text()="找企业"]') #定位2级菜单
        ActionChains(driver).move_to_element(shift_crm).perform()  # 鼠标移动到定位位置之上
        time.sleep(1)
        driver.find_element_by_xpath('//ul[@class="nav"]/li/a/span[text()="找企业"]').click() #进入找企业首页
        driver.find_element_by_xpath('//div/div/span[text()="批量查企业"]').click() #进入批量查企业
        allwindows = driver.window_handles  # 所有的窗口
        firstwin = driver.current_window_handle  # 当前的窗体  即第一个页面窗口
        # 选择窗口
        for win in allwindows:
            if win != firstwin:
                driver.switch_to.window(win) #进入窗口页面
                driver.maximize_window() #最大化窗口
                time.sleep(2)
                print(driver.title)
                # print(driver.url)
                # driver.execute_script("window.scrollBy(800,0);") #执行页面滑动
                operate = driver.find_elements_by_xpath(
                    '//div[@class="batch-search-title"]/span[@class="batch-right-operate"]/span') #定位切换的窗口内是否有需要的元素
                if operate: #如果有
                    operate[0].click() #点击需要的元素
                    print('切换窗口成功')
                    break
                else:
                    print("切换窗口失败")
        time.sleep(2)
        sh = driver.find_element_by_xpath('//input[@class="upload-file"]') #定位选择文件按钮
        # ActionChains(driver).move_to_element(sh).perform()
        ActionChains(driver).click(sh).perform() #模拟鼠标点击事件点击选择文件按钮
        time.sleep(2)
        shell = win32com.client.Dispatch('WScript.Shell') #模拟win系统操作上传弹窗
        shell.SendKeys(r'C:\Users\admin\Desktop\20210426213631.xlsx') #使用win系统在鼠标位置输入内容
        shell.SendKeys("{ENTER}") #使用win系统执行回车命令
        shell.SendKeys("{ENTER}") #使用win系统执行回车命令
        time.sleep(3)
        driver.find_element_by_css_selector('button.el-button--primary').click() #点击开始查询
        affirm = driver.find_element_by_css_selector(
            '#app > div > div > div.popup-window > div > div > div > span > span.submit-btn') #定位确定查询
        if affirm:
            affirm.click() #点击确定查询
class Sizer:
    @classmethod
    def Sizer(cls): #筛选器
        shaixuanxiang = int(input('请输入筛选项名称，1转crm情况，2转机器人，3查看情况'))
        shaixuanneirong = int(input('请输入筛选项内容，1全部，2未转/已查，3已转/未查'))
        driver.find_element_by_css_selector(f'.skb-filter-right-btn #userDeInput:nth-child({shaixuanxiang}) .text-wrapper').click()
        driver.find_element_by_css_selector(f'div:nth-child({shaixuanneirong})>.general-item').click()
    @classmethod
    def zhuanyiy1(self):
        shaixuanxiang = int(input('请输入筛选项名称，1转crm，2转机器人，3导出'))
        shaixuanneirong = int(input('请输入筛选项内容，1转移所选，2转前500，1000,2000'))
        koudian = int(input('请输入筛选项内容，1仅转移已查看，2扣除额度展开线索'))
        companyname = driver.find_elements_by_css_selector('td.el-table_1_column_3 span.name') #获取企业名称元素
        companynames = [] #创建企业列表
        if companyname:
            for com in companyname:
                comp = com.get_attribute('textContent') #获取企业名称搜索
                companynames.append(comp.strip()) #将企业名称添加到企业列表
        driver.find_element_by_css_selector('tr>th span.el-checkbox__inner').click() #点击企业全选按钮
        driver.find_element_by_css_selector(f'.option-left-btn #userDeInput:nth-child({shaixuanxiang}) .text-wrapper').click() #选择转移操作
        driver.find_element_by_css_selector(f'div:nth-child({shaixuanneirong})>.general-item').click() #执行转移
        driver.find_element_by_css_selector(f'.checkCont div:nth-child({koudian}) .el-radio__inner').click() #选择扣点方式
        driver.find_element_by_css_selector('.el-dialog__footer>span>button:nth-child(2)').click() #确认转移




    # @classmethod
    # def shell(cls):
    #     pass
        # driver.implicitly_wait(5)
        # driver.maximize_window()
        # time.sleep(5)
        # driver.find_element_by_xpath('div[@class="upload-btn"]/.').click()
        # driver.find_element_by_xpath('//div[@class="el-dialog mainDialog"]/div/div/div[@class="upload-btn"]/.').click()
        # driver.find_element_by_css_selector('div > div.upload-btn').click()
        # shell = win32com.client.Dispatch('WScript.Shell')
        # shell.SendKeys(r'C:\Users\admin\Desktop\上传数据\地图获客_20210426204910.xlsx' + '\n')

        # driver.get(url)
        # time.sleep(5)
        # sh = pypiwin32.

        # driver.switch_to.frame(driver.find_element_by_xpath('//html[@class="app js no-touch no-android chrome no-firefox no-iemobile no-ie no-ie10 no-ie11 no-ios"]'))
        # driver.find_element_by_css_selector('div.batch-search-box > span').click()
        # ActionChains(driver).move_to_element(sh).perform().click()


if __name__ == '__main__':
    Login('13523390917', 'Ik123456').logins()
    Login.upload_file()
    Sizer.Sizer()
    Sizer.zhuanyiy1()
    time.sleep(2)
    # driver.quit()
