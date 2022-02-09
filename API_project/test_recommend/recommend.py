#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    @Author : ShengMin
    @Created At : 2021/10/21 11:16 
    @Software: PyCharm
    @Description:
"""
import pymysql
import random
import json
import time

class Recommend:

    def connect(self,env):
        if env == 'test':
            hostName = "sh-cdb-mvw92zno.sql.tencentcdb.com"
            port = 59837
            userName = "yxy_skb_test"
            password = "9JqfEOe3kJjFWuTGx1l6"
            datebaseInfo = "yxy_skb_test"
            connect = pymysql.connect(host=hostName, port=port, user=userName,password=password, database=datebaseInfo)
            return connect
        elif env == 'staging':
            # connect = pymysql.connect(host="rm-m5eu4m6a4rugr22fcno.mysql.rds.aliyuncs.com", port=3306,
            #                           user="yxy_skb_staging",
            #                           password="Yxyskb#f65b9810", database="yxy_skb_staging")
            connect = pymysql.connect(host="sh-cdb-mvw92zno.sql.tencentcdb.com", port=59837, user="yxy_skb_staging",
                                      password="VRQKPsBUY52hrocG12hN", database="yxy_skb_staging")

    #insert table recommendation_task
    def insert_recommendation_task(self,con,oid,uid):
        cur = con.cursor()
        sql_insert_recommendation_task = 'insert into `yxy_skb_test`.`recommendation_task`(`oid`, `uid`, `status`, `cold_boot`, `total`) values(%s,%s,%s,%s,%s)'
        cur.execute(sql_insert_recommendation_task,(oid, uid, '0', '0', '0'))
        con.commit()

    #insert table recommender_user_tag_info
    def insert_recommender_user_tag_info(self,con,oid,uid,tag):
        cur = con.cursor()
        sql_insert_recommender_user_tag_info = 'insert into `yxy_skb_test`.`recommender_user_tag_info`(uid, oid,tags) values (%s,%s,%s)'
        cur.execute(sql_insert_recommender_user_tag_info,(uid,oid,tag))
        con.commit()

    #insert table recommendation_user_seed
    def insert_recommendation_user_seed(self, con, oid, uid, pid,company_name):
        cur = con.cursor()
        sql_insert_recommendation_user_seed = 'insert into `yxy_skb_test`.`recommendation_user_seed`(`oid`, `uid`, `pid`,`company_name`) values(%s,%s,%s,%s)'
        cur.execute(sql_insert_recommendation_user_seed, (oid,uid, pid,company_name))
        con.commit()

    #insert table recommendation_task_seed
    def insert_recommendation_task_seed(self, con, task_id, pid):
        cur = con.cursor()
        sql_insert_recommendation_task_seed = 'insert into `yxy_skb_test`.`recommendation_task_seed`(`task_id`, `pid`) values(%s,%s)'
        cur.execute(sql_insert_recommendation_task_seed, (task_id, pid))
        con.commit()

    #insert table recommendation_target_region
    # def insert_recommendation_target_region(self, con, uid, oid,region_code):
    #     cur = con.cursor()
    #     sql_insert_recommendation_target_region = 'insert into `yxy_skb_test`.`recommendation_target_region`(`business_type`, `business_id`, `oid`, `region_code`) values(%s,%s,%s,%s)'
    #     cur.execute(sql_insert_recommendation_target_region, ('1', uid,oid,region_code))
    #     con.commit()

    #insert table recommendation_target_region
    def insert_recommendation_target_region(self, con, uid, oid,region_code):
        try:
            cur = con.cursor()
            sql_insert_recommendation_target_region = 'insert into `yxy_skb_test`.`recommendation_target_region`(`business_type`, `business_id`, `oid`, `region_code`) values(%s,%s,%s,%s)'
            cur.execute(sql_insert_recommendation_target_region, ('1', uid,oid,region_code))
            con.commit()
        except:
            pass

    def get_oid(self):
        oid_range_min = 11110000
        oid_range_max = 11210000
        randam_oid = random.randint(oid_range_min,oid_range_max)
        print("oid: "+str(randam_oid))
        return(str(randam_oid))

    def get_uid(self):
        uid_range_min = 111100000
        uid_range_max = 112100000
        random_uid = random.randint(uid_range_min,uid_range_max)
        print("uid: " + str(random_uid))
        return(str(random_uid))

    def get_tag(self):
        tag_list = ["软件","财务服务","箱包","工程承包","租赁服务","乳制品","砌筑材料","保健食品",
                    "工程机械","展览服务","办公设备","节能设备",
                    "电工仪器仪表","化肥","陶瓷","皮革","玻璃","酒类",
                    "茶叶","钟表","数码产品","广告服务","农副产品加工",
                    "户外用品","日用五金","纺织加工","传感器","汽车用品","生物化工","模具","功能材料",
                    "文化办公设备","农业机械","种植业","摄影摄像服务","宠物","玻璃制品","定制加工","粮油作物","轮胎","会计服务",
                    "制冷设备","乐器","塑料机械","音像制品","手机配件","电线、电缆","管件","电动工具","舞台设备","服装加工",
                    "玻璃纤维","燃气设备","安防监控设备","工艺品加工","地板","宠物用品",
                    "电脑配件","化学试剂","通信线缆","消防设备","不锈钢材","景观工程",
                    "网络服务","建筑、建材类管材","纺织辅料","管材","非金属矿产",
                    "办公家具","贵金属","豆制品","量具","电池","市场调研","餐具",
                    "瓷砖","食用油","办公耗材","工业气体","石油设备","数控机床",
                    "船舶","型材","冲饮品","风机","低压电器","食品添加剂","塑料加工",
                    "配电输电设备","信息安全产品","染料","物流服务","室内照明灯具",
                    "工地施工材料","酒店设备","化学纤维","卫浴洁具","手套","方便食品"]
        choice_count = random.choices(list(range(1,6)), weights=[50, 20, 15, 10, 5],k=1)[0]
        choice_tags = random.choices(tag_list, k=choice_count)
        choice_tags_str = ",".join(choice_tags)
        return (choice_count,choice_tags_str)

    def get_seed_company(self):
        # 种子企业数量, 随机0-10个, 设置权重
        choice_count = random.choices(list(range(1,11)), weights=[40, 20, 10, 5, 5, 5, 5, 5, 2, 2, 1], k=1)[0]
        # 选择的种子企业
        # choice_seeds = random.choices(companys_list, k=choice_count)

    def get_region_code(self):
        region_codes = [11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 1101, 3101, 3301,
                        3302, 3303, 3304, 3305, 3306, 3307, 3308, 3309, 3310, 3311, 4401, 4402, 4403, 4404, 4405, 4406,
                        4407, 4408, 4409, 4412, 4413, 4414, 4415, 4416, 4417, 4418, 4419, 4420, 4451, 4452, 4453]
        # choice_codes = random.choices(region_codes)
        # print(str(choice_codes[0]))
        choice_count = random.choices(list(range(1, 6)), weights=[50, 20, 15, 10, 5], k=1)[0]
        choice_tags = random.choices(region_codes, k=choice_count)
        return choice_tags

    def insert_user_tag_data(self,con):
        uid = self.get_uid()
        oid = self.get_oid()
        tag = self.get_tag()
        self.insert_recommender_user_tag_info(con, oid, uid, tag[1])
        region_ids = self.get_region_code()
        for region_id in region_ids:
            print(region_id)
            self.insert_recommendation_target_region(con, uid, oid, region_id)
        self.insert_recommendation_task(con, oid, uid)

    # def insert_recommendation_target_region_data(self,con):
    #     uid = self.get_uid()
    #     oid = self.get_oid()
    #     region_id = self.get_region_code()
    #     self.insert_recommendation_target_region(con,uid,oid,region_id)
    #     self.insert_recommendation_task(con, oid, uid)

    def insert_recommendation_user_seed_data(self,con):
        filename = "C:/Users/Melody/Desktop/20000家工商企业-测试数据.json"
        with open(filename, 'r', encoding='UTF-8') as f:
            jlist = json.load(f)
        # print(len(jlist))
        uid = self.get_uid()
        oid = self.get_oid()
        for dic in jlist[0:30000]:
            uid = self.get_uid()
            oid = self.get_oid()
            pid = dic['PID']
            company = dic['ENTNAME']
            print(pid)
            print(company)
            self.insert_recommendation_user_seed(con, oid, uid, pid,company)
            self.insert_recommendation_task(con, oid, uid)
            time.sleep(1)

    def insert_recommendation_task_seed_data(self,con):
        filename = "C:/Users/Melody/Desktop/20000家工商企业-测试数据.json"
        with open(filename, 'r', encoding='UTF-8') as f:
            jlist = json.load(f)
        taskID=100000
        for dic in jlist[0:30000]:
            pid = dic['PID']
            print(pid)
            self.insert_recommendation_task_seed(con, taskID,pid)
            time.sleep(1)
            taskID+=1



if __name__ == '__main__':
    recomment = Recommend()
    con = recomment.connect("test")
    for i in range(30000):
        recomment.insert_user_tag_data(con)  #1
    # recomment.insert_recommendation_user_seed_data(con) #3


