# -*- coding: utf-8 -*-
# @Time    : 2021/9/8—18:09
# @Author  : 孟艳红
# @File    : te.py
from Configs.search_API import getCompanyBaseInfo
import requests

from Configs.search_API import search
host = 'lxcrm'
data = search(host).search_API('techTypeCompany', [10], 'IN')
# print(data)
# print(len(data['items'])-1)
# print(data['items'])
pid = data['items'][1]['id']
getCompanyBaseInfo = getCompanyBaseInfo(host)
re_tag = getCompanyBaseInfo.getCompanyBase(pid).json()["data"]["tags"]
# a = getCompanyBaseInfo
# print(a.url())
print(getCompanyBaseInfo.getCompanyBase(pid).url)
# print(re_tag)
