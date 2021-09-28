# @Time : 2021/9/27 17:41
# @Author : 孟艳红
# @File : test_count.py
# import numbers

from Visitors_identify.Configs.Pymysql import to_pymysql
import openpyxl
from openpyxl.styles import Font, Fill
from openpyxl.styles.borders import Border, Side
host = 'test'
pymysql = to_pymysql(host).pymysql()
cursor = pymysql.cursor()
# a = '12,13'
# a.split(',')
filename = 'zhongq.xlsx'
file = openpyxl.load_workbook(filename)
sheet = file['统计']
thin_border = Border(left=Side(style='thin'),
                     right=Side(style='thin'),
                     top=Side(style='thin'),
                     bottom=Side(style='thin'))
# from openpyxl.styles import numbers #导入单元格数据类型格式设置模块
# sheet['C' + str(i + 2)] = company_list[2].number_format =numbers.FORMAT_DATE_XLSX15  #将数字类型转换为文本

class Test_count:
    def testsum(self):
        cursor.execute("""select co_list_sum.customer,co_list_sum.company,co_list_sum.id_list,count(DISTINCT site_visitor_identify.ip_user) as ip_user_sum,co_list_sum.vist_sum ,co_list_sum.oidli from (select oidlist.customer_name as customer,oidlist.company_name as company,GROUP_CONCAT(DISTINCT org_sites.id separator ",") as id_list, oidlist.oid as oidli, count(DISTINCT site_visitors.visitor_id) as vist_sum from site_visitors right join org_sites on site_visitors.site_id = org_sites.id right join (select customer_name,company_name,oid from org_major_info where oid in (select oid from visitor_identify_account)) as oidlist  on org_sites.oid = oidlist.oid  group by  customer,company,oidli ) as co_list_sum left join site_visitor_identify on co_list_sum.oidli=site_visitor_identify.oid  group by co_list_sum.customer,co_list_sum.company,co_list_sum.oidli
""")
        pymysql.commit()
        siteid = cursor.fetchall()
        # import  re
        # rule = '/d'
        for i in range(len(siteid)):
            company_list = siteid[i]
            print(company_list)
            if company_list[2]:
                print(company_list)
                print(company_list[2].split(','))
        #     sheet['A' + str(i + 2)] = company_list[0]
        #     sheet['B' + str(i + 2)] = company_list[1]
        #     sheet['C' + str(i + 2)] = company_list[2]
        #     sheet['D' + str(i + 2)] = company_list[3]
        #     sheet['E' + str(i + 2)] = company_list[4]
        # file.save(filename)
        # print(siteid)
        # 识别企业数
        # sql = f'''select count(DISTINCT ip_user) from site_visitor_identify where oid={company_list[i][2]} and ip_user!=''  '''
        # cursor.execute(sql)
        # num = cursor.fetchone()
        # sheet['D' + str(i + 2)] = num[0]
