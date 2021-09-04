# @Time : 2021/8/23 14:35
# @Author : 孟艳红
# @File : get_skb.py
from selenium import webdriver
import random
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

for i in range(11):
    # if i <=1:
    #     driver = webdriver.Chrome()
    # else:
    driver = webdriver.Edge()
    driver.get('https://stage.lixiaoskb.com/login')
    print(driver.current_url)
    try:
        element = WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="chat-box" and @style="display: none;"]')))
        element.click()
    except:
            pass
    A = WebDriverWait(driver, 2, 0.5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.chat-textarea')))
    # A = driver.find_element_by_css_selector('.chat-textarea')
    A.send_keys(f'{random.randint(10,99)}')
    sleep(0.5)
    driver.find_element_by_css_selector('.chat-send').click()
    driver.delete_all_cookies()
    sleep(1.5)
# for i in range(9):
#     js='window.open("https://www.baidu.com/");'
#     driver.execute_script(js)
# allhandles=driver.window_handles  #获取当前窗口句柄
# # print(driver.get_cookies())
# for j in range(10):
#     if driver.current_window_handle==allhandles[j]:
#         # sleep(1.5)
#         # driver.delete_all_cookies()
#         # sleep(1.5)
#         # driver.get('https://stage.lixiaoskb.com/login')
#         print(driver.current_url)
#
#         # print(driver.title())
#         # driver.delete_all_cookies()
#     else:
#         driver.switch_to.window(allhandles[j])#切换窗口
#         # sleep(1.5)
#         # driver.delete_all_cookies()
#         # sleep(1.5)
#         # driver.get('https://stage.lixiaoskb.com/login')
#         print(driver.current_url)
#         # print(driver.title())
#     if j == 0:
#         sleep(4)
#     else:
#         sleep(0.5)
#     # sleep(5)
#     try:
#         driver.find_element_by_xpath('//div[@class="chat-box" and @style="display: none;"]').click()
#     except:
#         sleep(0.5)
#         if driver.find_elements_by_xpath('//div[@class="chat-box" and @style="display: block;"]') ==[]:
#             pass
#             # driver.find_element_by_xpath('//div[@class="chat-box" and @style="display: none;"]').click()
#     sleep(0.5)
#     driver.find_element_by_css_selector('.chat-textarea').send_keys(random.randint(100,1000))
#     # driver.find_element_by_css_selector('.chat-input .chat-textarea').send_keys('shanghai')
#     sleep(0.5)
#     driver.find_element_by_css_selector('.chat-send').click()
#     driver.delete_all_cookies()
#     # print(driver.title)
# driver.close()
# # driver.quit()