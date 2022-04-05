from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains  # 导入鼠标事件的方法
from selenium.webdriver.common.keys import Keys
ActionChains = ActionChains
driver = webdriver.Edge()

import requests, re, os

# import turtle
# a = "t.write('想要画的文字', font=(, 16))"

# print(a)
url = "https://www.ddxs.cc/ddxs/179910/"
data = requests.get(url)
rst=[]
hreflist = re.findall('''<dd><a href="/ddxs/(.*?)">第''', data.text, re.S)
namelis = re.findall('''.html">(.*?)</a></dd>''', data.text)
namelist=[]
for j in namelis:
    namelist.append(j.replace(' ', ',').replace('?', ' '))
zp = zip(hreflist, namelist)
for i in zp:
    rst.append(list(i))
for pr in rst[208:]:
    # print("https://www.ddxs.cc/ddxs/{}".format(pr[0]))
    driver.get("https://www.ddxs.cc/ddxs/{}".format(pr[0]))
    datas = driver.find_element_by_css_selector('html body div#wrapper div.content_read div.box_con div#content').text
    # datas = requests.get(url="https://www.ddxs.cc/ddxs/{}".format(pr[0]))
    with open('镜面管理局.txt', 'a', encoding="utf-8") as f:
        f.write(pr[1] + '\n\n')
        f.writelines(datas + '\n\n')
# driver.get("https://www.ddxs.cc/ddxs/179910/27486336.html")
# print(driver.window_handles)
# print(driver.current_window_handle)
# print(driver.current_url)
# print(driver.title)
# print(driver.find_element_by_css_selector('html body div#wrapper div.content_read div.box_con div#content').text)