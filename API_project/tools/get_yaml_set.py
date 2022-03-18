# -*- coding: utf-8 -*-
import yaml
import pprint
import os, sys


def get_yaml_data(fileDir):
    # 1- 读取文件操作---从磁盘读取到内存
    fo = open(fileDir, 'r', encoding="utf-8")  # file_obiect
    # 2- 使用yaml方法获取数据
    response = yaml.load(fo, Loader=yaml.FullLoader)
    fo.close()
    # with open(fileDir,encoding="utf-8") as f:
    #     key_list = yaml.safe_load(f)
    return response


# def set_yaml_data(fileName,inData):
#     fo = open(fileName,'w',encoding="utf-8")
#     yaml.dump(inData,fo)
#     fo.close()
if __name__ == '__main__':
    res = get_yaml_data('../data/yaml/have_or_not_search.yaml')
    print(res)
    # print(a)
    # for one in res:
    #     print(one)
    # print(res)
