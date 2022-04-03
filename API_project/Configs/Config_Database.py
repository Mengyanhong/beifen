import pymongo, pymysql, pytest, sys, datetime
from sshtunnel import SSHTunnelForwarder
from elasticsearch import Elasticsearch


class DataBase_All:
    def __init__(self, projectname="home"):
        self.ssh_pkey_path = sys.path[0].split(projectname)[0]

    def to_pymysql(self, host):
        if host == 'test':
            connect = pymysql.connect(host="sh-cdb-mvw92zno.sql.tencentcdb.com", port=59837, user="yxy_skb_test",
                                      password="9JqfEOe3kJjFWuTGx1l6", database="yxy_skb_test")
            # connect = pymysql.connect(host="rdscbq34656z0ix59br0.mysql.rds.aliyuncs.com", port=3306,
            #                           user="yxy_skb_test",
            #                           password="Yxyskb#ae964fd1", database="yxy_skb_test")
        elif host == 'staging':
            # connect = pymysql.connect(host="rm-m5eu4m6a4rugr22fcno.mysql.rds.aliyuncs.com", port=3306,
            #                           user="yxy_skb_staging",
            #                           password="Yxyskb#f65b9810", database="yxy_skb_staging")
            connect = pymysql.connect(host="sh-cdb-mvw92zno.sql.tencentcdb.com", port=59837, user="yxy_skb_staging",
                                      password="VRQKPsBUY52hrocG12hN", database="yxy_skb_staging")
        else:
            connect = pymysql.connect(host="rm-m5e1zye921nmxejq1do.mysql.rds.aliyuncs.com", user="tmp_read",
                                      password="pc4TJSALbECGk5yBCkTJ", database="yxy_skb", charset="utf8")
            # cursor = conn.cursor()
            # yield cursor
            # cursor.close
            # connect.close
        return connect

    def to_pymongo(self):
        # 连接数据库
        mongo_port = 3717
        mongo_address = "dds-m5e44df0967967a42.mongodb.rds.aliyuncs.com"
        mongo_user = 'enterprise_read'
        mongo_password = 'Ce782ef2'
        server = SSHTunnelForwarder(
            ssh_address_or_host=("47.104.226.30", 40022),  # 指定ssh登录的跳转机的IP port
            ssh_username='jar',  # 跳板机用户名
            ssh_pkey=f'{self.ssh_pkey_path}home\\.ssh\\id_rsa',  # 设置密钥
            remote_bind_address=(mongo_address, mongo_port)  # 设置数据库服务地址及端口
        )
        server.start()
        conn = pymongo.MongoClient(
            host='127.0.0.1',  # host、port 固定
            port=server.local_bind_port
        )
        db = conn["admin"]
        db.authenticate(mongo_user, mongo_password)

        def _to_pymongo(serve="start"):
            if serve == "close":
                conn.close()  # 关闭游标
                server.close()  # 关闭跳板机
                return "已关闭数据库链接"
            else:
                return conn  # 返回游标

        return _to_pymongo

    def to_pymongo_test(self):
        # 连接数据库
        mongo_host = "skb-test-mongodb.lixiaoskb.com"
        port = 27017
        mongo_user = 'twe_test'
        mongo_password = 'b7w7zfKapT3yW0DAV2bD'
        conn = pymongo.MongoClient(
            host=mongo_host,  # host、port 固定
            port=port,
            # username=mongo_user,
            # password=mongo_password
        )
        db = conn["admin"]
        db.authenticate(mongo_user, mongo_password)
        yield conn
        print(22)
        conn.close()  # 关闭游标
        # server.close()  # 关闭跳板机


class ES_All:
    def __init__(self, environment):
        self.environment = environment

    def ES(self):
        if self.environment == "lxcrm":
            es_client = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，prod
                                      http_auth=('mengyanhong', 'Aa123456'))
            # return es_client
            # print(host,1)
        elif self.environment == "staging":
            es_client = Elasticsearch('es-cn-2r42j6jsc00079qtt.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，staging
                                      http_auth=('elastic', 'Stagprod#985'))
        # print(host, 2)
        else:
            es_client = Elasticsearch('es-cn-i7m27x1em002z5u9d.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，test
                                      http_auth=('tester', 'tester_Aa123456'))
        # es_client = Elasticsearch('es-cn-nif1oiv5w0009di0f.public.elasticsearch.aliyuncs.com:9200',
        #                           http_auth=('lihexiang', 'Aa123456'))
        # es_client = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，prod
        #                           http_auth=('mengyanhong', 'Aa123456'))
        # es_client = Elasticsearch('es-cn-tl3280yva0001mwg8.kibana.elasticsearch.aliyuncs.com:5601',  # 最新地址，prod
        #                           http_auth=('mengyanhong', 'Aa123456'))
        # es_client = Elasticsearch('es-cn-i7m27x1em002z5u9d.public.elasticsearch.aliyuncs.com:9200', #最新地址，test
        #                           http_auth=('tester', 'tester_Aa123456'))
        return es_client


if __name__ == '__main__':
    b = DataBase_All().to_pymongo()
    db = b()
    s = db.enterprise.EnterpriseAlterInfo.find({}, {"PID": -1, "alterInfo": -1}).limit(10).skip(0)
    a = db.enterprise.EnterpriseBaseInfo.find_one({'PID': '9be95194807a7c6d509dd67761517f4e'})

    for i in s:
        print(i)
    # print(a)
    print(b("close"))
    # print(datetime.datetime(2013, 12, 6, 0, 0))
    # print(type(a))
    # print(s)
