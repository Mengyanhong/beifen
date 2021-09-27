# @Time : 2021/9/27 17:41
# @Author : 孟艳红
# @File : test_count.py
from Visitors_identify.Configs.Pymysql import to_pymysql
import openpyxl
host = 'test'
pymysql = to_pymysql(host).pymysql()
cursor = pymysql.cursor()
a = ('1213','2')
filename='zhongq.xlsx'
file=openpyxl.load_workbook(filename)
sheet=file['统计']
class Test_count:
    def testsum(self):

        cursor.execute("""select oidlist.customer_name,oidlist.company_name,GROUP_CONCAT(org_sites.id separator ",")  from org_sites right join (select customer_name,company_name,oid from org_major_info where oid in (select oid from visitor_identify_account)) as oidlist  on org_sites.oid = oidlist.oid group by customer_name, company_name""")
        pymysql.commit()
        siteid = cursor.fetchall()
        # import  re
        # rule = '/d'
        for i in range(len(siteid)) :
            company_list=list(siteid[i])
            # print(company_list[0])
            sheet['A' + str(i + 2)] = company_list[0]
            sheet['B' + str(i + 2)] = company_list[1]
            sheet['C' + str(i + 2)] = str(company_list[2])
        file.save(filename)
        # print(siteid)
        # 识别企业数
        sql = f'''select count(DISTINCT ip_user) from site_visitor_identify where oid={company_list[i][2]} and ip_user!=''  '''
        cursor.execute(sql)
        num = cursor.fetchone()
        sheet['D' + str(i + 2)] = num[0]