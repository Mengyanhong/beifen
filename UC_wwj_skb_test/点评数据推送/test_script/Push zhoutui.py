# -*- coding: utf-8 -*-
import pymongo
from sshtunnel import SSHTunnelForwarder
import openpyxl,datetime
import random
import time

def test():

    print('请先把文件转化为Excel后缀为 .xlsx，不要改文件名')
    filename=input('请复制文件名称：')
    # 例：filename='YEXT123456_2020-06-29'

    filepath=r'D:/Users/zhou tui/'+filename+'.xlsx'
    file=openpyxl.load_workbook(filepath)

    print('检查detail sheet---')
    sheet=file['detail']
    column_name=['C','D','E','F','G','H','I']
    #计算出列表的长度
    i=2
    while sheet['A'+str(i)].value!=None:
        i=i+1
    length=i-2
    # print(length)

    #检测表格中字段是否正确
    print('case1---')
    if sheet['A1'].value!='店铺ID':
        print('列A字段名不是店铺ID')
    for i in range(2,length+2):
        if str(sheet['A' + str(i)].value).isdigit()!=True:
            print(sheet['A' + str(i)].value)
            print('第'+str(i)+'行店铺ID的值非数字')

    if sheet['B1'].value!='店铺名称':
        print('列B字段名不是店铺名称')

    print('case2---')
    file_date=filename[11:15]+'-'+filename[16:18]+'-'+filename[19:21]
    year=int(filename[11:15])
    month=int(filename[16:18].lstrip('0'))
    day=int(filename[19:21].lstrip('0'))
    date_list=[(datetime.date(year,month,day)-datetime.timedelta(7)),(datetime.date(year,month,day)-datetime.timedelta(6)),
               (datetime.date(year,month,day)-datetime.timedelta(5)),(datetime.date(year,month,day)-datetime.timedelta(4)),
               (datetime.date(year,month,day)-datetime.timedelta(3)),(datetime.date(year,month,day)-datetime.timedelta(2)),
               (datetime.date(year,month,day)-datetime.timedelta(1))]
    for i in range(7):
        if sheet[column_name[i]+'1'].value!=str(date_list[i]):
            print('列'+column_name[i]+'字段名错误--日期错误')

    print('case3---')
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

    check_row=[2,int(length/100),int(length/10),int(length/5),int(length/2),int(3*length/4),length+1]
    for i in range(len(check_row)):
        res = conn.twinbeeStorage.DianpingTraffic.find_one({'shopId':str(sheet['A'+str(check_row[i])].value),'date':str(date_list[i])})
        if res==None:
            if sheet[column_name[i]+str(check_row[i])].value!=None:
               print(column_name[i]+str(check_row[i])+'值错误')
        else:
            if str(sheet[column_name[i]+str(check_row[i])].value)!=res['scale']['pv']['oneSelf']:
                print(column_name[i]+str(check_row[i])+'值错误!')

    res = conn.twinbeeStorage.DianpingTraffic.find_one({'shopId':str(125241295),'date':str("2020-08-30")})

    conn.close()
    server.close()


    print('检查sum sheet---')
    sheet_sum=file['sum']

    print('case1---')
    if sheet_sum['A1'].value!='店铺的总量':
        print('A1字段名不是店铺的总量')
    if sheet_sum['B1'].value!=length:
        print('店铺总量 值错误')

    print('case2---')
    if sheet_sum['A2'].value!='空白店铺的总量':
        print('A2字段名不是空白店铺的总量')
    temp=2 #定义一个临时变量，找出每列中第一个值为None的行
    for i in range(7):
        for j in range(temp,length+2):
            if sheet[column_name[i]+str(j)].value==None:
                temp=j
                break
    if sheet_sum['B2'].value!=length-temp+2:
        print('空白店铺的总量 值错误')

    print('case3---')
    if sheet_sum['A3'].value!='一周店铺的浏览量的总量':
        print('A3字段名不是一周店铺的浏览量的总量')
    sum=0
    for i in range(7):
        for j in range(2,length+2):
            if sheet[column_name[i]+str(j)].value==None:
                sheet[column_name[i]+str(j)].value=0
            sum=int(sheet[column_name[i]+str(j)].value)+sum
    if sheet_sum['B3'].value!=sum:
        print('一周店铺的浏览量的总量 值错误')

    checkdate=[]

    for i in range(7):
        noneData = 0
        lst = get_random_list(2, 1000, 500)
        for j in lst:
            if sheet[column_name[i]+str(j)].value==None or sheet[column_name[i]+str(j)].value==0:
                noneData=noneData+1
        if noneData/100>0.5:
            checkdate.append(str(date_list[i]))
    print("不符合的日期")
    print(checkdate)

def get_random_list(start,stop,n):
    '''
    生成范围在[start,stop], 长度为n的数组.
    区间包含左右endpoint
    '''
    arr = list(range(start, stop+1))
    shuffle_n(arr,n)
    return arr[-n:]

def shuffle_n(arr,n):

    random.seed(time.time())
    for i in range(len(arr)-1,len(arr)-n-1,-1):
        j = random.randint(0,i)
        arr[i], arr[j] = arr[j], arr[i]

if __name__ == '__main__':
    test()
