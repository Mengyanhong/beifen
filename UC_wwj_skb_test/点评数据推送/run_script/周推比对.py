# -*- coding: utf-8 -*-
import pymongo,sys
from sshtunnel import SSHTunnelForwarder
import openpyxl, datetime
ssh_pkey_path = sys.argv[0].split("home")[0]
print(f'{ssh_pkey_path}home/.ssh/id_rsa')
print('请先把文件转化为Excel后缀为 .xlsx，不要改文件名')
filename = input('请复制文件名称：')
# 例：filename='YEXT123456_2020-06-29'

filepath = f"D:/Excel/{filename}.xlsx"
file = openpyxl.load_workbook(filepath)

print('检查detail sheet---')
sheet = file['detail']
column_name = ['C', 'D', 'E', 'F', 'G', 'H', 'I']
# 计算出列表的长度

i = 2
while sheet['A' + str(i)].value != None:
    i = i + 1
length = i - 2
# print(length)

print('case1---检测表格中字段是否正确')
if sheet['A1'].value != '店铺ID':
    print('列A字段名不是店铺ID')
for i in range(2, length + 2):
    if str(sheet['A' + str(i)].value).isdigit() != True:
        print(sheet['A' + str(i)].value)
        print('第' + str(i) + '行店铺ID的值非数字')
if sheet['B1'].value != '店铺名称':
    print('列B字段名不是店铺名称')

print('case2---检测表格中字段是否正确')
file_date = filename[11:15] + '-' + filename[16:18] + '-' + filename[19:21]
year = int(filename[11:15])
month = int(filename[16:18].lstrip('0'))
day = int(filename[19:21].lstrip('0'))
date_list = [(datetime.date(year, month, day) - datetime.timedelta(7)),
             (datetime.date(year, month, day) - datetime.timedelta(6)),
             (datetime.date(year, month, day) - datetime.timedelta(5)),
             (datetime.date(year, month, day) - datetime.timedelta(4)),
             (datetime.date(year, month, day) - datetime.timedelta(3)),
             (datetime.date(year, month, day) - datetime.timedelta(2)),
             (datetime.date(year, month, day) - datetime.timedelta(1))]
date_list1 = [(datetime.date(year, month, day) - datetime.timedelta(14)),
              (datetime.date(year, month, day) - datetime.timedelta(13)),
              (datetime.date(year, month, day) - datetime.timedelta(12)),
              (datetime.date(year, month, day) - datetime.timedelta(11)),
              (datetime.date(year, month, day) - datetime.timedelta(10)),
              (datetime.date(year, month, day) - datetime.timedelta(9)),
              (datetime.date(year, month, day) - datetime.timedelta(8))]
for i in range(7):
    if sheet[column_name[i] + '1'].value != str(date_list[i]):
        print('列' + column_name[i] + '字段名错误--日期错误')

print('case3---数据正确性检测-抽查和数据库是否一致')
# 连接数据库
mongo_port = 3717
mongo_address = "dds-m5ed9ea9d9a653b41.mongodb.rds.aliyuncs.com"
mongo_user = 'enterprise_read'
mongo_password = 'CuOIdrN4j7S1OI6Ds8gT'
server = SSHTunnelForwarder(
    ssh_address_or_host=("47.104.226.30", 40022),  # 指定ssh登录的跳转机的IP port
    ssh_username='jar',  # 跳板机用户名
    ssh_pkey=f'{ssh_pkey_path}home/.ssh/id_rsa',  # 设置密钥
    remote_bind_address=(mongo_address, mongo_port)  # 设置数据库服务地址及端口
)
server.start()
conn = pymongo.MongoClient(
    host='127.0.0.1',  # host、port 固定
    port=server.local_bind_port
)

db = conn["admin"]
db.authenticate(mongo_user, mongo_password)

# 仅检测前1000条数据，因为后面的数据大都为0或空
if length >= 1000:
    check_row = 1000
else:
    check_row = length

