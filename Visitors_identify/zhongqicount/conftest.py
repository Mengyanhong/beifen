import pymongo,pymysql,pytest
from sshtunnel import SSHTunnelForwarder

@pytest.fixture()
def sql():
    conn = pymysql.connect(host="rm-m5e1zye921nmxejq1do.mysql.rds.aliyuncs.com", user="tmp_read",
                           password="pc4TJSALbECGk5yBCkTJ", database="yxy_skb", charset="utf8")
    cursor = conn.cursor()
    yield cursor
    # conn.close()


#正式
@pytest.fixture()
def mongoDB():
    # 连接数据库
    mongo_port = 3717
    mongo_address = "dds-m5e44df0967967a42.mongodb.rds.aliyuncs.com"
    mongo_user = 'enterprise_read'
    mongo_password = 'Ce782ef2'
    server = SSHTunnelForwarder(

        ssh_address_or_host=("47.104.226.30", 40022),  # 指定ssh登录的跳转机的IP port
        ssh_username='jar',  # 跳板机用户名
        ssh_pkey='D:/Users/admin/.ssh/id_rsa/id_rsa',  # 设置密钥
        remote_bind_address=(mongo_address, mongo_port)  # 设置数据库服务地址及端口
    )
    server.start()
    conn = pymongo.MongoClient(
        host='127.0.0.1',  # host、port 固定
        # port=27017
        port=server.local_bind_port
    )
    db = conn["admin"]
    db.authenticate(mongo_user, mongo_password)

    yield conn
    conn.close()
    server.close()
