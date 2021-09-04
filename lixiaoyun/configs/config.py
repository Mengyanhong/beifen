from selenium import webdriver

driver = webdriver.Chrome()

from selenium.webdriver.common.action_chains import ActionChains  # 导入鼠标事件的方法

ActionChains = ActionChains

TEST_HOST = 'https://lxcrm-test.weiwenjia.com/soukebox/search?'

# WebDriverWait(driver, 2, 0.5).until(EC.visibility_of_element_located(
#     (By.XPATH, '/html/body/section/section/section/aside/section/section/nav/ul/li[2]/a')))  # 隐式等待的书写方式