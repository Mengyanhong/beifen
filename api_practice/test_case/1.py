# -*- coding: GBK -*-
# @Time : 2021/7/14 10:55
# @Author : 孟艳红
# @File : test_category.py
import requests


# def categoryL2():
#     Request_URL = 'https://skb.weiwenjia.com/api_skb/v1/shop_search'
#     Request_headers = {
#         'app_token': 'a14cc8b00f84e64b438af540390531e4',
#         'Authorization': f'Token token=18033bf7b969d9b12ef830c66c1f2464',
#         'Content-Type': 'application/json',
#         'crm_platform_type': 'lixiaoyun'
#     }
#     Request_payload = {'shopName': '', 'hasUnfolded': 0, 'hasSyncClue': 0, 'page': 1, 'pagesize': 10,
#                        'condition': {'cn': 'composite', 'cr': 'MUST', 'cv': [
#                            {'cn': 'category', 'cv': {'categoryL1': ['10'], 'categoryL2': ['2714']}, 'cr': 'IN'}]}}
#     response = requests.post(url=Request_URL, headers=Request_headers, json=Request_payload, verify=False)
#     return response.json()
# if __name__ == '__main__':
#     print(categoryL2)

# print(530000-88678)
#
# print(92323-88678)
#
# print(30000-27024)
#
# print(2598+613)

# print('%6d' % (12345))
#
#
# def my_abs(x):
#     if not isinstance(x, (int, float)):
#         raise TypeError('bad operand type')
#     if x >= 0:
#         return x
#     else:
#         return -x
from API_project.tools.Excelread import Excel_Files
excel_file = Excel_Files(file_name="联系方式渠道配置.xlsx", sheel="联系方式渠道配置")  # 实例化Excel用例文件
a = excel_file.open_file_rows("name")
b = excel_file.open_file_rows("value")
print(a)
c = []
c = set(c)
c.add(int(a[b.index("企业梦工厂")]))
c.add(9)
print(b)
print(list(c))
sum1 = 0
for i in range(2001):
    if i % 2== 0:
        sum1 = sum1 +i
print(sum1)
a = [1,2,3,4,5,6]
print(a[1:6:2])
sum = 0
for i in range(0,2001,2):
    sum = sum+i
print(sum)
n1 = 255
n2 = 1000
print(hex(n2))
L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [x.lower() for x in L1 if isinstance(x, str)]
print(L2)
a = 0
b = 1
for i in range(20):
    print(b)
    e = a+b
    a = b
    b = e
    # a,b = b,a+b
#
# def fib(max):
#     n, a, b = 0, 0, 1
#     while n < max:
#         print(b)
#         a, b = b, a + b
#         n = n + 1
#     return 'done'
#
# if __name__ == '__main__':
#     fib(10)
