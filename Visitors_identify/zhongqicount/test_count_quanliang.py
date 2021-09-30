import pytest,openpyxl,datetime

filename='quanliang.xlsx'
file=openpyxl.load_workbook(filename)
sheet=file['统计']

# begin='2021-09-17 00:00:00'
# end='2021-09-17 23:59:59'

class TestTongji:
    def test_companyname(self,sql,mongoDB):
        cursor=sql
        db = mongoDB
        cursor.execute("""select customer_n1,company_n1,GROUP_CONCAT(set_id11 separator ","),sum(ip_user_sum),SUM(visitor_id_sum1),oidl21 from (select customer_n as customer_n1,company_n as company_n1,oidl2 as oidl21,set_id1 as set_id11,visitor_id_sum as visitor_id_sum1, COUNT(DISTINCT site_visitor_identify.ip_user) as ip_user_sum from  (select customer_na as customer_n,company_na as company_n,oidl1 as oidl2,set_id as set_id1 ,COUNT(DISTINCT site_visitors.visitor_id) as visitor_id_sum from (select oidlist.customer_nam as customer_na,oidlist.company_nam as company_na,oidlist.oidl as oidl1,org_sites.id as set_id from org_sites  right join  (select org_major_info.customer_name as customer_nam ,org_major_info.company_name as company_nam,org_major_info.oid as oidl from org_major_info right join visitor_identify_account on visitor_identify_account.oid = org_major_info.oid group by customer_nam,company_nam,oidl) as oidlist  on org_sites.oid = oidlist.oidl  group by customer_na,company_na,oidl1,set_id) as set_list 
        left join site_visitors on set_list.set_id = site_visitors.site_id group by customer_n,company_n,oidl2,set_id1 ) as visitor_id_sum_list left join site_visitor_identify on visitor_id_sum_list.set_id1 = site_visitor_identify.site_id  group by customer_n1,company_n1,oidl21,set_id11,visitor_id_sum1) as list group by customer_n1,company_n1
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
            if company_list[2]:
                siteId_list = company_list[2].split(',')
                siteId_list_find = []
                for siteId_list_id in siteId_list:
                    siteId_list_find.append(int(siteId_list_id))
                allIP = db.visitor.SiteVisitorLogging.find({"siteId": {'$in': siteId_list_find}}, {"ip": 1})
                # allIP=db.visitor.SiteVisitorLogging.find({'$and': [{'visitDate': {'$gte': datetime.datetime(2021, 9, 17, 00, 00, 00)}},
                #               {'visitDate': {'$lte': datetime.datetime(2021, 9, 17, 23, 59, 59)}},
                #               {'siteId': company_list[i][2][j]}]})
                iplis = []
                for ipdata in allIP:
                    iplis.append(ipdata['ip'])
                iplist = list(set(iplis))
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
            else:
                sheet['F' + str(i + 2)] = 0
                sheet['G' + str(i + 2)] = 0
        file.save(filename)