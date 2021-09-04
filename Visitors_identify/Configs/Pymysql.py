# -*- coding: utf-8 -*-
# @Time    : 2021/8/5—15:42
# @Author  : 孟艳红
# @File    : Pymysql.py

import pymysql,time
class to_pymysql:
    def __init__(self,host):
        self.host = host
    def pymysql(self):
        if self.host == 'test':
            connect = pymysql.connect(host="sh-cdb-mvw92zno.sql.tencentcdb.com", port=59837, user="yxy_skb_test",
                                      password="9JqfEOe3kJjFWuTGx1l6", database="yxy_skb_test")
            # connect = pymysql.connect(host="rdscbq34656z0ix59br0.mysql.rds.aliyuncs.com", port=3306,
            #                           user="yxy_skb_test",
            #                           password="Yxyskb#ae964fd1", database="yxy_skb_test")
        elif self.host == 'staging':
            # connect = pymysql.connect(host="rm-m5eu4m6a4rugr22fcno.mysql.rds.aliyuncs.com", port=3306,
            #                           user="yxy_skb_staging",
            #                           password="Yxyskb#f65b9810", database="yxy_skb_staging")
            connect = pymysql.connect(host="sh-cdb-mvw92zno.sql.tencentcdb.com", port=59837, user="yxy_skb_staging",
                                      password="VRQKPsBUY52hrocG12hN", database="yxy_skb_staging")
        else:
            connect = False
        return connect
        # cursor = connect.cursor()  # 获取游标
        # cursor.execute("select * from recommendation_task_result")  # 执行语句
        # pymysql.commit()#提交sql
        # # cu = cursor.fetchone()  # 获取第一个数据（字典）
        # # r1 = cursor.fetchall()  # 获取全部数据（字典）# 结果是元组,fetchone()获取查询结果
        # cursor.close()
        # connect.close()
if __name__ == '__main__':
    pymysql = to_pymysql('test').pymysql()
    cursor = pymysql.cursor()

    # cursor.execute("delete from yxy_skb_test.org_sites where id = 219")
    # pymysql.commit()
    # time.sleep(2)
    # cu = cursor.execute("select * from `yxy_skb_test`.`org_sites` where `oid` = 5505101")
    # # cu = cursor.fetchone()  # 获取第一个数据（字典）
    # cu1 = cursor.fetchall()  # 获取第一个数据（字典）
    cursor.execute(
        "delete from yxy_skb_test.site_visitors where site_id in (select id from org_sites where oid = 5505101)")
    pymysql.commit()
    cursor.execute(
        "delete from yxy_skb_test.site_visitor_sessions where site_id in (select id from org_sites where oid = 5505101)")
    pymysql.commit()
    cursor.execute(
        "delete from yxy_skb_test.site_visitor_session_records where site_id in (select id from org_sites where oid = 5505101)")
    pymysql.commit()
    cursor.execute(
        "delete from yxy_skb_test.site_visitor_identify where site_id in (select id from org_sites where oid = 5505101)")
    pymysql.commit()
    cursor.execute(
        "delete from yxy_skb_test.online_customer_msg_info where site_id in (select id from org_sites where oid = 5505101)")
    pymysql.commit()
    cu = cursor.execute(
        "delete from yxy_skb_test.org_sites where oid = 5505101")
    pymysql.commit()
    cursor.execute("select * from `yxy_skb_test`.`org_sites` where `oid` = 5505101")
    cu1= cursor.fetchone()  # 获取第一个数据（字典）
    # cu = cursor.fetchone()  # 获取第一个数据（字典）
    time.sleep(2)
    cursor.close()
    pymysql.close()
    print(cu1)