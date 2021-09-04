# -*- coding: utf-8 -*-
# 测试是否是500强企业
import requests,json
import urllib3
urllib3.disable_warnings()

from search_API import search_API

class TestIsChineseTop500:
    def test_isChineseTop500(self,connect_db):
        API_data=search_API('isChineseTop500',True,'IS')['items']
        API_PID=[]
        for i in range(len(API_data)):
            API_PID.append(API_data[i]['id'])
        print(API_PID)

        db_PID=[]
        db=connect_db
        db_datas = db.enterprise.enterpriseTags.find({'tag': 2})
        for db_data in db_datas:
            db_PID.append(db_data['PID'])
        print(db_PID)

        diff_PID=[]
        for i in range(len(db_PID)):
            flag=False
            for j in range(len(API_PID)):
                if API_PID[j]==db_PID[i]:
                    flag = True
                    break
            if flag==False:
                diff_PID.append(db_PID[i])

        print(diff_PID)







