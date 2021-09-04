from configs.BasePage import basepage
from configs.myDriver import Driver
from libs.search_page import search_elment
from selenium.webdriver.common.action_chains import ActionChains
import time

class Gets_business_list_information_element(basepage): #获取企业列表内的元素
    def companyname(self): #获取企业名称列表元素
        return self.driver.find_elements_by_css_selector('td.el-table_1_column_3 span.name')
    def com_element(self):  # 获取企业列表全选按钮
        return self.driver.find_element_by_css_selector('tr>th span.el-checkbox__inner')
    def get_filter_Unfold_status(self,number): # 获取号码展开状态
        return self.driver.find_element_by_css_selector(f'tr:nth-child({number})>td .shortPhone')
class Enterprise_list_operation(Gets_business_list_information_element,search_elment):
    def get_enterprise(self):
        Driver.login()
        self.to_page(2,'https://ik-staging.ikcrm.com/soukebox/search')
        time.sleep(2)
        self.search_input_element().send_keys("上海电气集团上海电机厂有限公司")
        time.sleep(1)
        self.search_carte().click()
        time.sleep(2)
        print(self.get_filter_Unfold_status(1).get_attribute('textContent'))
if __name__ == '__main__':

    a = Enterprise_list_operation().get_enterprise()