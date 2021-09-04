from configs.config import driver,ActionChains
from libs.login import login
from tools.yamlControl import get_yaml_data
import time

file = get_yaml_data('../data/login_case.yaml')[0]

login_file = login(file[1],file[0]) #初始化登录数据
login_file.login() #登录
login_switch = login_file.login_case() #判断登录账户是否正确

class Switch_module:
    def search(self,login_switch,search_text):
        driver.implicitly_wait(5)
        if login_switch == True:  # 判断登陆结果
            list_site = driver.find_element_by_xpath(
                "/html/body/section/section/section/aside/section/section/nav/ul/li[2]/a")  # 定位悬浮位置
            ActionChains(driver).move_to_element(list_site).perform()  # 鼠标移动到定位位置之上
            time.sleep(2)
            list_site_Ac = driver.find_elements_by_xpath(
                f"/html/body/section/section/section/aside/section/section/nav/ul/li[2]/div/ul/li[1]/a")  # 获取二级菜单内容
            if list_site_Ac == []:
                list_site_text = list_site.text
                list_site.click()  # 点击找企业
                search_input = driver.find_elements_by_xpath(
                    '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/input')
                if search_input != []:
                    for i in search_input:
                        i.send_keys(search_text)  # 定位输入框
                        driver.find_element_by_xpath(
                            '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[2]/button').click()  # 执行搜索
                        print('----------进入单SKB高级数据版', list_site_text, '----------')
                        return True
                else:
                    print('----------进入非高级数据版单SKB', list_site_text, '----------')
                    return False
            else:
                for i in list_site_Ac:
                    i_text =i.get_attribute('textContent')
                    i_text = i_text.strip('\n').strip()
                    i.click()  # 点击二级菜单找企业
                    search_input = driver.find_elements_by_xpath(
                        '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[1]/div/div[1]/input')
                    if search_input != []:
                        for i in search_input:
                            i.send_keys(search_text)  # 定位输入框
                            driver.find_element_by_xpath(
                                '/html/body/section/section/section/div[2]/div/div/div/div[1]/div[2]/div[2]/button').click()  # 执行搜索
                            print('----------进入高级数据版', i_text, '----------')
                            return True
                    else:
                        print('----------进入非高级数据版', i_text, '----------')
                        return False
        else:
            return 'error'

    def search_page(self,search_retu,search_text):
        driver.implicitly_wait(5)
        search_input = driver.find_elements_by_xpath(
            '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/input')  # 定位找企业结果页输入框
        search = driver.find_elements_by_xpath(
            '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/div')  # 定位找企业结果页搜一搜按钮
        search_input_del = driver.find_elements_by_xpath(
            '/html/body/section/section/section/div[2]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/div[3]')  # 定位找企业结果页输入框删除按钮
        if search_retu == False:
            for i in search_input:
                i.send_keys(search_text)
            for i in search:
                i.click()
            return ('搜索结束')
        elif search_retu == True:
            if search_input_del != []:
                for i in search_input_del:
                    i.click()
                    time.sleep(1.5)
            for i in search_input:
                i.send_keys(search_text)
            for i in search:
                i.click()
            return ('搜索结束')
        else:
            return ('账户错误')
if __name__ == "__main__": #快捷键ctrl+j
    file = get_yaml_data('../data/login_case.yaml')[0]
    print(file)
    loog_file = login(file[1],file[0])
    res = loog_file.login()
    print(res)
    res_1 = loog_file.login_case()
    print(res_1)
    res_2 = Switch_module().search(res_1,file[1]['search'])
    res_3 = Switch_module().search_page(res_2,file[1]['search'])
    print(res_3)
    time.sleep(3)
    driver.quit()
    # pprint.pprint(res_1)