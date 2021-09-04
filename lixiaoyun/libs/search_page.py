from configs.BasePage import basepage
from configs.myDriver import Driver
from selenium.webdriver.common.action_chains import ActionChains
import time

class search_elment(basepage):
    def search_input_element(self):# 定位找企业结果页输入框
        return self.driver.find_element_by_css_selector('.el-input>input')
    def search_carte(self): # 定位找企业结果页搜一搜按钮
        return self.driver.find_element_by_css_selector('.search-company-btn>.to-search')
    def search_input_del_carte(self): # 定位找企业结果页输入框删除按钮
        return self.driver.find_elements_by_xpath(
        '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]')
    # search_input = driver.find_elements_by_xpath(
    #     '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/input')
    # search = driver.find_elements_by_xpath(
    #     '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div')  # 定位找企业结果页搜一搜按钮
    # search_input_del = driver.find_elements_by_xpath(
    #     '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]')  # 定位找企业结果页输入框删除按钮
    # if search_retu == False:
    #     for i in search_input:
    #         i.send_keys(search_text)
    #     for i in search:
    #         i.click()
    #     return ('搜索结束')
    # elif search_retu == True:
    #     if search_input_del != []:
    #         for i in search_input_del:
    #             i.click()
    #             time.sleep(1.5)
    #     for i in search_input:
    #         i.send_keys(search_text)
    #     for i in search:
    #         i.click()
    #     return ('搜索结束')
    # else:
    #     return ('账户错误')