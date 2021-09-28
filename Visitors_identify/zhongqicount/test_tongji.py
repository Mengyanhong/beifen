from collections import Counter
from itertools import count

import pytest, openpyxl, datetime

filename = 'zhongq.xlsx'
file = openpyxl.load_workbook(filename)
sheet = file['统计']


# begin='2021-09-17 00:00:00'
# end='2021-09-17 23:59:59'

class TestTongji:
    def test_companyname(self, sql, mongoDB):
        cursor = sql
        db = mongoDB
        # sql='''SELECT customer_name,company_name,org_major_info.oid from org_major_info right join visitor_identify_account
        #         on org_major_info.oid=visitor_identify_account.oid
        #         where visitor_identify_account.create_time BETWEEN '2021-09-17 00:00:00' and '2021-09-17 23:59:59' '''
        # sql = '''SELECT customer_name,company_name,org_major_info.oid from org_major_info right join visitor_identify_account
        #                 on org_major_info.oid=visitor_identify_account.oid '''
        # cursor.execute(sql)
        cursor.execute("""select co_list_sum.customer,co_list_sum.company,co_list_sum.id_list,count(DISTINCT site_visitor_identify.ip_user) 
        as ip_user_sum,co_list_sum.vist_sum ,co_list_sum.oidli from (select oidlist.customer_name 
        as customer,oidlist.company_name as company,GROUP_CONCAT(DISTINCT org_sites.id separator ",") 
        as id_list, oidlist.oid as oidli, count(DISTINCT site_visitors.visitor_id) as vist_sum from site_visitors 
        right join org_sites on site_visitors.site_id = org_sites.id right join (select customer_name,company_name,oid from org_major_info 
        where oid in (select oid from visitor_identify_account)) as oidlist  on org_sites.oid = oidlist.oid  group by  customer,company,oidli ) 
        as co_list_sum left join site_visitor_identify on co_list_sum.oidli=site_visitor_identify.oid  group by co_list_sum.customer,co_list_sum.company,co_list_sum.oidli
        """)
        # pymysql.commit()
        siteid = cursor.fetchall()
        # import  re
        # rule = '/d'
        for i in range(len(siteid)):
            company_list = siteid[i]
            sheet['A' + str(i + 2)] = company_list[0]
            sheet['B' + str(i + 2)] = company_list[1]
            sheet['C' + str(i + 2)] = company_list[2]
            sheet['D' + str(i + 2)] = company_list[3]
            sheet['E' + str(i + 2)] = company_list[4]
        # file.save(filename)

            if company_list[2]:
                # print(company_list)
                siteId_list = company_list[2].split(',')
                siteId_list_find = []
                for siteId_list_id in siteId_list:
                    siteId_list_find.append(int(siteId_list_id))
                # print(siteId_list)
                allIP = db.visitor.SiteVisitorLogging.find({"siteId": {'$in': siteId_list_find}})
                # allIP = db.visitor.SiteVisitorLogging.aggregate([{'$group':{'_id':{"siteId": {'$in': siteId_list_find}},'ip': {'$push': "$ip"}}}])
                # allIP=db.visitor.SiteVisitorLogging.find({'$and': [{'visitDate': {'$gte': datetime.datetime(2021, 9, 17, 00, 00, 00)}},
                #               {'visitDate': {'$lte': datetime.datetime(2021, 9, 17, 23, 59, 59)}},
                #               {'siteId': company_list[i][2][j]}]})
                iplis = []
                for ipdata in allIP:
                    print(ipdata)
                    # break
                    iplis.append(ipdata['ip'])
                # # print(allIP)
                # print(iplis)
                # # break
                iplist = list(set(iplis))  # 去重
                # # print(Counter(iplist).items())
                # # print(iplist)
                # break
                ip_exist = db.IPSupplier.IPData.find({"ip": {"$in": iplist}})
                for ip in ip_exist:
                    print(ip)
                    break
                # for ip in iplist:
                #     print(ip)
                #     break
                    # ip_exist=db.IPSupplier.IPData.find({"ip":ip})
                    # for ip_exist_u in ip_exist:
                    #     print(ip_exist_u)
                    #     break
                #     print(ip_exist)
                #     break
                # if ip_exist==None:
                #     print(1)
                #     # not_companyLine_total+=1
                # else:
                #     print(ip_exist)
                #     break
                # companyLine_total+=1
            #
            # sheet['E' + str(i + 2)]=visitor_total
            # sheet['F' + str(i + 2)]=companyLine_total
            # sheet['G' + str(i + 2)]=not_companyLine_total

        #     iplist = list(set(iplist))
        #     for ip in iplist:
        #         ip_exist = db.IPSupplier.IPData.find_one({"ip": ip})
        #         if ip_exist == None:
        #             not_companyLine_total += 1
        #         else:
        #             companyLine_total += 1
        #
        # sheet['E' + str(i + 2)] = visitor_total
        # sheet['F' + str(i + 2)] = companyLine_total
        # sheet['G' + str(i + 2)] = not_companyLine_total
        #
        # file.save(filename)
        #
        #
        # company_list=[]
        # # result=list(cursor.fetchall())
        # # for ele in result:
        # #     company_list.append(list(ele))
        # #
        # # for ele in company_list:
        # #     siteid_list=[]
        # #     sql = f'''select id from org_sites where oid={ele[2]} '''
        # #     cursor.execute(sql)
        # #     siteid = cursor.fetchall()
        # #     for id in siteid:
        # #         siteid_list.append(id[0])
        # #     ele.append(siteid_list)
        # # print(company_list)
        # #
        # # for i in range(len(company_list)):
        # #     print(company_list[i])
        # #     sheet['A'+str(i+2)]=company_list[i][0]
        # #     sheet['B'+str(i+2)]=company_list[i][1]
        # #     sheet['C'+str(i+2)]=str(company_list[i][3])
        # #
        # #     #识别企业数
        # #     sql = f'''select count(DISTINCT ip_user) from site_visitor_identify where oid={company_list[i][2]} and ip_user!=''  '''
        # #     cursor.execute(sql)
        # #     num=cursor.fetchone()
        # #     sheet['D' + str(i + 2)]=num[0]
        # #
        # #
        # #     visitor_total=0
        # #     companyLine_total=0
        # #     not_companyLine_total = 0
        # #
        # #     for j in range(len(company_list[i][3])):
        # #         # 访客数
        # #         sql=f'''select count(DISTINCT visitor_id) from site_visitors where site_id={company_list[i][3][j]} and visitor_id!='' '''
        # #         cursor.execute(sql)
        # #         num=cursor.fetchone()
        # #         visitor_total+=num[0]
        #
        #         allIP=db.visitor.SiteVisitorLogging.find({"siteId":company_list[i][3][j]})
        #         # allIP=db.visitor.SiteVisitorLogging.find({'$and': [{'visitDate': {'$gte': datetime.datetime(2021, 9, 17, 00, 00, 00)}},
        #         #               {'visitDate': {'$lte': datetime.datetime(2021, 9, 17, 23, 59, 59)}},
        #         #               {'siteId': company_list[i][2][j]}]})
        #         iplist=[]
        #         for ipdata in allIP:
        #             iplist.append(ipdata['ip'])
        #         iplist=list(set(iplist))
        #         for ip in iplist:
        #             ip_exist=db.IPSupplier.IPData.find_one({"ip":ip})
        #             if ip_exist==None:
        #                 not_companyLine_total+=1
        #             else:
        #                 companyLine_total+=1
        #
        #     sheet['E' + str(i + 2)]=visitor_total
        #     sheet['F' + str(i + 2)]=companyLine_total
        #     sheet['G' + str(i + 2)]=not_companyLine_total
        #
        # file.save(filename)
