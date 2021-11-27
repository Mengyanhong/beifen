
import pytest, openpyxl, datetime,time

filename = 'data_report/9月29号0点-10月14号12点.xlsx'
file = openpyxl.load_workbook(filename)
sheet = file['统计']


# b=time.`
# end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# begin='2021-09-17 00:00:00'
# end='2021-09-17 23:59:59'

class TestTongji:
    def test_companyname(self, sql, mongoDB):
        cursor = sql
        db = mongoDB
        cursor.execute("""select customer_n1,company_n1,GROUP_CONCAT(set_id11 separator ","),sum(ip_user_sum),SUM(visitor_id_sum1),oidl21,list.visitor_id_sum_list_org_id from
         (select customer_n as customer_n1,company_n as company_n1,oidl2 as oidl21,set_id1 as set_id11,visitor_id_sum as visitor_id_sum1, 
         COUNT(DISTINCT site_visitor_identify.ip_user) as ip_user_sum,visitor_id_sum_list.set_org_id as visitor_id_sum_list_org_id from  
         (select customer_na as customer_n,company_na as company_n,oidl1 as oidl2,set_id as set_id1 ,COUNT(DISTINCT site_visitors.visitor_id) as
          visitor_id_sum,set_list.oid_org_id as set_org_id,site_visitors.create_time from (select oidlist.customer_nam as customer_na,oidlist.company_nam as
           company_na,oidlist.oidl as oidl1,org_sites.id as set_id,oidlist.org_id as oid_org_id from org_sites  right join (select org_major_info.customer_name as
            customer_nam ,org_major_info.company_name as company_nam,org_major_info.oid as oidl,org_major_info.id as org_id  from org_major_info right join
             visitor_identify_account on visitor_identify_account.oid = org_major_info.oid  group by customer_nam,company_nam,oidl,org_id  order by org_id) as
              oidlist  on org_sites.oid = oidlist.oidl  group by customer_na,company_na,oidl1,set_id,oid_org_id order by oid_org_id) as set_list left join
               site_visitors on set_list.set_id = site_visitors.site_id group by customer_n,company_n,oidl2,set_id1,set_org_id order by set_org_id asc ) as
                visitor_id_sum_list left join site_visitor_identify on visitor_id_sum_list.set_id1 = site_visitor_identify.site_id group by
                 customer_n1,company_n1,oidl21,set_id11,visitor_id_sum1,visitor_id_sum_list_org_id order by visitor_id_sum_list_org_id asc) as list group by
                  customer_n1,company_n1 order by list.visitor_id_sum_list_org_id asc""")
        # pymysql.commit()
        siteid = cursor.fetchall()
        # import  re
        # rule = '/d'
        cursor.execute("""select customer_n1,company_n1,GROUP_CONCAT(set_id11 separator ","),sum(ip_user_sum),SUM(visitor_id_sum1),oidl21,list.visitor_id_sum_list_org_id from
         (select customer_n as customer_n1,company_n as company_n1,oidl2 as oidl21,set_id1 as set_id11,visitor_id_sum as visitor_id_sum1, 
         COUNT(DISTINCT site_visitor_identify.ip_user) as ip_user_sum,visitor_id_sum_list.set_org_id as visitor_id_sum_list_org_id from  (
         select customer_na as customer_n,company_na as company_n,oidl1 as oidl2,set_id as set_id1 ,COUNT(DISTINCT site_visitors.visitor_id) as
          visitor_id_sum,set_list.oid_org_id as set_org_id,site_visitors.create_time from (select oidlist.customer_nam as customer_na,oidlist.company_nam as
           company_na,oidlist.oidl as oidl1,org_sites.id as set_id,oidlist.org_id as oid_org_id from org_sites  right join (select org_major_info.customer_name as
            customer_nam ,org_major_info.company_name as company_nam,org_major_info.oid as oidl,org_major_info.id as org_id  from org_major_info right join
             visitor_identify_account on visitor_identify_account.oid = org_major_info.oid  group by customer_nam,company_nam,oidl,org_id  order by org_id) as
              oidlist  on org_sites.oid = oidlist.oidl  group by customer_na,company_na,oidl1,set_id,oid_org_id order by oid_org_id) as set_list left join
               site_visitors on set_list.set_id = site_visitors.site_id where site_visitors.create_time between '2021-09-29 00:00:00' and '2021-10-14 12:00:00' group by
                customer_n,company_n,oidl2,set_id1,set_org_id order by set_org_id asc ) as visitor_id_sum_list left join
                 site_visitor_identify on visitor_id_sum_list.set_id1 = site_visitor_identify.site_id where
                  site_visitor_identify.create_time between '2021-09-29 00:00:00' and '2021-10-14 12:00:00' group by
                   customer_n1,company_n1,oidl21,set_id11,visitor_id_sum1,visitor_id_sum_list_org_id order by visitor_id_sum_list_org_id asc) as
                    list group by customer_n1,company_n1 order by list.visitor_id_sum_list_org_id asc""")
        siteid_sum = cursor.fetchall()
        for i in range(len(siteid)):
            company_list = siteid[i]
            company_list_sum = 0
            for j in siteid_sum:
                if company_list[5] == j[5]:
                    company_list_sum += 1
                    sheet['A' + str(i + 2)] = j[0]
                    sheet['B' + str(i + 2)] = j[1]
                    sheet['C' + str(i + 2)] = company_list[2]
                    sheet['D' + str(i + 2)] = j[3]
                    sheet['E' + str(i + 2)] = j[4]
                    siteId_list = j[2].split(',')
                    siteId_list_find = []
                    for siteId_list_id in siteId_list:
                        siteId_list_find.append(int(siteId_list_id))
                    # allIP = db.visitor.SiteVisitorLogging.find({"siteId": {'$in': siteId_list_find}}, {"ip": 1})
                    allIP = db.visitor.SiteVisitorLogging.find({'$and': [{'createDate': {
                        '$gte': datetime.datetime(2021, 9, 29, 00, 00, 00),
                        '$lte': datetime.datetime(2021, 10, 14, 12, 00, 00)}},
                                                                         {"siteId": {'$in': siteId_list_find}}]},
                                                               {"ip": 1})
                    # allIP=db.visitor.SiteVisitorLogging.find({'$and': [{'visitDate': {'$gte': datetime.datetime(2021, 9, 17, 00, 00, 00)}},
                    #               {'visitDate': {'$lte': datetime.datetime(2021, 9, 17, 23, 59, 59)}},
                    #               {'siteId': company_list[i][2][j]}]})
                    iplis = []
                    for ipdata in allIP:
                        iplis.append(ipdata['ip'])
                    iplist = list(set(iplis))
                    # iplist = iplis
                    ip_exist_sum = 0
                    for index in range(0, len(iplist), 2000):
                        item_list = iplist[index:index + 2000]
                        ip_exist = db.IPSupplier.IPData.find({"ip": {'$in': item_list}}, {"ip": 1})
                        for ip_exist_list in ip_exist:
                            if ip_exist_list:
                                ip_exist_sum += 1
                    if ip_exist_sum == 0:
                        sheet['F' + str(i + 2)] = 0
                        sheet['G' + str(i + 2)] = len(iplist)
                    else:
                        sheet['F' + str(i + 2)] = ip_exist_sum
                        sheet['G' + str(i + 2)] = len(iplist) - ip_exist_sum
                    break
            if company_list_sum == 0:
                sheet['A' + str(i + 2)] = company_list[0]
                sheet['B' + str(i + 2)] = company_list[1]
                sheet['C' + str(i + 2)] = company_list[2]
                sheet['D' + str(i + 2)] = 0
                sheet['E' + str(i + 2)] = 0
                sheet['G' + str(i + 2)] = 0
                sheet['F' + str(i + 2)] = 0
        file.save(filename)
