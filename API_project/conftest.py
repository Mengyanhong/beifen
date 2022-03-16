# -*- coding: utf-8 -*-
import time,pytest
import pymongo
from sshtunnel import SSHTunnelForwarder
import datetime
from elasticsearch import Elasticsearch

def pytest_collection_modifyitems(items): #设置用例标题显示编码
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        print(item.nodeid)
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.fixture()
def connect_db():
    # 连接数据库
    mongo_port = 3717
    mongo_address = "dds-m5e44df0967967a42.mongodb.rds.aliyuncs.com"
    mongo_user = 'enterprise_read'
    mongo_password = 'CuOIdrN4j7S1OI6Ds8gT'
    server = SSHTunnelForwarder(

        ssh_address_or_host=("47.104.226.30", 40022),  # 指定ssh登录的跳转机的IP port
        ssh_username='jar',  # 跳板机用户名
        ssh_pkey='C:/Users/admin/.ssh/id_rsa/id_rsa',  # 设置密钥
        remote_bind_address=(mongo_address, mongo_port)  # 设置数据库服务地址及端口
    )
    server.start()
    conn = pymongo.MongoClient(
        host='127.0.0.1',  # host、port 固定
        port=server.local_bind_port
    )
    db = conn["enterprise"]
    db.authenticate(mongo_user, mongo_password)

    yield conn
    conn.close()
    server.close()
@pytest.fixture()
def ES():
    # def _ES(host):
    #     if host == "lxcrm":
    #         es_client = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，prod
    #                                   http_auth=('mengyanhong', 'Aa123456'))
    #         return es_client
    #         # print(host,1)
    #     elif host == "staging":
    #         yield Elasticsearch('es-cn-2r42j6jsc00079qtt.kibana.elasticsearch.aliyuncs.com:9200',  # 最新地址，staging
    #                           http_auth=('elastic', 'Stagprod#985'))
    #         print(host, 2)
    #     else:
    #         yield Elasticsearch('es-cn-i7m27x1em002z5u9d.public.elasticsearch.aliyuncs.com:9200',   # 最新地址，test
    #                           http_auth=('tester', 'tester_Aa123456'))
    #         print(host, 3)
    # return _ES
    # es_client = Elasticsearch('es-cn-nif1oiv5w0009di0f.public.elasticsearch.aliyuncs.com:9200',
    #                           http_auth=('lihexiang', 'Aa123456'))
    es_client = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200', #最新地址，prod
                              http_auth=('mengyanhong', 'Aa123456'))
    # es_client = Elasticsearch('es-cn-i7m27x1em002z5u9d.public.elasticsearch.aliyuncs.com:9200', #最新地址，test
    #                           http_auth=('tester', 'tester_Aa123456'))
    yield es_client

# @pytest.fixture()
# def ES():
#     # es_client = Elasticsearch('es-cn-nif1oiv5w0009di0f.public.elasticsearch.aliyuncs.com:9200',
#     #                           http_auth=('lihexiang', 'Aa123456'))
#     es_client = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200', #最新地址，prod
#                               http_auth=('mengyanhong', 'Aa123456'))
#     # es_client = Elasticsearch('es-cn-i7m27x1em002z5u9d.public.elasticsearch.aliyuncs.com:9200', #最新地址，test
#     #                           http_auth=('tester', 'tester_Aa123456'))
#     yield es_client

@pytest.fixture()
def ES_test():
    # es_client = Elasticsearch('es-cn-nif1oiv5w0009di0f.public.elasticsearch.aliyuncs.com:9200',
    #                           http_auth=('lihexiang', 'Aa123456'))
    # es_client = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200', #最新地址，prod
    #                           http_auth=('mengyanhong', 'Aa123456'))
    es_client = Elasticsearch('es-cn-i7m27x1em002z5u9d.public.elasticsearch.aliyuncs.com:9200', #最新地址，test
                              http_auth=('tester', 'tester_Aa123456'))
    yield es_client

@pytest.fixture()
def date():
    def _date(bef_af,n):
        currentDate = datetime.date.today() #当前日期
        current_day = currentDate.day
        current_month = currentDate.month
        current_year = currentDate.year

        # 闰年：能被4整除而不能被100整除 或者 能被400整除
        month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        # bef_af 传入值为 bef 或者 af
        #n月前
        if bef_af=='bef':
            if current_month>n:
                bef_month=current_month-n
                bef_year=current_year
            else:
                bef_month = current_month + 12 - n
                bef_year = current_year - 1

            if (bef_year % 4 == 0 and bef_year % 100 != 0) or (bef_year % 400 == 0):
                month_day[1] += 1
            if current_day>month_day[bef_month-1]: #假设n月前没有31日，则置为当月最后一天
                bef_day=month_day[bef_month-1]
            else:
                bef_day=current_day
            result_time=int(time.mktime(datetime.date(bef_year,bef_month,bef_day).timetuple())*1000)
            return result_time

        elif bef_af=='af':
            if current_month+n<=12:
                af_month=current_month+n
                af_year=current_year
            else:
                af_month=current_month+n-12
                af_year=current_year+1

            if (af_year % 4 == 0 and af_year % 100 != 0) or (af_year % 400 == 0):
                month_day[1] += 1
            if current_day>month_day[af_month-1]: #假设n月前没有31日，则置为当月最后一天
                af_day=month_day[af_month-1]
            else:
                af_day=current_day
            result_time=int(time.mktime(datetime.date(af_year,af_month,af_day).timetuple())*1000)
            return result_time
    return _date

@pytest.fixture()
#计算当前时间到某个时间的时间差
def diff_date():
    def _diff_date(createDate):
        currentDate = datetime.date.today()
        current_day = currentDate.day
        current_month = currentDate.month
        current_year = currentDate.year

        # 闰年：能被4整除而不能被100整除 或者 能被400整除
        month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (current_year % 4 == 0 and current_year % 100 != 0) or (current_year % 400 == 0):
            month_day[1] += 1
        timeArray = time.localtime(createDate/1000)
        createDate=time.strftime("%Y-%m-%d",timeArray)
        print(createDate)

        create_year = int(createDate[:4])
        create_month = int(createDate[5:7])
        create_day = int(createDate[8:10])

        # 计算日
        if current_day >= create_day:
            diff_day = current_day - create_day
        else:
            if current_month>1:
                diff_day = current_day - create_day + month_day[current_month-1-1] #-1 索引的-1，-1是算上一个月的天数
                current_month -= 1
            else:
                diff_day = current_day - create_day + month_day[11]  #直接加12月的天数
                current_month =12
                create_year-=1

        # 计算月
        if current_month >= create_month:
            diff_month = current_month - create_month
        else:
            diff_month = current_month - create_month + 12
            current_year -= 1

        diff_year = current_year - create_year
        return [diff_year,diff_month,diff_day]
    return _diff_date



# def pytest_collection_modifyitems(session: "Session", config: "Config", items: list["Item"]) -> None:
#     # item表示每个测试用例，解决用例名称中文显示问题
#     for item in items:
#         item.name = item.name.encode("utf-8").decode("unicode-escape")
#         item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")





