import pymongo
from sshtunnel import SSHTunnelForwarder
import openpyxl,datetime

# print('请先把文件转化为Excel后缀为 .xlsx，不要改文件名')
# filename=input('请复制文件名称：')
# # 例：filename='DIANPING_ANALYTICS_2020_07_02'广州科技职业技术学院
# filepath=r'C:\\Users\\92110\\Desktop\\datacheck\\'+filename+'.xlsx'
filepath =r'D:/Users/yue tui/Yext-WWJ数据提供需求--Dianping ID-1019-店铺状态.xlsx'
file=openpyxl.load_workbook(filepath)
sheet=file["Yext-WWJ数据提供需求--Dianping ID-101"]
i=2
while sheet['A'+str(i)].value!=None:
    i=i+1
length=i-2
print(length)
#检查表格中得字段名称是否正确
print('case1---')
if sheet['A1'].value!='店铺数字id':
    print('列A字段名不是店铺数字id')
for i in range(2,length+2):
    if str(sheet['A' + str(i)].value).isdigit()!=True:
        print(sheet['A' + str(i)].value)
        print('第'+str(i)+'行shop_id的值非数字')

print('case2---')
if sheet['B1'].value!='店铺字母id':
    print('列B字段名不是店铺字母id')
print('case3---')
if sheet['C1'].value!='店铺状态':
    print('列C字段名不是店铺状态')

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

print('case4---')
# check_row=[2,int(length/100),int(length/20),int(length/2),int(length/50),length+1]
for i in range(2,length):
    res = conn.twinbeeStorage.DazhongDianping.find_one({'shopId':str(sheet['A'+str(i)].value)})
    # print(res)
    check_column = ['A', 'C']
    check_field = [res['shopId'],res['status']]
    # print(check_field)
    for j in range(2):
        if str(sheet[str(check_column[j])+str(i)].value)!=check_field[j]:
            print('shopId'+str(sheet[str(check_column[j])+str(i)])+'的'+check_field[j]+'值错误')

conn.close()
server.close()
