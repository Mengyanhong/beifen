from Configs.config import driver,url
import time
import inspect
import random
class Logins:
    @classmethod
    def login(self):
        driver.implicitly_wait(5)
        driver.get(url) #访问网址
        driver.find_element_by_name("username").send_keys("libai") #输入账户
        driver.find_element_by_name("password").send_keys("opmsopms123") #输入密码
        # driver.find_element_by_xpath("//form/div/input[@class='form-control' and @name='password']").send_keys("opmsopms123")
        # driver.find_element_by_xpath('//button[@class="btn btn-lg btn-login btn-block"]').click()
        driver.find_element_by_tag_name('button').click() #点击登录
    @staticmethod
    def comment():
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//li/a/i[@class="fa fa-plane"]').click() #点击员工相册
        time.sleep(2)
        driver.find_element_by_xpath('//div[1]/p[1]/a').click() #点击图片名称进入图片详情
        time.sleep(2)
        tar = driver.find_element_by_xpath('//form/div/div/textarea[@name="comment" and @class="form-control"]')
        driver.execute_script("arguments[0].scrollIntoView();", tar)  # 通过定位需要移动到的位置移动到可见的元素区
        tar.send_keys("滚动测试")
        # driver.execute_script("window.scrollBy(0,800);") #向上滑动800像素
        # driver.find_element_by_xpath('//form/div/div/textarea[@name="comment" and @class="form-control"]').send_keys(
        #     "实践") #输入评论信息
        # driver.find_element_by_class_name('btn-primary').click()
        jieguo = int(input('请输入测试结果'))
        if jieguo == 1:
            print("测试结束没有评论")
        else:
            driver.find_element_by_xpath('//button[@class="btn btn-primary pull-right"]').click() #执行提交
            print("测试结束评论成功")

    @staticmethod
    def leave():
        driver.implicitly_wait(5)
        # driver.find_element_by_xpath('//li/a/i[@class="fa fa-suitcase"]').click()  # 点击员工相册
        driver.find_element_by_class_name('fa-suitcase').click() # 点击员工相册
        driver.find_element_by_xpath('//div[@class="jumbotron text-center"]/span/a[text()="请假"]').click() #点击审批管理
        time.sleep(1)
        driver.find_element_by_class_name("btn-success").click() #点击我要请假
        driver.find_element_by_xpath('//select[@name="type" and @class="form-control"]').click() #点击请假类型
        driver.find_element_by_xpath('//select/option[text()="事假"]').click() #选择事假
        time.sleep(1)
        driver.find_element_by_name('started').send_keys('2021-04-25') #输入请假日期
        time.sleep(1)
        driver.find_element_by_name('ended').send_keys('2021-04-28')  # 输入请假日期
        aed = driver.find_element_by_xpath('//div/input[@type="number" and @name="days"]')  # 定位请假天数
        aed.clear()  # 清空输入框
        time.sleep(1)
        aed.click()
        aed.send_keys("3")  # 输入请假天数
        driver.find_element_by_xpath('//div/textarea[@class="form-control"]').send_keys('上海太大了')  # 输入请假事由
        driver.execute_script("window.scrollBy(0,300);") #向上滑动300像素
        driver.find_element_by_class_name('fa-plus-circle').click()  # 点击添加审批
        driver.find_element_by_xpath(f'//div/ul/li[{random.randint(1, 5)}]/a[@class="js-selectuser"]').click()  # 选择审批人员
        jieguo = int(input('请输入测试结果'))
        if jieguo == 1:
            print("测试结束没有提交审批")
        else:
            driver.find_element_by_class_name('btn-primary').click()  # 提交审批
            print("测试结束提交审批成功")

if __name__ == '__main__':
    Logins.login()
    Logins.comment()
    Logins.leave()
    time.sleep(3)
    # print(inspect.ismethod(Logins.login))
    # print(inspect.isfunction(Logins.comment))
    driver.quit()