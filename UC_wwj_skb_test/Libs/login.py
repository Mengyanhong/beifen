# from UC_wwj_skb_test.Configs.uiconfig import driver, ActionChains
import time
import win32gui
import win32com.client
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 导入鼠标事件的方法
driver = webdriver.Edge(r'C:\Users\dell\PycharmProjects\workbook\venv\Scripts\msedgedriver.exe')

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
        driver.find_element_by_class_name('navbar-brand')

    @classmethod
    def l(cls):
        shift_crm = driver.find_element_by_xpath('//li[@id="menu-zhaoqiye"]/a/span[text()="找企业"]') #定位2级菜单
        ActionChains(driver).move_to_element(shift_crm).perform()  # 鼠标移动到定位位置之上
        time.sleep(3)
        driver.find_element_by_xpath('//ul[@class="nav"]/li/a/span[text()="找企业"]').click() #进入找企业首页
        driver.find_element_by_xpath('//div/div/span[text()="批量查企业"]').click() #进入批量查企业
        firstwin = driver.current_window_handle  # 当前的窗体  即第一个页面窗口
        allwindows = driver.window_handles  # 所有的窗口
        # 选择窗口
        for win in allwindows:
            if win != firstwin:
                driver.switch_to.window(win)
                # time.sleep(2)
                driver.execute_script("window.scrollBy(800,0);")
                fff = driver.find_elements_by_xpath(
                    '//div[@class="batch-search-title"]/span[@class="batch-right-operate"]/span')
                if fff:
                    fff[0].click()
                    driver.maximize_window()
                    time.sleep(1)
                    sh = driver.find_element_by_xpath('//input[@class="upload-file"]')
                    # ActionChains(driver).move_to_element(sh).perform()
                    ActionChains(driver).click(sh).perform()
                    time.sleep(1)
                    shell = win32com.client.Dispatch('WScript.Shell')
                    shell.SendKeys(r'C:\Users\admin\Desktop\20210426213631.xlsx')
                    shell.SendKeys("{ENTER}")
                    shell.SendKeys("{ENTER}")
                    time.sleep(3)
                    driver.find_element_by_css_selector('button.el-button--primary').click()
                    driver.find_element_by_css_selector(
                        '#app > div > div > div.popup-window > div > div > div > span > span.submit-btn').click()
                    print('成功')
                    break
                else:
                    print("失败")

    @classmethod
    def shell(cls):
        pass
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
    Login.l()
    time.sleep(2)
    # driver.quit()
