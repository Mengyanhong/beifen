from configs.mySettings import url,username,password
from configs.myDriver import Driver
from selenium.webdriver.support import expected_conditions as EX #导入显示等待元素定位时的ex执行模块
from selenium.webdriver.support.wait import WebDriverWait  #导入显示等待模块
from selenium.webdriver.common.by import By
import time


#创建基层运行版本

class basepage:
    def __init__(self):
        self.driver = Driver.get_driver() #获取driver驱动
    # WebDriverWait(driver,3,0.5).until(EC.visibility_of_element_located((By.CLASS_NAME,'customer-brand'))) #显示等待
    def get_element_WebDriverWait(self,timeout,locator): #创建显示等待函数,locator 格式 (By.ID, "kw")
        return WebDriverWait(driver=self.driver,timeout=timeout,poll_frequency=0.5).\
            until(EX.visibility_of_element_located(locator))

    def to_page(self,wait_time,url):
        time.sleep(wait_time)
        self.driver.get(url)
if __name__ == '__main__':
    basepage().to_page(1,url)
    print(time.time())
    Driver.get_driver().quit()