sum_0andnone1 = 0
sum_0andnone2 = 0
sum_0andnone3 = 0
sum_0andnone4 = 0
sum_0andnone5 = 0
sum_0andnone6 = 0
sum_0andnone7 = 0
# 统计每天0和空的总量，若超过500算异常
sum_0andnone = [sum_0andnone1, sum_0andnone2, sum_0andnone3, sum_0andnone4, sum_0andnone5, sum_0andnone6, sum_0andnone7]
for i in range(2, check_row + 2):
    res = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list[0])})
    re = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list1[0])})
    res1 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list[1])})
    re1 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list1[1])})
    res2 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list[2])})
    re2 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list1[2])})
    res3 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list[3])})
    re3 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list1[3])})
    res4 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list[4])})
    re4 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list1[4])})
    res5 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list[5])})
    re5 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list1[5])})
    res6 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list[6])})
    re6 = conn.twinbeeStorage.DianpingTraffic.find_one(
        {'shopId': str(sheet['A' + str(i)].value), 'date': str(date_list1[6])})
    # if None==res==res1==res2==res3==res4==res5==res6:
    #     if None==re==re1==re2==re3==re4==re5==re6:
    #         print('数据和上周相同都为None')
    #     elif 0==re==re1==re2==re3==re4==re5==re6:
    #         print('本周数据为None，上周数据为0')
    #         print(str(sheet['A' + str(i)].value) + '店铺ID')
    #     elif re==re1==re2==re3==re4==re5==re6!=None and re==re1==re2==re3==re4==re5==re6!=0:
    #         print('上周有数据这周无数据')
    #         print(str(sheet['A' + str(i)].value)+'数据错误')
    # else:
    #     if 0 == res == res1 == res2 == res3 == res4 == res5 == res6:
    #         if 0 == re == re1 == re2 == re3 == re4 == re5 == re6:
    #             print('数据和上周相同都为0')
    #         elif None == re == re1 == re2 == re3 == re4 == re5 == re6:
    #             print('本周数据为0，上周数据为None')
    #             print(str(sheet['A' + str(i)].value) + '店铺ID')
    #         elif re == re1 == re2 == re3 == re4 == re5 == re6 != None and re == re1 == re2 == re3 == re4 == re5 == re6 != 0:
    #             print('上周有数据这周无数据')
    #             print(str(sheet['A' + str(i)].value) + '数据错误')
    res7 = [res, res1, res2, res3, res4, res5, res6]
    re7 = [re, re1, re2, re3, re4, re5, re6]
    res_lin = 0
    re_lin = 0
    for j in range(7):
        if res7[j] == None:
            sum_0andnone[j] += 1
            res_lin += 1
            if re7[j] == None:
                re_lin += 1
            if sheet[column_name[j] + str(i)].value != None:
                print(column_name[j] + str(i) + '值错误')
        else:
            if str(sheet[column_name[j] + str(i)].value) == '0' or sheet[column_name[j] + str(i)].value == None:
                sum_0andnone[j] += 1
                res_lin += 1
            if (re7[j]) == None or (re7[j])['scale']['pv']['oneSelf'] == '0':
                re_lin += 1
            if str(sheet[column_name[j] + str(i)].value) != (res7[j])['scale']['pv']['oneSelf']:
                print('\n' + '第' + (column_name[j] + str(i)) + '列值错误，数据库数值' + (res7[j])['scale']['pv']['oneSelf'] +
                      '表格数值' + str(sheet[column_name[j] + str(i)].value))
                # print('上周数值', (re7[j])['scale']['pv']['oneSelf'])
                print('店铺ID', str(sheet['A' + str(i)].value))
    # print('本周有', + res_lin , '天数据为0，上周有', + re_lin ,'天数据为0，店铺ID为', str(sheet['A'+str(i)].value))
    # if res_lin == re_lin == 7:
    #     print('\n本周数据和上周相同，本周',+ res_lin,'天数据为0，上周',+ re_lin,'天数据为0,数据店铺ID为',str(sheet['A'+str(i)].value))
    if res_lin == 7 and re_lin != 7:
        print('\n本周无数据上周有数据，本周', + res_lin, '天数据为0，上周', + re_lin, '天数据为0,数据店铺ID为', str(sheet['A' + str(i)].value))
    # elif res_lin != 7 and re_lin == 7:
    #     print('\n本周有数据上周无数据，本周',+ res_lin,'天数据为0，上周',+ re_lin,'天数据为0,数据店铺ID为',str(sheet['A'+str(i)].value))
    # elif 3 <= res_lin < 7 and 3 <= re_lin < 7:
    #     print('\n本周和上周数据均有超过3天的数据为0，本周',+ res_lin,'天数据为0，上周',+ re_lin,'天数据为0,数据店铺ID为',str(sheet['A'+str(i)].value))
    elif 3 < res_lin < 7 and re_lin < 4:
        print('\n本周有超过4天为0的数据，本周', + res_lin, '天数据为0，上周', + re_lin, '天数据为0,数据店铺ID为', str(sheet['A' + str(i)].value))

print("\n判断前1000条数据中有没有超过500的0或空")
for s in range(7):
    if sum_0andnone[s] >= 500:
        print(column_name[s] + '列前1000条数据中有超过500的0或空')

conn.close()
server.close()

print('检查sum sheet---')
sheet_sum = file['sum']

print('case1---字段名及值的检测')
if sheet_sum['A1'].value != '店铺的总量':
    print('A1字段名不是店铺的总量')
if sheet_sum['B1'].value != length:
    print('店铺总量 值错误')

print('case2---字段名及值的检测')
if sheet_sum['A2'].value != '空白店铺的总量':
    print('A2字段名不是空白店铺的总量')
temp = 2  # 定义一个临时变量，找出每列中第一个值为None的行
for i in range(7):
    for j in range(temp, length + 2):
        if sheet[column_name[i] + str(j)].value == None:
            temp = j
            break
if sheet_sum['B2'].value != length - temp + 2:
    print('空白店铺的总量 值错误')

print('case3---字段名及值的检测')
if sheet_sum['A3'].value != '一周店铺的浏览量的总量':
    print('A3字段名不是一周店铺的浏览量的总量')
sum = 0
for i in range(7):
    for j in range(2, length + 2):
        if sheet[column_name[i] + str(j)].value == None:
            sheet[column_name[i] + str(j)].value = 0
        sum = int(sheet[column_name[i] + str(j)].value) + sum
if sheet_sum['B3'].value != sum:
    print('一周店铺的浏览量的总量 值错误')
