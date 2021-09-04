from selenium import webdriver
from configs.mySettings import url,username,password
class Driver:
    driver = None
    @classmethod
    def get_driver(cls,browser_name="chrome"):
        """获取浏览器驱动对象
        第一次调用，则生成并返回
        第二次及以后调用，则直接返回
        :return:
        """
        if cls.driver is None:
            if browser_name == "chrome":
                cls.driver = webdriver.Chrome()
            elif browser_name == "edge":
                cls.driver = webdriver.Edge()
            cls.driver.implicitly_wait(5)
            cls.driver.maximize_window()
            # cls.login()
        return cls.driver
    @classmethod
    def login(cls):
        """登录"""
        cls.driver.get(url)
        cls.driver.find_element_by_id('account').send_keys(username)
        cls.driver.find_element_by_xpath('//span/input[@id="password"]').send_keys(password)
        cls.driver.find_element_by_xpath('//button[@class="ant-btn ant-btn-primary"]').click()
        # cls.driver.find_element_by_class_name('navbar-brand')
if __name__ == '__main__':
    a1 = Driver().get_driver("edge")
    a2 = Driver.login()
    # a3 = Driver().get_driver("edge")
