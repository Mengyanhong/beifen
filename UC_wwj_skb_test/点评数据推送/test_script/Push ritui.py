# -*- coding: utf-8 -*-
import pymongo
from sshtunnel import SSHTunnelForwarder
import openpyxl,datetime

print('请先把文件转化为Excel后缀为 .xlsx，不要改文件名')
filename=input('请复制文件名称：')
# 例：filename='DIANPING_ANALYTICS_2020_07_02'广州科技职业技术学院

filepath=r'D:/Users/ri tui/'+filename+'.xlsx'
file=openpyxl.load_workbook(filepath)
sheet=file[filename]

#计算出列表的长度
i=2
while sheet['A'+str(i)].value!=None:
    i=i+1
length=i-2


#检测表格中字段是否正确
print('case1---')
if sheet['A1'].value!='shop_id':
    print('列A字段名不是shop_id')
for i in range(2,length+2):
    if str(sheet['A' + str(i)].value).isdigit()!=True:
        print(sheet['A' + str(i)].value)
        print('第'+str(i)+'行shop_id的值非数字')

print('case2---')
if sheet['B1'].value!='date':
    print('列B字段名不是date')
file_date=filename[19:23]+'-'+filename[24:26]+'-'+filename[27:29]
year=int(filename[19:23])
month=int(filename[24:26].lstrip('0'))
day=int(filename[27:29].lstrip('0'))
actual_date=(datetime.date(year,month,day)-datetime.timedelta(7))
if str(sheet['B2'].value)[:10]!=str(actual_date):
    print('date的值错误')

print('case3---')
if sheet['C1'].value!='platformType':
    print('列C字段名不是platformType')
for i in range(2,length+2):
    if sheet['C' + str(i)].value!=0:
        print('第'+str(i)+'行platformType的值非0')

print('case 4 &6 &8 &10 &12 ---')
field_name=['unique_views_peer_average','profile_views_peer_average','stay_duration_peer_average','jump_rate_peer_average',
            'reviews','reviews_industry','directions_phone_calls','directions_phone_calls_industry']
column_name=['D','G','J','M','P','Q','R','S']
for i in range(len(field_name)):
    if sheet[column_name[i]+'1'].value!=field_name[i]:
        print('列'+column_name[i]+'字段名不是'+field_name[i])
    for j in range(2,length+2):
        if sheet[column_name[i]+str(j)].value!=None:
            print('第'+str(j)+'行'+field_name[i]+'的值非空')

print('case5 &7 &9 &11---')
field_name=['unique_views_peer_excellent','unique_views_self','profile_views_peer_excellent','profile_views_self',
            'stay_duration_peer_excellent','stay_duration_self','jump_rate_peer_excellent','jump_rate_self']
column_name=['E','F','H','I','K','L','N','O']
for i in range(len(field_name)):
    if sheet[column_name[i]+'1'].value!=field_name[i]:
        print('列'+column_name[i]+'字段名不是'+field_name[i])
    for j in range(2,length+2):
        if '.' not in str(sheet[column_name[i]+str(j)].value):
            if str(sheet[column_name[i]+str(j)].value).isdigit()!=True:
                print('第'+str(j)+'行'+field_name[i]+'的值非数字')
        else:
            temp=str(sheet[column_name[i]+str(j)].value).split('.')
            value=temp[0]+temp[1]
            if str(value).isdigit()!=True:
                print('第' + str(j) + '行' + field_name[i] + '的值非数字')

#连接数据库
mongo_port = 3717
mongo_address = "dds-m5e44df0967967a42.mongodb.rds.aliyuncs.com"
mongo_user = 'enterprise_read'
mongo_password = 'Ce782ef2'
server = SSHTunnelForwarder(

    ssh_address_or_host=("47.104.226.30", 40022),  # 指定ssh登录的跳转机的IP port
    ssh_username='jar',  # 跳板机用户名
    ssh_pkey='C:/Users/admin/.ssh/id_rsa/id_rsa',  # 设置密钥
    remote_bind_address=(mongo_address, mongo_port)  # 设置数据库服务地址及端口
)
server.start()
conn = pymongo.MongoClient(
    host='127.0.0.1',  # host、port 固定
    port=server.local_bind_port
)

db = conn["twinbeeStorage"]
db.authenticate(mongo_user, mongo_password)

print('case13 &14 &15 &16 &17---')
check_row=[2,int(length/100),int(length/20),int(length/2),length+1]

for i in range(len(check_row)):
    res = conn.twinbeeStorage.DianpingTraffic.find_one({'shopId':str(sheet['A'+str(check_row[i])].value),'date':str(actual_date)})
    # print(res)
    check_column = ['E', 'F', 'H', 'I', 'K', 'L', 'N', 'O']
    check_field = [res['scale']['uv']['peerExcellent'],res['scale']['uv']['oneSelf'],
                   res['scale']['pv']['peerExcellent'],res['scale']['pv']['oneSelf'],
                   res['quality']['stayDuration']['peerExcellent'], res['quality']['stayDuration']['oneSelf'],
                   res['quality']['jumpRate']['peerExcellent'], res['quality']['jumpRate']['oneSelf']]
    for j in range(8):
        if str(sheet[check_column[j]+str(check_row[i])].value)!=check_field[j]:
            print('shopId'+sheet['A'+str(check_row[i])]+'的'+check_field[j]+'值错误')
"""遍历整个表格"""
for i in range(2,length):
    res = conn.twinbeeStorage.DianpingTraffic.find_one({'shopId':str(sheet['A'+str(i)].value),'date':str(actual_date)})
    # print(res)
    check_column = ['E', 'F', 'H', 'I', 'K', 'L', 'N', 'O']
    check_field = [res['scale']['uv']['peerExcellent'],res['scale']['uv']['oneSelf'],
                   res['scale']['pv']['peerExcellent'],res['scale']['pv']['oneSelf'],
                   res['quality']['stayDuration']['peerExcellent'], res['quality']['stayDuration']['oneSelf'],
                   res['quality']['jumpRate']['peerExcellent'], res['quality']['jumpRate']['oneSelf']]
    for j in range(8):
        if str(sheet[check_column[j]+str(i)].value)!=check_field[j]:
            print(str(i) + ' 行的 '+ str(check_column[j]) + ' 列值错误 ,应是'+ str(check_field[j]))
            # print(i,j)

conn.close()
server.close()





