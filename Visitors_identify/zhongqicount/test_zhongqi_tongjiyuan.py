import pytest,openpyxl,datetime

filename= 'data_report/zhongqi.xlsx'
file=openpyxl.load_workbook(filename)
sheet=file['统计']

# begin='2021-09-17 00:00:00'
# end='2021-09-17 23:59:59'

class TestTongji:
    def test_companyname(self,sql,mongoDB):
        cursor=sql
        db = mongoDB
        # sql='''SELECT customer_name,company_name,org_major_info.oid from org_major_info right join visitor_identify_account
        #         on org_major_info.oid=visitor_identify_account.oid
        #         where visitor_identify_account.create_time BETWEEN '2021-09-17 00:00:00' and '2021-09-17 23:59:59' '''
        sql = '''SELECT customer_name,company_name,org_major_info.oid from org_major_info right join visitor_identify_account 
                        on org_major_info.oid=visitor_identify_account.oid '''
        cursor.execute(sql)
        company_list=[]
        result=list(cursor.fetchall())
        for ele in result:
            company_list.append(list(ele))

        for ele in company_list:
            siteid_list=[]
            sql = f'''select id from org_sites where oid={ele[2]} '''
            cursor.execute(sql)
            siteid = cursor.fetchall()
            for id in siteid:
                siteid_list.append(id[0])
            ele.append(siteid_list)
        print(company_list)

        for i in range(len(company_list)):
            print(company_list[i])
            sheet['A'+str(i+2)]=company_list[i][0]
            sheet['B'+str(i+2)]=company_list[i][1]
            sheet['C'+str(i+2)]=str(company_list[i][3])

            #识别企业数
            sql = f'''select count(DISTINCT ip_user) from site_visitor_identify where oid={company_list[i][2]} and ip_user!=''  '''
            cursor.execute(sql)
            num=cursor.fetchone()
            sheet['D' + str(i + 2)]=num[0]


            visitor_total=0
            companyLine_total=0
            not_companyLine_total = 0

            for j in range(len(company_list[i][3])):
                # 访客数
                sql=f'''select count(DISTINCT visitor_id) from site_visitors where site_id={company_list[i][3][j]} and visitor_id!='' '''
                cursor.execute(sql)
                num=cursor.fetchone()
                visitor_total+=num[0]

                allIP=db.visitor.SiteVisitorLogging.find({"siteId":company_list[i][3][j]})
                # allIP=db.visitor.SiteVisitorLogging.find({'$and': [{'visitDate': {'$gte': datetime.datetime(2021, 9, 17, 00, 00, 00)}},
                #               {'visitDate': {'$lte': datetime.datetime(2021, 9, 17, 23, 59, 59)}},
                #               {'siteId': company_list[i][2][j]}]})
                iplist=[]
                for ipdata in allIP:
                    iplist.append(ipdata['ip'])
                iplist=list(set(iplist))
                for ip in iplist:
                    ip_exist=db.IPSupplier.IPData.find_one({"ip":ip})
                    if ip_exist==None:
                        not_companyLine_total+=1
                    else:
                        companyLine_total+=1

            sheet['E' + str(i + 2)]=visitor_total
            sheet['F' + str(i + 2)]=companyLine_total
            sheet['G' + str(i + 2)]=not_companyLine_total

        file.save(filename)



