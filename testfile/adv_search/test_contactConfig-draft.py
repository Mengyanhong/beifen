# -*- coding: utf-8 -*-
# 来源配置测试
import openpyxl
from adv_search.config_API import configuration_file
import urllib3
urllib3.disable_warnings()

HOST = 'test'
configuration_file = configuration_file(HOST)

staticConfig=configuration_file.staticConfig()['contactSource']
level1_num_api=len(staticConfig)

data=openpyxl.load_workbook('来源站点.xlsx')
sheet_last=data['来源']

for i in range(2,1000):
    if sheet_last['L'+str(i)].value==None:
        level1_num_request=i-2
        break

for i in range(2, 1000):
    if sheet_last['A'+str(i)].value==None:
        level2_num_request=i-2
        break

class TestTradeMarkInventoryCategory:
    def test_level(self):
        level2_sum = 0
        print(staticConfig)

        #判断一级的数量和值
        assert level1_num_api==level1_num_request
        for i in range(level1_num_api):
            print(i)
            assert staticConfig[i]['value']==sheet_last['L'+str(i+2)].value

            #判断二级的数量
            level2_num_api=len(staticConfig[i]['sub'])
            level2_num_request = 0
            for a in range(2,1000):
                if sheet_last['A'+str(a+level2_sum)].value==staticConfig[i]['value']:
                    level2_num_request+=1
                else:
                    level2_sum+=level2_num_request
                    break
            assert level2_num_api==level2_num_request

            # 判断二级的值
            for j in range(level2_num_api):
                assert staticConfig[i]['sub'][j]['value']==sheet_last['B'+str(j+2+level2_sum-level2_num_api)].value
                print(i,j)

