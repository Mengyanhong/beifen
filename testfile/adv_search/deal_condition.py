# -*- coding: utf-8 -*-
import pytest,time,yaml
from adv_search.search_API import search_API

import openpyxl
file='条件及条件值.xlsx'
data=openpyxl.load_workbook(file)
condition_name=data['条件']
condition_value=data['条件值']

def class_dict():
    first_class=[]
    first_class_draft=[] #算出None的个数用于后面计算二级分类总数
    for i in range(2,202):
        first_class_draft.append(condition_name['A' + str(i)].value)
        if condition_name['A'+str(i)].value!=None:
            first_class.append(condition_name['A'+str(i)].value)

    sencond_class_num=[]#存储对应二级分类的个数
    sum = 0
    for i in range(len(first_class_draft)):
        if first_class_draft[i]!=None:
            sencond_class_num.append(sum)
            sum=0
        else:
            sum+=1
        if i==len(first_class_draft)-1:
            sencond_class_num.append(sum)

    sencond_class_num=sencond_class_num[1:]
    for i in range(len(sencond_class_num)):
        sencond_class_num[i] += 1 #None+自己 为总个数

    class_dict={} #一级二级分类的字典
    sum = 0
    for i in range(len(first_class)):
        sencond_class = []
        for j in range(2 + sum, sencond_class_num[i] + 2 + sum):
            sencond_class.append(condition_name['B' + str(j)].value)
        class_dict[first_class[i]] = sencond_class
        sum += sencond_class_num[i]  # 计算一级菜单的起始位置
    return class_dict

def value_dict():
    value_dict={}
    column_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N']
    for column in column_list:
        value_list=[]
        for i in range(2,50):
            if condition_value[column+str(i)].value==None:
                break
            else:
                value_list.append(str(condition_value[column+str(i)].value))
        value_dict[condition_value[column+str(1)].value]=value_list
    return value_dict


# level=[]
#
# for i in range(2,300):
#     dict={}
#     level2 = []
#     if sheet_condition['A'+str(i)]!=None:
#         level2.append(sheet_condition['B'+str(i)].value)
#         dict[sheet_condition['A'+str(i)].value]=level2
#     if sheet_condition['A'+str(i)]==None:
#         level2.append(sheet_condition['B' + str(i)].value)

