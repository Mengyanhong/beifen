# -*- coding: utf-8 -*-
import os,sys
con = r'C:\Users\admin\Desktop\新建文本文档 (3).txt'
projectname =  'lixiaoyun'
config = open(con,'r+')

configs = config.read().encode('GBK').decode('GBK')
print(configs)
config.write(configs)
config.seek(0)
# print(config.read())
config.close()

