
from selenium import webdriver


# driver = webdriver.Chrome()  # 定义webdriver路径
# # # coding = utf-8 from selenium import webdriver
# driver.maximize_window()  # 最大化浏览器
# driver.implicitly_wait(10)  # 等待页面加载最长等待10秒
# driver.get(
#     "https://www.baidu.com/")  # 访问登录页面
dr=webdriver.Chrome()
dr.get('https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=selenium%E6%BB%91%E5%8A%A8%E9%A1%B5%E9%9D%A2%E7%9A%84%E6%BB%9A%E5%8A%A8%E6%9D%A1&fenlei=256&rsv_pq=b9a89f1700056ce3&rsv_t=e83ah8TveyZuqKXPy2ASktbbNvBVnnHsOqW5zXjg0gupc%2Fls5b3bo5JQDao&rqlang=cn&rsv_enter=1&rsv_dl=ts_2&rsv_sug3=30&rsv_sug1=36&rsv_sug7=101&rsv_sug2=1&rsv_btype=i&prefixsug=selenium%25E6%25BB%2591%25E5%258A%25A8&rsp=2&inputT=49183&rsv_sug4=52208')
# js=document.getElementsByClassName("scroll")[0].scrollTop=10000 #可以调整10000，10000就是到底
# dr.execute_script("window.scrollTo(11,1000);")
js="var q=document.documentElement.scrollTop=10000"
dr.execute_script(js)
# 就是这么简单，修改这个元素的scrollTop就可以
# dr.execute_script(js)